import csv
import os
import shutil
from datetime import datetime


def load_existing_qsos(filename, is_adif=False):
    """Reads existing logs to index unique keys and prevent duplicates."""
    existing_records = set()
    if not os.path.isfile(filename):
        return existing_records

    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as f:
            if is_adif:
                content = f.read().lower()
                records = content.split("<eor>")
                for rec in records:
                    if not rec.strip():
                        continue
                    call = extract_adif_field(rec, "call")
                    qso_date = extract_adif_field(rec, "qso_date")
                    time_on = extract_adif_field(rec, "time_on")
                    band = extract_adif_field(rec, "band")
                    if call and qso_date and time_on and band:
                        existing_records.add((call.upper(), qso_date, time_on, band.lower()))
            else:
                reader = csv.DictReader(f)
                for row in reader:
                    unique_key = (
                        str(row.get('call', '')).upper(),
                        str(row.get('qso_date', '')),
                        str(row.get('time_on', '')),
                        str(row.get('band', '')).lower()
                    )
                    existing_records.add(unique_key)
    except Exception:
        pass
    return existing_records


def extract_adif_field(record_str, field_name):
    """Helper to extract data out of ADIF tagged data format."""
    marker = f"<{field_name}:"
    if marker not in record_str:
        return None
    try:
        start = record_str.index(marker) + len(marker)
        length_str = record_str[start:record_str.index(">", start)]
        if ":" in length_str:
            length = int(length_str.split(":")[0])
        else:
            length = int(length_str)
        data_start = record_str.index(">", start) + 1
        return record_str[data_start:data_start + length].strip()
    except Exception:
        return None


def calculate_band_from_freq(freq_mhz):
    """Converts a numerical frequency string or float into its standard HF/VHF/UHF ADIF band string."""
    try:
        f = float(freq_mhz)
        if 1.8 <= f <= 2.0:
            return "160m"
        elif 3.5 <= f <= 4.0:
            return "80m"
        elif 7.0 <= f <= 7.3:
            return "40m"
        elif 10.1 <= f <= 10.15:
            return "30m"
        elif 14.0 <= f <= 14.35:
            return "20m"
        elif 18.068 <= f <= 18.168:
            return "17m"
        elif 21.0 <= f <= 21.45:
            return "15m"
        elif 24.89 <= f <= 24.99:
            return "12m"
        elif 28.0 <= f <= 29.7:
            return "10m"
        elif 50.0 <= f <= 54.0:
            return "6m"
        elif 144.0 <= f <= 148.0:
            return "2m"
        elif 420.0 <= f <= 450.0:
            return "70cm"
        else:
            return "Custom"
    except (ValueError, TypeError):
        return "Unknown"


def create_file_backup(filename):
    """Creates a timestamped backup copy of the target file if it exists."""
    if not os.path.isfile(filename) or os.path.getsize(filename) == 0:
        return True
    try:
        base, ext = os.path.splitext(filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{base}_backup_{timestamp}{ext}"
        shutil.copy2(filename, backup_filename)
        return True
    except Exception as e:
        log_error(f"Backup Failure for {filename}: {str(e)}")
        return False


def log_error(error_message, err_filename="qrz_logging_errors.log"):
    """Appends validation failures to an external error log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(err_filename, mode='a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {error_message}\n")


def export_qrz_log_premium(qso_list, filename="qrz_export.csv", format_type="csv", app_id=None):
    """
    Validates, deduplicates, runs automatic frequency-to-band matching, creates a backup,
    and appends records. Supports custom ADIF application fields.
    """
    format_type = format_type.lower().strip()
    is_adif = format_type in ['adif', 'adi']

    qrz_fields = ['call', 'band', 'mode', 'qso_date', 'time_on', 'freq', 'rst_sent', 'rst_rcvd']

    # 1. Load historical database contacts to prevent duplicate entries
    existing_qsos = load_existing_qsos(filename, is_adif=is_adif)
    valid_qso_list = []

    # 2. Validate, calculate parameters, and deduplicate input data
    for index, qso in enumerate(qso_list):
        try:
            # Ensure mandatory fields (minus band, since we can auto-calculate it)
            required_keys = ['call', 'mode', 'qso_date', 'time_on', 'freq', 'rst_sent', 'rst_rcvd']
            missing_fields = [field for field in required_keys if field not in qso]
            if missing_fields:
                raise ValueError(f"Missing required fields: {missing_fields}")

            # Auto-calculate band if missing or check accuracy if provided
            calculated_band = calculate_band_from_freq(qso['freq'])
            band = str(qso.get('band', calculated_band)).lower().strip()
            if band == "unknown" or band == "custom":
                band = calculated_band

            call = str(qso['call']).upper().strip()
            qso_date = str(qso['qso_date']).strip()
            time_on = str(qso['time_on']).strip()

            qso_key = (call, qso_date, time_on, band)

            if qso_key not in existing_qsos:
                # Build unified dictionary data
                sanitized_qso = qso.copy()
                sanitized_qso['call'] = call
                sanitized_qso['band'] = band
                valid_qso_list.append(sanitized_qso)
                existing_qsos.add(qso_key)

        except Exception as e:
            log_error(f"Index {index} Validation Error: {str(e)} | Content: {qso}")

    if not valid_qso_list:
        print("No new unique records found to append.")
        return

    # 3. Create the safety backup file before changing anything
    if not create_file_backup(filename):
        print("Aborting log export: Backup generation failed. Check permissions.")
        return

    # 4. Write Output
    try:
        if is_adif:
            file_exists = os.path.isfile(filename) and os.path.getsize(filename) > 0
            with open(filename, mode='a' if file_exists else 'w', encoding='utf-8') as f:
                if not file_exists:
                    f.write("ADIF Premium Export File\n")
                    f.write("<EOH>\n\n")

                for qso in valid_qso_list:
                    adif_row = ""
                    # Add standard fields
                    for field in qrz_fields:
                        val = str(qso[field])
                        adif_row += f"<{field}:{len(val)}>{val} "

                    # Inject Custom QRZ Logbook application-specific fields if requested
                    if app_id:
                        app_str = str(app_id)
                        adif_row += f"<app_qrzlog_logid:{len(app_str)}>{app_str} "

                    f.write(adif_row + "<EOR>\n")
        else:
            # Standard CSV fallback generation
            has_valid_header = False
            if os.path.isfile(filename):
                with open(filename, mode='r', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    if next(reader, None) == qrz_fields:
                        has_valid_header = True

            # If writing CSV, application IDs can be appended dynamically as an extra column
            final_fields = qrz_fields + ['app_qrzlog_logid'] if app_id else qrz_fields

            with open(filename, mode='a' if has_valid_header else 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=final_fields, extrasaction='ignore')
                if not has_valid_header:
                    writer.writeheader()
                for qso in valid_qso_list:
                    if app_id:
                        qso['app_qrzlog_logid'] = app_id
                    writer.writerow(qso)

        print(f"Successfully processed entries. Added {len(valid_qso_list)} records to {filename}.")
    except Exception as e:
        log_error(f"File Write System Error: {str(e)}")
        print("File write failed. Technical details saved to error log.")


# ==========================================
# Verification / Execution Test Setup
# ==========================================
if __name__ == "__main__":
    # Notice 'band' is omitted from dictionaries below; the script calculates it automatically from 'freq'
    my_log_data = [
        {'call': 'W7AW', 'mode': 'FT8', 'qso_date': '20260605', 'time_on': '231000', 'freq': '14.074',
         'rst_sent': '-12', 'rst_rcvd': '-15'},
        {'call': 'K1ZZ', 'mode': 'SSB', 'qso_date': '20260605', 'time_on': '231500', 'freq': '7.200', 'rst_sent': '59',
         'rst_rcvd': '57'}
    ]

    # Test ADIF writing with custom QRZ log id tracking injected:
    print("--- Testing Premium ADIF Generation ---")
    export_qrz_log_premium(my_log_data, filename="qrz_premium.adi", format_type="adif", app_id="98765")

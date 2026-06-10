import csv
import hashlib
import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import messagebox


class QSOLogger:
    """
    A unified, real-time logging class compatible with QRZ logbook uploads.
    Displays critical validation and system failures via Tkinter graphical message boxes.
    """

    def __init__(self, format_preference="csv", base_filename="qrz_logbook", app_id=None):
        self.app_id = app_id
        # Expanded fields to explicitly track and format 'app_id' in both CSV and ADIF modes
        self.qrz_fields = ['call', 'band', 'mode', 'qso_date', 'time_on', 'freq', 'rst_sent', 'rst_rcvd', 'app_id']

        # Initialize a hidden Tkinter root window to prevent an empty GUI window from populating
        self._root = tk.Tk()
        self._root.withdraw()

        # Backup rate-limiting variables
        self.backup_interval_minutes = 0  # Default: backup every time (0 minutes)
        self._last_backup_time = None  # Tracks when the last backup happened

        # Initialize state variables and set the filename cleanly using the helper logic
        self.format_preference = format_preference
        self.set_filename(base_filename)

    def set_filename(self, base_filename):
        """
        Dynamically changes the output file target on the fly.
        Automatically reapplies the file extension layout based on format_preference.
        """
        pref = str(self.format_preference).lower().strip() if self.format_preference else "csv"

        if pref in ['adi', 'adif']:
            self.format_type = "adif"
            self.filename = f"{base_filename}.adi"
            self.is_adif = True
        else:
            self.format_type = "csv"
            self.filename = f"{base_filename}.csv"
            self.is_adif = False

        # print(f"Logger target updated. Current output destination: '{self.filename}'")

    def set_backup_interval(self, minutes):
        """Sets the minimum minutes that must elapse before generating a new file backup."""
        try:
            val = float(minutes)
            if val < 0:
                raise ValueError("Interval cannot be negative.")
            self.backup_interval_minutes = val
            # print(f"Backup cooldown interval set to {self.backup_interval_minutes} minutes.")
        except (ValueError, TypeError):
            self._show_gui_error("Configuration Error", "Backup interval must be a valid positive number.")



    def _show_gui_error(self, title, error_message):
        """Displays a graphical error modal using Tkinter."""
        messagebox.showerror(title, error_message)

    def _generate_deterministic_id(self, call, qso_date, time_on, band):
        """
        Generates a reliable unique hash key for a contact.
        If the exact same contact is processed again, it recreates the exact same ID.
        """
        unique_string = f"{call.upper()}-{qso_date}-{time_on}-{band.lower()}"
        return hashlib.md5(unique_string.encode('utf-8')).hexdigest()[:12]

    def _extract_adif_field(self, record_str, field_name):
        """Internal tracking helper for parsing out existing ADIF tags."""
        marker = f"<{field_name}:"
        if marker not in record_str:
            return None
        try:
            start = record_str.index(marker) + len(marker)
            length_str = record_str[start:record_str.index(">", start)]
            length = int(length_str.split(":")) if ":" in length_str else int(length_str)
            data_start = record_str.index(">", start) + 1
            return record_str[data_start:data_start + length].strip()
        except Exception:
            return None



    def _load_existing_qsos(self):
        """Scans the active target file dynamically to index historical records."""
        existing_records = set()
        if not os.path.isfile(self.filename):
            return existing_records

        try:
            with open(self.filename, mode='r', newline='', encoding='utf-8') as f:
                if self.is_adif:
                    content = f.read().lower()
                    records = content.split("<eor>")
                    for rec in records:
                        if not rec.strip():
                            continue
                        call = self._extract_adif_field(rec, "call")
                        qso_date = self._extract_adif_field(rec, "qso_date")
                        time_on = self._extract_adif_field(rec, "time_on")
                        band = self._extract_adif_field(rec, "band")
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
        except Exception as e:
            self._show_gui_error("Log Read Error", f"Could not scan existing log database index:\n{str(e)}")
        return existing_records

    def change_format(self, new_format, force_backup=True):
        """
        Changes the output file extension on the fly while retaining the base filename.
        Forces a file backup instantly by default before switching formats.
        """
        clean_format = str(new_format).lower().strip()
        if clean_format not in ['csv', 'adi', 'adif']:
            self._show_gui_error("Invalid Format", f"'{new_format}' is not supported.")
            return False

        # Create an instant backup of the current file before updating names/formats
        if force_backup:
            self._create_file_backup(force=True)

        current_base = os.path.splitext(self.filename)[0]
        self.format_preference = clean_format
        self.set_filename(current_base)
        return True

    def _create_file_backup(self, force=False):
        """
        Creates a timestamped copy of the active file.
        Honors the time threshold limit unless 'force' is set to True.
        """
        if not os.path.isfile(self.filename) or os.path.getsize(self.filename) == 0:
            return True

        now = datetime.now()

        # Check time threshold ONLY if force is False
        if not force and self._last_backup_time is not None:
            elapsed_minutes = (now - self._last_backup_time).total_seconds() / 60.0
            if elapsed_minutes < self.backup_interval_minutes:
                return True

        try:
            base, ext = os.path.splitext(self.filename)
            timestamp = now.strftime("%Y%m%d_%H%M%S")
            # If it's a forced backup due to format change, label it clearly
            suffix = "_format_switch" if force else ""
            backup_filename = f"{base}_backup_{timestamp}{suffix}{ext}"

            shutil.copy2(self.filename, backup_filename)

            self._last_backup_time = now
            # print(f"Backup created successfully: {backup_filename}")
            return True
        except Exception as e:
            self._show_gui_error("Backup System Failure", f"Failed to backup {self.filename}:\n{str(e)}")
            return False

    def append_qso(self, qso):
        """Validates, deduplicates, and saves a single QSO record down to disk."""
        try:
            required_keys = ['call', 'band', 'mode', 'qso_date', 'time_on', 'freq', 'rst_sent', 'rst_rcvd']
            missing_fields = [field for field in required_keys if field not in qso]
            if missing_fields:
                raise ValueError(f"Missing required fields: {missing_fields}")

            band = str(qso['band']).lower().strip()
            if not band:
                raise ValueError("The field 'band' cannot be empty.")

            call = str(qso['call']).upper().strip()
            qso_date = str(qso['qso_date']).strip()
            time_on = str(qso['time_on']).strip()

            qso_key = (call, qso_date, time_on, band)
        except Exception as e:
            self._show_gui_error("Data Validation Error", f"QSO formatting constraints violated:\n{str(e)}")
            return False

        existing_qsos = self._load_existing_qsos()
        if qso_key in existing_qsos:
            messagebox.showinfo("Duplicate QSO", f"Skipped contact: {call} on {band} already exists in log.")
            return False

        # Regular appending relies on standard time threshold restrictions (force=False)
        if not self._create_file_backup(force=False):
            return False

        sanitized_qso = qso.copy()
        sanitized_qso['call'] = call
        sanitized_qso['band'] = band

        if 'app_id' in sanitized_qso and sanitized_qso['app_id']:
            final_id = str(sanitized_qso['app_id']).strip()
        elif self.app_id:
            final_id = str(self.app_id).strip()
        else:
            final_id = self._generate_deterministic_id(call, qso_date, time_on, band)

        sanitized_qso['app_id'] = final_id

        try:
            file_exists = os.path.isfile(self.filename) and os.path.getsize(self.filename) > 0

            if self.is_adif:
                with open(self.filename, mode='a' if file_exists else 'w', encoding='utf-8') as f:
                    if not file_exists:
                        f.write("ADIF Real-Time Log File Class\n")
                        f.write("<EOH>\n\n")

                    adif_row = ""
                    for field in self.qrz_fields:
                        if field == 'app_id':
                            adif_row += f"<app_qrzlog_logid:{len(final_id)}>{final_id} "
                        else:
                            val = str(sanitized_qso[field])
                            adif_row += f"<{field}:{len(val)}>{val} "
                    f.write(adif_row + "<EOR>\n")
            else:
                with open(self.filename, mode='a' if file_exists else 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=self.qrz_fields)
                    if not file_exists:
                        writer.writeheader()

                    row_data = {field: sanitized_qso.get(field, '') for field in self.qrz_fields}
                    writer.writerow(row_data)

            # print(f"Successfully added record {call} to storage file with ID: {final_id}")
            return True
        except Exception as e:
            self._show_gui_error("File Write Error", f"Could not append record to storage file:\n{str(e)}")
            return False



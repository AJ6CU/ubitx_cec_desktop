import time
import sys
from SDRPlusPlusController import SDRPlusPlusController

MEMORIES = [
    {"freq_hz": 162550000, "mode": "FM", "filter_hz": 15000, "name": "NOAA Weather Radio 1"},
    {"freq_hz": 145000000, "mode": "FM", "filter_hz": 12500, "name": "2m National Calling"},
    {"freq_hz": 7074000, "mode": "USB", "filter_hz": 3000, "name": "40m FT8 Digital Activity"}
]


def on_freq_update(hz):
    print(f"\n[SDR++ Event] Frequency shifted to: {hz / 1e6:.4f} MHz")
    print("Command [freq/mode/band/narrow/widen/filter/log/query/show/clear/exit]: ", end="", flush=True)


def on_filter_update(width):
    print(f"\n[SDR++ Event] Passband adjusted to: {width} Hz")
    print("Command [freq/mode/band/narrow/widen/filter/log/query/show/clear/exit]: ", end="", flush=True)


def on_scan_advance(ch):
    print(f"[Scanner Sweep] Sweeping -> {ch['name']} ({ch['freq_hz'] / 1e6:.4f} MHz - {ch['mode']})")


def main():
    sdr = SDRPlusPlusController(host='127.0.0.1', port=4532)
    sdr.on_frequency_change = on_freq_update
    sdr.on_filter_change = on_filter_update
    sdr.on_scan_step = on_scan_advance

    print("[*] Contacting SDR++ Client Link Layer on Port 4532...")
    if not sdr.connect():
        print("[-] Ensure RigCTL Server is active on port 4532 inside SDR++.")
        return

    print("\n=============================================================")
    print(" DICTIONARY ENGINE INTERFACE PANEL (PORT 4532 ACTIVE)")
    print(" - Type 'log [note]'   ➔ Saves active VFO metrics to the dictionary []")
    print(" - Type 'query [Hz]'   ➔ Checks if a frequency in Hz has a saved log []")
    print(" - Type 'show'         ➔ Dumps out the entire active logging dictionary []")
    print(" - Type 'clear'        ➔ Empties out the dictionary registry database []")
    print("=============================================================\n")

    try:
        while True:
            raw_input = input("Command: ").strip()
            if not raw_input: continue

            user_cmd = raw_input.lower()
            if user_cmd == 'exit': break

            # 1. Handle Log Creation
            if user_cmd == 'log' or user_cmd.startswith('log '):
                note = raw_input[4:].strip() if len(raw_input) > 4 else "Manual Log Entry"
                entry = sdr.log_current_state(description=note)
                print(f"[✔ SAVED TO DICT] Key: {sdr.current_frequency} Hz -> Data: {entry}")

            # 2. Handle Dictionary Queries []
            elif user_cmd.startswith('query '):
                hz_str = user_cmd[6:].strip()
                if hz_str.isdigit():
                    result = sdr.query_logs(int(hz_str))
                    if result:
                        print(f"[Query Hit] Match Found for {hz_str} Hz:\n  -> {result}")
                    else:
                        print(f"[Query Miss] No dictionary keys found matching {hz_str} Hz.")
                else:
                    print(
                        "[-] Usage Error: Type 'query' followed by an integer frequency in Hz (e.g., 'query 7074000').")

            # 3. Dump out everything inside the log store []
            elif user_cmd == 'show':
                all_logs = sdr.get_all_logs()
                if not all_logs:
                    print("[!] The internal tracking dictionary database is completely empty.")
                else:
                    print(f"\n--- CURRENT IN-MEMORY LOG DICTIONARY ({len(all_logs)} Entries) ---")
                    for key_hz, data in all_logs.items():
                        print(f" Key [{key_hz} Hz] ➔ {data}")
                    print("----------------------------------------------------------------\n")

            # 4. Clear memory []
            elif user_cmd == 'clear':
                sdr.clear_logs()
                print("[✔ MEMORY PURGED] The internal log store dictionary has been emptied.")

            # Standard Tuning and Passband commands
            elif user_cmd == 'filter':
                print(f"[Query Result] Current Filter Width: {sdr.get_filter_width_hz()} Hz (Mode: {sdr.current_mode})")
            elif user_cmd == 'scan':
                print("[!] Launching memory block scanner...")
                sdr.start_memory_scan(MEMORIES, delay_seconds=2.5)
            elif user_cmd == 'stop':
                sdr.stop_scan()
                print("[!] Scanner stopped.")
            elif user_cmd == 'widen':
                sdr.widen(200)
            elif user_cmd == 'narrow':
                sdr.narrow(200)
            elif user_cmd in ['usb', 'lsb', 'cw', 'am', 'wfm', 'fm']:
                sdr.stop_scan()
                sdr.set_mode(user_cmd, 0)
            elif user_cmd in sdr.HAM_BANDS:
                sdr.stop_scan()
                sdr.change_band(user_cmd)
            else:
                try:
                    mhz_val = float(user_cmd)
                    sdr.stop_scan()
                    sdr.set_frequency_mhz(mhz_val)
                except ValueError:
                    print(f"[-] Input string parsing exception token: '{raw_input}'")

    except KeyboardInterrupt:
        pass
    finally:
        sdr.disconnect()
        print("\nConnection safely dropped.")


if __name__ == "__main__":
    main()

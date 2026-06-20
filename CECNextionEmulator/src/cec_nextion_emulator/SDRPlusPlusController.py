import socket
import time
import threading
from datetime import datetime
from typing import List, Dict, Union


class SDRPlusPlusController:
    """
    An advanced object-oriented controller to interface with SDR++ using
    the Hamlib RigCTL network protocol wrapper on default Port 4532.
    Includes an in-memory dictionary log store.
    """

    HAM_BANDS = {
        '80m': (3500000, 'LSB', 2700),
        '40m': (7074000, 'USB', 3000),
        '20m': (14200000, 'USB', 2400),
        '15m': (21074000, 'USB', 3000),
        '10m': (28400000, 'USB', 2400),
        '2m': (145000000, 'FM', 12500)
    }

    DEFAULT_FILTER_FALLBACKS = {
        'USB': 2400, 'LSB': 2400, 'CW': 500, 'AM': 6000, 'NFM': 12500, 'FM': 12500, 'WFM': 180000
    }

    def __init__(self, host: str = '127.0.0.1', port: int = 4532):
        self.host = host
        self.port = port
        self.sock = None
        self.is_connected = False
        self.running = False

        # State tracking cache variables
        self.current_frequency = 0
        self.current_mode = "UNKNOWN"
        self.current_filter_width = 2400

        # --- NEW: In-Memory Dictionary Logger Storage ---
        # Key: Frequency in Hz (int) -> Value: Dictionary of telemetry metadata
        self.logged_signals: Dict[int, Dict[str, Union[str, int, float]]] = {}

        # Scanner properties
        self.scan_thread = None
        self.is_scanning = False
        self._scan_stop_event = threading.Event()

        # Public system callbacks
        self.on_frequency_change = None
        self.on_mode_change = None
        self.on_filter_change = None
        self.on_scan_step = None

    def connect(self) -> bool:
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(1.5)
            self.sock.connect((self.host, self.port))
            self.is_connected = True
            self.running = True
            self.monitor_thread = threading.Thread(target=self._update_loop, daemon=True)
            self.monitor_thread.start()
            return True
        except Exception as e:
            print(f"[-] Connection failed to SDR++ at {self.host}:{self.port} -> {e}")
            self.is_connected = False
            return False

    def disconnect(self):
        self.stop_scan()
        self.running = False
        if self.sock:
            try:
                self.sock.close()
            except socket.error:
                pass
        self.is_connected = False

    # =========================================================================
    #  DICTIONARY LOGGING MANAGEMENT METHODS
    # =========================================================================

    def log_current_state(self, description: str = "Manual Log Entry") -> Dict[str, Union[str, int, float]]:
        """
        Gathers current VFO parameters and saves them into the internal dictionary.
        Uses the active frequency (Hz) as the dictionary key.
        """
        # Ensure we have the most accurate current filter value mapped
        self.get_filter_width_hz()

        hz_key = self.current_frequency
        mhz_val = hz_key / 1_000_000
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_entry = {
            "timestamp": timestamp_str,
            "mhz": mhz_val,
            "mode": self.current_mode,
            "filter_hz": self.current_filter_width,
            "description": description if description else "Manual Log Entry"
        }

        # Save into the object's dictionary matching the target Hz key entry
        self.logged_signals[hz_key] = log_entry
        return log_entry

    def query_logs(self, freq_hz: int) -> Union[Dict[str, Union[str, int, float]], None]:
        """Queries the internal log store for a specific frequency in Hz. Returns None if missing."""
        return self.logged_signals.get(int(freq_hz), None)

    def clear_logs(self):
        """Completely clears out the internal dictionary log registry."""
        self.logged_signals.clear()

    def get_all_logs(self) -> Dict[int, Dict[str, Union[str, int, float]]]:
        """Returns the full dictionary collection of logged signals."""
        return self.logged_signals

    # =========================================================================
    #  CORE TRANSCEIVER TUNING METHODS
    # =========================================================================

    def set_frequency_hz(self, hz: int) -> bool:
        if not self.is_connected: return False
        try:
            cmd = f"F {int(hz)}\n".encode('utf-8')
            self.sock.sendall(cmd)
            self.sock.recv(1024)
            return True
        except socket.error:
            self.is_connected = False
            return False

    def set_frequency_mhz(self, mhz: float) -> bool:
        return self.set_frequency_hz(int(mhz * 1_000_000))

    def set_mode(self, mode: str, passband_hz: int = 0) -> bool:
        if not self.is_connected: return False
        target_mode = mode.upper()
        if passband_hz == 0:
            passband_hz = self.DEFAULT_FILTER_FALLBACKS.get(target_mode, 2400)
        try:
            cmd = f"M {target_mode} {int(passband_hz)}\n".encode('utf-8')
            self.sock.sendall(cmd)
            self.sock.recv(1024)
            self.current_mode = target_mode
            self.current_filter_width = passband_hz
            return True
        except socket.error:
            self.is_connected = False
            return False

    def set_filter_width_hz(self, passband_hz: int) -> bool:
        if not self.is_connected or self.current_mode == "UNKNOWN": return False
        return self.set_mode(self.current_mode, max(50, passband_hz))

    def get_filter_width_hz(self) -> int:
        self._sync_mode_only()
        return self.current_filter_width

    def widen(self, step_hz: int = 200) -> bool:
        new_width = self.current_filter_width + step_hz
        return self.set_filter_width_hz(new_width)

    def narrow(self, step_hz: int = 200) -> bool:
        new_width = self.current_filter_width - step_hz
        return self.set_filter_width_hz(new_width)

    def change_band(self, band_name: str) -> bool:
        band = band_name.lower().strip()
        if band in self.HAM_BANDS:
            hz, mode, default_width = self.HAM_BANDS[band]
            self.set_frequency_hz(hz)
            time.sleep(0.05)
            self.set_mode(mode, default_width)
            return True
        return False

    def start_memory_scan(self, channels: List[Dict[str, Union[int, str]]], delay_seconds: float = 2.0):
        if self.is_scanning: return
        self.is_scanning = True
        self._scan_stop_event.clear()
        self.scan_thread = threading.Thread(target=self._run_scan, args=(channels, delay_seconds), daemon=True)
        self.scan_thread.start()

    def stop_scan(self):
        if self.is_scanning:
            self._scan_stop_event.set()
            if self.scan_thread: self.scan_thread.join(timeout=2.0)
            self.is_scanning = False

    def _sync_mode_only(self):
        if not self.is_connected: return
        try:
            self.sock.sendall(b'm\n')
            mode_resp = self.sock.recv(1024).decode('utf-8').strip()
            clean_lines = mode_resp.replace('RPRT 0', '').strip().split('\n')
            if clean_lines and clean_lines[0].strip():
                mode_val = clean_lines[0].strip().upper()
                if mode_val != self.current_mode:
                    self.current_mode = mode_val
                    self.current_filter_width = self.DEFAULT_FILTER_FALLBACKS.get(mode_val, 2400)
        except socket.error:
            pass

    def _run_scan(self, channels: List[Dict[str, Union[int, str]]], delay: float):
        idx = 0
        while not self._scan_stop_event.is_set() and self.is_connected:
            current_ch = channels[idx]
            self.set_frequency_hz(current_ch["freq_hz"])
            time.sleep(0.05)
            width = current_ch.get("filter_hz", 0)
            self.set_mode(str(current_ch["mode"]), width)
            if self.on_scan_step: self.on_scan_step(current_ch)
            elapsed = 0.0
            while elapsed < delay:
                if self._scan_stop_event.is_set(): return
                time.sleep(0.1)
                elapsed += 0.1
            idx = (idx + 1) % len(channels)

    def _update_loop(self):
        while self.running and self.is_connected:
            if self.is_scanning:
                time.sleep(0.5)
                continue
            try:
                self.sock.sendall(b'f\n')
                freq_resp = self.sock.recv(1024).decode('utf-8').strip()
                clean_freq = freq_resp.replace('RPRT 0', '').strip()
                if clean_freq.isdigit():
                    freq_val = int(clean_freq)
                    if freq_val != self.current_frequency:
                        self.current_frequency = freq_val
                        if self.on_frequency_change: self.on_frequency_change(freq_val)
                time.sleep(0.05)
                self._sync_mode_only()
            except (socket.timeout, socket.error):
                pass
            time.sleep(0.2)

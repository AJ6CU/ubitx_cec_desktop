import socket
import time
import sys
import threading

# CONFIGURATION: Match the port displayed in your SDR++ RigCTL Server panel
SDR_HOST = '127.0.0.1'
SDR_PORT = 453214.032  # Usually 4533 or 4532

# Global flag to cleanly close threads on exit
running = True


def monitor_sdr(sock):
    """
    Background loop that continuously polls SDR++ for frequency and mode changes.
    """
    global running
    last_freq = 0
    last_mode = ""

    while running:
        try:
            # 1. Check Frequency
            sock.sendall(b'f\n')
            freq_resp = sock.recv(1024).decode('utf-8').strip()
            clean_freq = freq_resp.replace('RPRT 0', '').strip()

            if clean_freq.isdigit():
                current_freq = int(clean_freq)
                if current_freq != last_freq:
                    print(f"\n[SDR++ Update] Frequency: {current_freq / 1_000_000:.6f} MHz")
                    last_freq = current_freq
                    print("Enter command (e.g., '14.200', 'usb', 'lsb', 'cw'): ", end="", flush=True)

            time.sleep(0.05)

            # 2. Check Mode
            sock.sendall(b'm\n')
            mode_resp = sock.recv(1024).decode('utf-8').strip()
            clean_mode_data = mode_resp.replace('RPRT 0', '').strip().split('\n')

            if clean_mode_data and clean_mode_data[0]:
                current_mode = clean_mode_data[0].upper()
                if current_mode != last_mode:
                    print(f"\n[SDR++ Update] Mode: {current_mode}")
                    last_mode = current_mode
                    print("Enter command (e.g., '14.200', 'usb', 'lsb', 'cw'): ", end="", flush=True)

        except (socket.timeout, socket.error):
            pass

        time.sleep(0.2)


def main():
    global running
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(2.0)

    try:
        print(f"Connecting to SDR++ RigCTL Server at {SDR_HOST}:{SDR_PORT}...")
        client_socket.connect((SDR_HOST, SDR_PORT))
        print("Connected successfully!")
        print("=============================================================")
        print(" HOW TO CONTROL SDR++ FROM THIS TERMINAL:")
        print(" - Type a frequency in MHz to jump to it (e.g., '101.1' or '14.200')")
        print(" - Type a mode name to change filters (e.g., 'usb', 'lsb', 'cw', 'am', 'wfm')")
        print(" - Type 'exit' to quit.")
        print("=============================================================\n")
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

    # Start the background listener thread
    listener_thread = threading.Thread(target=monitor_sdr, args=(client_socket,), daemon=True)
    listener_thread.start()

    # Main thread handles user input commands
    try:
        while True:
            user_input = input("Enter command (e.g., '14.200', 'usb', 'lsb', 'cw'): ").strip().lower()

            if not user_input:
                continue
            if user_input == 'exit':
                break

            # Handle Mode Commands
            if user_input in ['usb', 'lsb', 'cw', 'am', 'wfm', 'fm', 'raw']:
                # Format: M [MODE] [PASSBAND] (Using 0 tells SDR++ to use its default width)
                cmd = f"M {user_input.upper()} 0\n".encode('utf-8')
                client_socket.sendall(cmd)
                # Read acknowledgement from server
                client_socket.recv(1024)

                # Handle Frequency Commands (checks if input looks like a floating-point number)
            else:
                try:
                    mhz = float(user_input)
                    hz = int(mhz * 1_000_000)
                    # Format: F [FREQUENCY IN HZ]
                    cmd = f"F {hz}\n".encode('utf-8')
                    client_socket.sendall(cmd)
                    client_socket.recv(1024)
                except ValueError:
                    print(f"[!] Unknown input command: '{user_input}'")

    except KeyboardInterrupt:
        pass
    finally:
        print("\nClosing connection...")
        running = False
        client_socket.close()


if __name__ == "__main__":
    main()

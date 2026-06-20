import socket
import time
import sys

# CHANGE THIS to match the exact port displayed in your SDR++ RigCTL Server panel
SDR_HOST = '127.0.0.1'
SDR_PORT = 4532  # Usually 4533 or 4532 for SDR++


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(2.0)

    try:
        print(f"Connecting to SDR++ RigCTL Server at {SDR_HOST}:{SDR_PORT}...")
        client_socket.connect((SDR_HOST, SDR_PORT))
        print("Connected successfully! Polling SDR++ frequency changes...\n")
    except Exception as e:
        print(f"Connection failed: {e}")
        print("Fix: Ensure you typed a name, clicked '+', and pressed 'Start' in SDR++.")
        sys.exit(1)

    last_freq = 0

    try:
        while True:
            try:
                # 'f\n' is the official universal Hamlib command to "get frequency"
                client_socket.sendall(b'f\n')

                # Read the response back from SDR++
                response = client_socket.recv(1024).decode('utf-8').strip()

                if response:
                    # Strip out generic success tokens if they appear
                    clean_resp = response.replace('RPRT 0', '').strip()

                    if clean_resp.isdigit():
                        current_freq = int(clean_resp)

                        # Only print to the terminal when the frequency actually changes!
                        if current_freq != last_freq:
                            freq_mhz = current_freq / 1_000_000
                            print(f"[!] FREQUENCY CHANGED -> {freq_mhz:.6f} MHz ({current_freq} Hz)")
                            last_freq = current_freq

            except socket.timeout:
                print("[Warning] Polling timed out... retrying.")

            # Poll 5 times a second so it catches fast scrolling wheels instantly
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\nStopping frequency monitor script.")
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()

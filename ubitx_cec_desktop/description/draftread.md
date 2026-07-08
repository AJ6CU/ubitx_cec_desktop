# uBITX CEC Desktop
> **The Visual Control of KD8CEC Firmware.**

`uBITX_CEC_Desktop` is a cross-platform desktop application for KD8CEC-powered uBITX radios featuring zero hardware modifications and a fully integrated SDR-based panadapter. By leveraging the existing Nextion serial protocol via a simple inline TTL-to-USB/Wi-Fi adapter, it delivers high-speed rig control and real-time spectrum visualization without touching a soldering iron to your main board.

---

## 🚀 Features

* **No Solder, No Mods:** Plugs inline with your existing Nextion display setup—zero risk to your radio.
* **Bi-Directional SDR++ Integration:** Changing frequency or mode on the radio updates SDR++, and clicking the SDR++ waterfall instantly retunes the physical transceiver.
* **Automated SDR Dashboard:** Launches instantly when entering SDR mode, providing quick hotkeys for ham bands and operating modes.
* **Memory Banks & Scanning:** Create organized channel banks and scan through them natively from your laptop.
* **Second Nano Telemetry:** Full support for Ian's (KD8CEC) "Second Nano" feature, giving you real-time SWR/Power monitoring and an integrated CW-to-text decoder window.
* **One-Click Quick Logging:** Hit the "Log" button to instantly grab your current VFO, mode, date, and time. Automatically exports to standard **ADIF (.adi)** or **CSV** formats for easy importing into Logbook of the World (LotW), QRZ, or HRD.
* **Cross-Platform Compatibility:** Distributed as a Python Wheel to run natively anywhere Python is supported.

---

## 🔌 Hardware Setup

If your uBITX already has a Nextion display installed, installation requires absolutely zero internal modifications:

1. **Unplug** your Nextion display's data cable from the Raduino/uBITX header.
2. **Connect** that cable into an inline Y-splitter or pass-through cable adapter.
3. **Plug** the data tap end of your cable into a **TTL-to-USB** or **TTL-to-Wi-Fi** module.
4. **Connect** the module to your laptop.

The software seamlessly listens to and injects Nextion protocol packets to drive your physical screen, your Second Nano board, and the desktop application in perfect sync.

---

## 💻 Installation & First Launch

Because the application is packaged as a standard Python Wheel, it features universal cross-platform compatibility across **Windows, Linux (including Raspberry Pi), and macOS**.

### 1. Install via pip
Ensure you have Python installed, open your terminal, and run:
```bash
pip install uBITX_CEC_Desktop
```

### 2. Run the Application
Launch the software directly from your terminal:
```bash
ubitx-cec-desktop
```

### 3. Zero-Configuration Startup
There is no tedious manual configuration required. On initial startup, the application will automatically:
* Scan your system to discover and connect to the active COM port or TTL-to-Wi-Fi bridge.
* Auto-initialize the communication link with your active SDR++ instance.

---

## 🤝 License & Community
This project is open-source and dedicated to the uBITX and KD8CEC amateur radio community. 

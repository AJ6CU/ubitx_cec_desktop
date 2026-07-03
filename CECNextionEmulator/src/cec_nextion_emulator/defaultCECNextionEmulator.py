# Calibrated CEC Nextion Emulator Unified Configuration Data Profile Module

default_config_data = {
    "CW BFO": "",
    "CW Copy VFOA to VFOB on Split": "True",
    "CW Delay Before TX": "500",
    "CW Delay Returning to RX": "5000",
    "CW Key Type": "STRAIGHT",
    "CW Speed": "10",
    "CW Tone": "600",
    "Callsign": "",
    "DSP": "True",
    "Logbook Backup Interval": "30",
    "Logbook Location": "~",
    "Logbook Name": "uBITX_Logbook",
    "Logbook Switch": "False",
    "Logbook Type": "ADI",
    "MCU Command Headroom": 0.09,
    "MCU Read Wait Period": 0.04,
    "MCU Update Period": 250,
    "Master Cal": "",
    "NUMBER DELIMITER": ".",
    "PWR Factor": "1.00",
    "PWR SWR": "False",
    "SSB BFO": "",
    "SWR Factor": "1.00",
    "Scan Channels Registry Queue": {
        "DEFAULT SET": [
            {
                "bandwidth": 2400,
                "freq_hz": 1840000,
                "label": "160M-VOX",
                "mode": "LSB",
                "name": "160m - Voice / Calling"
            },
            {
                "bandwidth": 2400,
                "freq_hz": 3885000,
                "label": "80M-AM",
                "mode": "LSB",
                "name": "80m - AM / Ragchew"
            },
            {
                "bandwidth": 2400,
                "freq_hz": 7200000,
                "label": "40M-LSB",
                "mode": "LSB",
                "name": "40m - LSB Voice Calling"
            },
            {
                "bandwidth": 500,
                "freq_hz": 7074000,
                "label": "40M-FT8",
                "mode": "USB",
                "name": "40m - FT8 Digital"
            },
            {
                "bandwidth": 2400,
                "freq_hz": 14300000,
                "label": "20M-MNET",
                "mode": "USB",
                "name": "20m - Intercon Marine / Maritime Mobile"
            },
            {
                "bandwidth": 2400,
                "freq_hz": 14230000,
                "label": "20M-SSTV",
                "mode": "USB",
                "name": "20m - SSTV (Slo-Scan TV)"
            },
            {
                "bandwidth": 500,
                "freq_hz": 14074000,
                "label": "20M-FT8",
                "mode": "USB",
                "name": "20m - FT8 Digital"
            },
            {
                "bandwidth": 2400,
                "freq_hz": 18130000,
                "label": "17M-USB",
                "mode": "USB",
                "name": "17m - USB Voice Calling"
            },
            {
                "bandwidth": 2400,
                "freq_hz": 21300000,
                "label": "15M-USB",
                "mode": "USB",
                "name": "15m - USB Voice Calling"
            },
            {
                "bandwidth": 2400,
                "freq_hz": 24950000,
                "label": "12M-USB",
                "mode": "USB",
                "name": "12m - USB Voice Calling"
            },
            {
                "bandwidth": 2400,
                "freq_hz": 28400000,
                "label": "10M-USB",
                "mode": "USB",
                "name": "10m - Tech / General Voice Calling"
            }
        ],
        "VHF LOCAL": []
    },
    "Scan On Station Time": 5000,
    "Scan Set Settings": [
        [
            0,
            "None"
        ],
        [
            1,
            "None"
        ],
        [
            2,
            "None"
        ],
        [
            3,
            "None"
        ],
        [
            4,
            "None"
        ],
        [
            5,
            "None"
        ],
        [
            6,
            "None"
        ],
        [
            7,
            "None"
        ],
        [
            8,
            "None"
        ],
        [
            9,
            "None"
        ],
        [
            10,
            "None"
        ],
        [
            11,
            "None"
        ],
        [
            12,
            "None"
        ],
        [
            13,
            "None"
        ],
        [
            14,
            "None"
        ],
        [
            15,
            "None"
        ],
        [
            16,
            "None"
        ],
        [
            17,
            "None"
        ],
        [
            18,
            "None"
        ],
        [
            19,
            "None"
        ]
    ],
    "SDR":"False",
    "Serial Port": "/dev/cu.usbserial-A5069RR4",
    "TXOffset": "EEPROM",
    "VFO Touch Optimized": "True",
    "Virtual Keyboard Switch": "True"
}

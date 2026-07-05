#!/usr/bin/python3
"""
settingsSDR

Used to save of machines

UI source file: settingsSDR.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.simpletooltip import Tooltip


def safe_i18n_translator(value):
    """i18n - Setup translator in derived class file"""
    return value


def safe_fo_callback(widget):
    """on first objec callback - Setup callback in derived class file."""
    pass


def safe_image_loader(master, image_name: str):
    """Image loader - Setup image_loader in derived class file."""
    img = None
    try:
        img = tk.PhotoImage(file=image_name, master=master)
    except tk.TclError:
        pass
    return img


#
# Base class definition
#
class settingsSDRUI(ttk.Labelframe):
    def __init__(
        self,
        master=None,
        *,
        translator=None,
        on_first_object_cb=None,
        data_pool=None,
        image_loader=None,
        **kw
    ):
        if translator is None:
            translator = safe_i18n_translator
        _ = translator  # i18n string marker.
        if image_loader is None:
            image_loader = safe_image_loader
        if on_first_object_cb is None:
            on_first_object_cb = safe_fo_callback

        super().__init__(master, **kw)

        frame1 = ttk.Frame(self)
        frame1.configure(height=200, style="Normal.TFrame", width=200)
        # First object created
        on_first_object_cb(frame1)

        self.SDR_Frame = ttk.Frame(frame1, name="sdr_frame")
        self.SDR_Frame.configure(
            height=200,
            style="NormalOutline.TFrame",
            width=200)
        self.enableSDR_Frame = ttk.Frame(
            self.SDR_Frame, name="enablesdr_frame")
        self.enableSDR_Frame.configure(
            height=200, style="Normal.TFrame", width=200)
        self.SDR_Enable_Label = ttk.Label(
            self.enableSDR_Frame, name="sdr_enable_label")
        self.SDR_Enable_Label.configure(
            state="disabled",
            style="Heading1b.TLabel",
            text='Enable SDR')
        self.SDR_Enable_Tooltip = Tooltip(self.SDR_Enable_Label)
        self.SDR_Enable_Tooltip.configure(
            padx=8,
            relief="raised",
            text='Enable/disable use of external SDR software to provide a Panadapter.',
            wraplength=300)
        self.SDR_Enable_Label.pack(padx="10 5", side="left")
        self.SDR_Enable_Menubutton = ttk.Menubutton(
            self.enableSDR_Frame, name="sdr_enable_menubutton")
        self.SDR_Enable_VAR = tk.StringVar()
        self.SDR_Enable_Menubutton.configure(
            style="Heading0.TMenubutton",
            takefocus=True,
            textvariable=self.SDR_Enable_VAR,
            width=5)
        self.SDR_Enable_Menu = tk.Menu(
            self.SDR_Enable_Menubutton,
            name="sdr_enable_menu")
        self.SDR_Enable_Menu.configure(tearoff=False)
        self.SDR_Enable_Menu.add(
            "command",
            command=self.selectSDR_On_CB,
            font="{Arial} 24 {}",
            label='True',
            state="normal")
        self.SDR_Enable_Menu.add(
            "command",
            command=self.selectSDR_Off_CB,
            font="{Arial} 24 {}",
            label='False',
            state="normal")
        self.SDR_Enable_Menubutton.configure(menu=self.SDR_Enable_Menu)
        self.SDR_Enable_Menubutton.pack(padx="70 0", side="left")
        self.enableSDR_Frame.grid(
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            row=0,
            sticky="ew")
        self.sdrSoftwareSelection_Frame = ttk.Frame(
            self.SDR_Frame, name="sdrsoftwareselection_frame")
        self.sdrSoftwareSelection_Frame.configure(
            height=200, style="Normal.TFrame", width=200)
        self.sdrSoftware_Label = ttk.Label(
            self.sdrSoftwareSelection_Frame,
            name="sdrsoftware_label")
        self.sdrSoftware_Label.configure(
            state="disabled",
            style="Heading1b.TLabel",
            text='SDR Software')
        self.sdrSoftware_Tooltip = Tooltip(self.sdrSoftware_Label)
        self.sdrSoftware_Tooltip.configure(
            padx=8,
            relief="raised",
            text='Select the external SDR software used. Only sdr++ is tested. Others may work if they support rigctl but they cannot be auto started.',
            wraplength=300)
        self.sdrSoftware_Label.grid(
            column=0, padx="10 5", pady=5, row=0, sticky="w")
        self.sdrSoftware_Menubutton = ttk.Menubutton(
            self.sdrSoftwareSelection_Frame, name="sdrsoftware_menubutton")
        self.SDR_Software_VAR = tk.StringVar()
        self.sdrSoftware_Menubutton.configure(
            style="Heading0.TMenubutton",
            takefocus=True,
            textvariable=self.SDR_Software_VAR,
            width=5)
        self.sdrSoftware_Menu = tk.Menu(
            self.sdrSoftware_Menubutton,
            name="sdrsoftware_menu")
        self.sdrSoftware_Menu.configure(tearoff=False)
        self.sdrSoftware_Menu.add(
            "command",
            command=self.selectSDRPlusPlus_CB,
            font="{Arial} 24 {}",
            label='sdr++',
            state="normal")
        self.sdrSoftware_Menubutton.configure(menu=self.sdrSoftware_Menu)
        self.sdrSoftware_Menubutton.grid(column=1, padx="43 10", pady=5, row=0)
        self.autostartSDR_Checkbox = ttk.Checkbutton(
            self.sdrSoftwareSelection_Frame, name="autostartsdr_checkbox")
        self.autostartSDR_VAR = tk.StringVar()
        self.autostartSDR_Checkbox.configure(
            offvalue=False,
            onvalue=True,
            style="Checkbox1b.TCheckbutton",
            text='Autostart',
            variable=self.autostartSDR_VAR)
        self.autostartSDR_Checkbox.grid(column=2, padx="75 0", row=0)
        self.autostartSDR_Checkbox.configure(command=self.autostartSDR_CB)
        self.sdrSoftwareSelection_Frame.grid(
            column=0, columnspan=2, padx=10, pady=10, row=1, sticky="ew")
        self.SDR_Frame.grid(column=0, columnspan=2, row=0, sticky="ew")
        self.SDR_Network_Frame = ttk.Frame(frame1, name="sdr_network_frame")
        self.SDR_Network_Frame.configure(
            height=200, style="NormalOutline.TFrame", width=200)
        self.heading_Frame = ttk.Frame(
            self.SDR_Network_Frame, name="heading_frame")
        self.heading_Frame.configure(
            height=200, style="Normal.TFrame", width=200)
        self.networkAddress_Label = ttk.Label(
            self.heading_Frame, name="networkaddress_label")
        self.networkAddress_Label.configure(
            state="disabled",
            style="Heading1b.TLabel",
            text='SDR Network Address')
        self.networkAddress_Tooltip = Tooltip(self.networkAddress_Label)
        self.networkAddress_Tooltip.configure(
            padx=8,
            relief="raised",
            text='Match the entries here to the SDR++ settings under the Module Manager for Rigctl Server',
            wraplength=300)
        self.networkAddress_Label.pack(anchor="w", side="top")
        self.networkAddressSuggestion_Label = ttk.Label(
            self.heading_Frame, name="networkaddresssuggestion_label")
        self.networkAddressSuggestion_Label.configure(
            style="Heading2bi.TLabel",
            text='Usually 127.0.0.1 or localhost with port 4532 or 4533 (less common)',
            width=60)
        self.networkAddressSuggestion_Label.pack(side="left")
        self.heading_Frame.grid(
            column=0,
            columnspan=2,
            padx=10,
            pady="10 0",
            row=0,
            sticky="w")
        self.address_Frame = ttk.Frame(
            self.SDR_Network_Frame, name="address_frame")
        self.address_Frame.configure(
            height=200, style="Normal.TFrame", width=200)
        self.ipAddress_Label = ttk.Label(
            self.address_Frame, name="ipaddress_label")
        self.ipAddress_Label.configure(
            state="disabled",
            style="Heading1b.TLabel",
            text='Network address:')
        self.tooltip2 = Tooltip(self.ipAddress_Label)
        self.tooltip2.configure(
            padx=8,
            relief="raised",
            text='This is the internal loopback IP address of your machine. Unless you really know what you are doing, you should not change it. If you must, edit the .ini file in your home directory.',
            wraplength=300)
        self.ipAddress_Label.pack()
        self.ipAddress_Entry = ttk.Entry(
            self.address_Frame, name="ipaddress_entry")
        self.networkAddress_VAR = tk.StringVar(value='999.9.9.9')
        self.ipAddress_Entry.configure(
            font="{Arial} 24 {}",
            justify="right",
            state="disabled",
            takefocus=True,
            textvariable=self.networkAddress_VAR,
            width=8)
        _text_ = '999.9.9.9'
        self.ipAddress_Entry["state"] = "normal"
        self.ipAddress_Entry.delete("0", "end")
        self.ipAddress_Entry.insert("0", _text_)
        self.ipAddress_Entry["state"] = "disabled"
        self.ipAddress_Entry.pack()
        self.port_Label = ttk.Label(self.address_Frame, name="port_label")
        self.port_Label.configure(
            state="disabled",
            style="Heading1b.TLabel",
            text='Port:')
        self.port_Tooltip = Tooltip(self.port_Label)
        self.port_Tooltip.configure(
            padx=8,
            relief="raised",
            text='Check SDR++ Module Manager/Rigel Server entry. Typically 4532 or perghaps 4533.',
            wraplength=300)
        self.port_Label.pack(pady="10 0")
        self.tooltip3 = Tooltip(self.address_Frame)
        self.tooltip3.configure(
            padx=8,
            relief="raised",
            text='Check SDR++ Module Manager/Rigel Server entry. Typically 4532 or perhaps 4533.',
            wraplength=300)
        self.port_Entry = ttk.Entry(self.address_Frame, name="port_entry")
        self.networkPort_VAR = tk.StringVar(value='4532')
        self.port_Entry.configure(
            font="{Arial} 24 {}",
            justify="right",
            takefocus=True,
            textvariable=self.networkPort_VAR,
            width=5)
        _text_ = '4532'
        self.port_Entry.delete("0", "end")
        self.port_Entry.insert("0", _text_)
        self.port_Entry.pack()
        self.address_Frame.grid(padx=200, pady=20, row=1)
        self.SDR_Network_Frame.grid(
            column=0,
            columnspan=2,
            pady="10 0",
            row=2,
            sticky="ew")
        self.defaultBandwidth_Frame = ttk.Frame(
            frame1, name="defaultbandwidth_frame")
        self.defaultBandwidth_Frame.configure(
            height=200, style="NormalOutline.TFrame", width=200)
        self.defaultBandwidth_Title_Label = ttk.Label(
            self.defaultBandwidth_Frame, name="defaultbandwidth_title_label")
        self.defaultBandwidth_Title_Label.configure(
            state="disabled", style="Heading1b.TLabel", text='Default Bandwidth')
        self.tooltip11 = Tooltip(self.defaultBandwidth_Title_Label)
        self.tooltip11.configure(
            padx=8,
            relief="raised",
            text='Match the entries here to the SDR++ settings under the Module Manager for Rigctl Server',
            wraplength=300)
        self.defaultBandwidth_Title_Label.pack(
            anchor="w", padx=10, pady=10, side="top")
        self.tooltip6 = Tooltip(self.defaultBandwidth_Frame)
        self.tooltip6.configure(
            padx=8,
            relief="raised",
            text='Match the entries here to the SDR++ settings under the Module Manager for Rigctl Server',
            wraplength=300)
        self.cwBandwidth_Frame = ttk.Frame(
            self.defaultBandwidth_Frame,
            name="cwbandwidth_frame")
        self.cwBandwidth_Frame.configure(
            height=200, style="Normal.TFrame", width=200)
        self.cwDefaultBandwidth_Label = ttk.Label(
            self.cwBandwidth_Frame, name="cwdefaultbandwidth_label")
        self.cwDefaultBandwidth_Label.configure(
            state="disabled", style="Heading1b.TLabel", text='CW')
        self.tooltip9 = Tooltip(self.cwDefaultBandwidth_Label)
        self.tooltip9.configure(
            padx=8,
            relief="raised",
            text='Sets the default bandwidth for CW on the SDR when you hit the Reset button',
            wraplength=300)
        self.cwDefaultBandwidth_Label.pack(padx=10, side="left")
        self.cwDefault_Spinbox = ttk.Spinbox(
            self.cwBandwidth_Frame, name="cwdefault_spinbox")
        self.cwDefault_VAR = tk.StringVar(value='500')
        self.cwDefault_Spinbox.configure(
            font="{Arial} 24 {}",
            from_=200,
            increment=50,
            justify="right",
            style="Custom.TSpinbox",
            textvariable=self.cwDefault_VAR,
            to=500,
            width=6)
        _text_ = '500'
        self.cwDefault_Spinbox.delete("0", "end")
        self.cwDefault_Spinbox.insert("0", _text_)
        self.cwDefault_Spinbox.pack(side="top")
        self.cwDefault_Spinbox.configure(command=self.cwDefault_CB)
        self.cwBandwidth_Frame.pack(
            anchor="center", padx=40, pady="0 10", side="left")
        self.ssbBandwidthFrame = ttk.Frame(
            self.defaultBandwidth_Frame,
            name="ssbbandwidthframe")
        self.ssbBandwidthFrame.configure(
            height=200, style="Normal.TFrame", width=200)
        self.ssb_DefaultBandwidth_Label = ttk.Label(
            self.ssbBandwidthFrame, name="ssb_defaultbandwidth_label")
        self.ssb_DefaultBandwidth_Label.configure(
            state="disabled", style="Heading1b.TLabel", text='SSB')
        self.tooltip10 = Tooltip(self.ssb_DefaultBandwidth_Label)
        self.tooltip10.configure(
            padx=8,
            relief="raised",
            text='Sets the default bandwidth for SSB on the SDR when you hit the Reset button',
            wraplength=300)
        self.ssb_DefaultBandwidth_Label.pack(padx=10, side="left")
        self.ssbDefault_Spinbox = ttk.Spinbox(
            self.ssbBandwidthFrame, name="ssbdefault_spinbox")
        self.ssbDefault_VAR = tk.StringVar(value='2600')
        self.ssbDefault_Spinbox.configure(
            font="{Arial} 24 {}",
            from_=2000,
            increment=100,
            justify="right",
            style="Custom.TSpinbox",
            textvariable=self.ssbDefault_VAR,
            to=3200,
            width=6)
        _text_ = '2600'
        self.ssbDefault_Spinbox.delete("0", "end")
        self.ssbDefault_Spinbox.insert("0", _text_)
        self.ssbDefault_Spinbox.pack(side="top")
        self.ssbDefault_Spinbox.configure(command=self.ssbDefault_CB)
        self.ssbBandwidthFrame.pack(anchor="center", pady="0 20", side="left")
        self.defaultBandwidth_Frame.grid(
            column=0, columnspan=2, padx=0, pady=10, row=4, sticky="ew")
        frame1.pack(
            anchor="center",
            expand=True,
            fill="both",
            padx=10,
            pady=10,
            side="top")
        self.closingFrame = ttk.Frame(self, name="closingframe")
        self.closingFrame.configure(
            height=50, style="Normal.TFrame", width=200)
        self.apply_Button = ttk.Button(self.closingFrame, name="apply_button")
        self.apply_Button.configure(
            style="Button2b.TButton",
            takefocus=True,
            text='Apply')
        self.apply_Button_Tooltip = Tooltip(self.apply_Button)
        self.apply_Button_Tooltip.configure(
            padx=8,
            relief="raised",
            text='Updates the setting and closes the window.',
            wraplength=300)
        self.apply_Button.pack(anchor="center", padx=10, side="left")
        self.apply_Button.configure(command=self.apply_CB)
        self.cancel_Buttom = ttk.Button(
            self.closingFrame, name="cancel_buttom")
        self.cancel_Buttom.configure(
            style="Button2b.TButton",
            takefocus=True,
            text='Cancel')
        self.cancel_Button_Tooltip = Tooltip(self.cancel_Buttom)
        self.cancel_Button_Tooltip.configure(
            padx=8,
            relief="raised",
            text='Exit without writing any changes.',
            wraplength=300)
        self.cancel_Buttom.pack(anchor="center", padx=10, side="left")
        self.cancel_Buttom.configure(command=self.cancel_CB)
        self.closingFrame.pack(
            anchor="center",
            expand=False,
            pady="20 10",
            side="top")
        self.configure(
            cursor="arrow",
            style="Heading2.TLabelframe",
            text='SDR Settings ')
        # Layout for 'settingsSDR_Labelframe' skipped in custom widget
        # template.

    def selectSDR_On_CB(self):
        pass

    def selectSDR_Off_CB(self):
        pass

    def selectSDRPlusPlus_CB(self):
        pass

    def autostartSDR_CB(self):
        pass

    def cwDefault_CB(self):
        pass

    def ssbDefault_CB(self):
        pass

    def apply_CB(self):
        pass

    def cancel_CB(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    widget = settingsSDRUI(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()

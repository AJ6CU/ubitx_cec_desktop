#!/usr/bin/python3
"""
sdrDashboard

A small window that pops up when a sdr is connected

UI source file: sdrDashboard.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.hideableframe import HideableFrame
from pygubu.widgets.scrolledframe import ScrolledFrame
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
class sdrDashboardUI(ttk.Frame):
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

        self.liveTelemetry_Frame = ttk.Labelframe(
            self, name="livetelemetry_frame")
        self.liveTelemetry_Frame.configure(
            style="Normal.TLabelframe",
            text=' Live Telemetry Tracker Panel ')
        # First object created
        on_first_object_cb(self.liveTelemetry_Frame)

        frame7 = ttk.Frame(self.liveTelemetry_Frame)
        frame7.configure(height=200, style="Normal.TFrame", width=200)
        label1 = ttk.Label(frame7)
        label1.configure(
            style="Heading3b.TLabel",
            text='Active VFO Frequency:')
        label1.pack(padx="42 10", side="left")
        self.label_val_freq = ttk.Label(frame7, name="label_val_freq")
        self.label_val_freq.configure(
            style="Heading3b.TLabel",
            text='000.0000 MHz',
            width=13)
        self.label_val_freq.pack(side="left")
        label4 = ttk.Label(frame7)
        label4.configure(style="Heading3b.TLabel", text='Mode:')
        label4.pack(padx="40 10", side="left")
        self.label_val_mode = ttk.Label(frame7, name="label_val_mode")
        self.label_val_mode.configure(style="Heading3b.TLabel", text='UNKNOWN')
        self.label_val_mode.pack(side="left")
        frame7.pack(anchor="center", expand=True, fill="x", pady=5, side="top")
        frame5 = ttk.Frame(self.liveTelemetry_Frame)
        frame5.configure(height=200, style="Normal.TFrame", width=200)
        lbl_volume_txt = ttk.Label(frame5)
        lbl_volume_txt.configure(
            style="Heading3b.TLabel",
            text='Audio Volume (0-100):')
        self.tooltip1 = Tooltip(lbl_volume_txt)
        self.tooltip1.configure(
            padx=8,
            relief="raised",
            text='Controls system volume',
            wraplength=300)
        lbl_volume_txt.pack(padx="50 0", side="left")
        self.volume_scale = ttk.Scale(frame5, name="volume_scale")
        self.volume_scale.configure(
            from_=0,
            length=150,
            orient="horizontal",
            takefocus=False,
            to=100)
        self.volume_scale.pack(ipady=5, padx=10, side="left")
        self.volume_scale.bind(
            "<B1-Motion>",
            self.action_on_volume_slider_move,
            add="+")
        self.volume_scale.bind(
            "<ButtonRelease-1>",
            self.action_on_volume_slider_move,
            add="+")
        self.label_volume_val = ttk.Label(frame5, name="label_volume_val")
        self.label_volume_val.configure(
            font="TkFixedFont",
            style="Heading3b.TLabel",
            text='50%',
            width=6)
        self.label_volume_val.pack(side="left")
        self.button_mute_toggle = ttk.Button(frame5, name="button_mute_toggle")
        self.button_mute_toggle.configure(
            style="Button1bRaised.TButton",
            takefocus=False,
            text='🔊 Mute Audio',
            width=15)
        self.tooltip3 = Tooltip(self.button_mute_toggle)
        self.tooltip3.configure(
            padx=8,
            relief="raised",
            text='Mute/Unmute System Volume',
            wraplength=300)
        self.button_mute_toggle.pack(ipady=5, padx=10, side="left")
        self.button_mute_toggle.configure(command=self.action_toggle_mute)
        frame5.pack(anchor="center", expand=True, fill="x", pady=5, side="top")
        self.liveTelemetry_Frame.pack(anchor="n", side="top")
        self.sdrCommands_ScrolledFrame = ScrolledFrame(
            self, scrolltype="both", name="sdrcommands_scrolledframe")
        self.sdrCommands_ScrolledFrame.innerframe.configure(
            style="Normal.TFrame")
        self.sdrCommands_ScrolledFrame.configure(usemousewheel=False)
        self.band_all_Frame = ttk.Frame(
            self.sdrCommands_ScrolledFrame.innerframe,
            name="band_all_frame")
        self.band_all_Frame.configure(style="Normal.TFrame")
        self.bands_Frame = ttk.Frame(self.band_all_Frame, name="bands_frame")
        self.bands_Frame.configure(height=200, style="Normal.TFrame")
        self.bandsToggle_Button = ttk.Button(
            self.bands_Frame, name="bandstoggle_button")
        self.bandsToggle_Button.configure(
            state="normal", style="Custom.Toolbutton", text='Bands')
        self.bandsToggle_Button.pack(expand=False, side="left")
        self.bandsToggle_Button.configure(command=self.toggleBands_CB)
        self.bands_Frame.grid(column=0, row=0, sticky="nw")
        self.bandsAccordion_Frame = HideableFrame(
            self.band_all_Frame, name="bandsaccordion_frame")
        self.bandsAccordion_Frame.configure(style="Normal.TFrame")
        self.quickHamBandSelect_Labelframe = ttk.Labelframe(
            self.bandsAccordion_Frame, name="quickhambandselect_labelframe")
        self.quickHamBandSelect_Labelframe.configure(
            style="Normal.TLabelframe", text=' Ham Radio Bands')
        self.Band160m = ttk.Button(
            self.quickHamBandSelect_Labelframe,
            name="band160m")
        self.Band160m.configure(style="Button1bRaised.TButton", text='160M')
        self.Band160m.grid(column=0, ipady=5, padx=10, pady=10, row=0)
        def Band160m_cmd_(): self.action_quick_band("Band160m")

        self.Band160m.configure(command=Band160m_cmd_)
        self.Band80m = ttk.Button(
            self.quickHamBandSelect_Labelframe,
            name="band80m")
        self.Band80m.configure(style="Button1bRaised.TButton", text='80M')
        self.Band80m.grid(column=1, ipady=5, padx=10, pady=10, row=0)
        def Band80m_cmd_(): self.action_quick_band("Band80m")

        self.Band80m.configure(command=Band80m_cmd_)
        self.Band40m = ttk.Button(
            self.quickHamBandSelect_Labelframe,
            name="band40m")
        self.Band40m.configure(style="Button1bRaised.TButton", text='40M')
        self.Band40m.grid(column=2, ipady=5, padx=10, pady=10, row=0)
        def Band40m_cmd_(): self.action_quick_band("Band40m")

        self.Band40m.configure(command=Band40m_cmd_)
        self.Band30m = ttk.Button(
            self.quickHamBandSelect_Labelframe,
            name="band30m")
        self.Band30m.configure(style="Button1bRaised.TButton", text='30M')
        self.Band30m.grid(column=0, ipady=5, padx=10, pady=10, row=1)
        def Band30m_cmd_(): self.action_quick_band("Band30m")

        self.Band30m.configure(command=Band30m_cmd_)
        self.Band20m = ttk.Button(
            self.quickHamBandSelect_Labelframe,
            name="band20m")
        self.Band20m.configure(style="Button1bRaised.TButton", text='20M')
        self.Band20m.grid(column=1, ipady=5, padx=10, pady=10, row=1)
        def Band20m_cmd_(): self.action_quick_band("Band20m")

        self.Band20m.configure(command=Band20m_cmd_)
        self.Band17m = ttk.Button(
            self.quickHamBandSelect_Labelframe,
            name="band17m")
        self.Band17m.configure(style="Button1bRaised.TButton", text='17M')
        self.Band17m.grid(column=2, ipady=5, padx=10, pady=10, row=1)
        def Band17m_cmd_(): self.action_quick_band("Band17m")

        self.Band17m.configure(command=Band17m_cmd_)
        self.Band15m = ttk.Button(
            self.quickHamBandSelect_Labelframe,
            name="band15m")
        self.Band15m.configure(style="Button1bRaised.TButton", text='15M')
        self.Band15m.grid(column=0, ipady=5, padx=10, pady=10, row=2)
        def Band15m_cmd_(): self.action_quick_band("Band15m")

        self.Band15m.configure(command=Band15m_cmd_)
        self.Band12m = ttk.Button(
            self.quickHamBandSelect_Labelframe,
            name="band12m")
        self.Band12m.configure(style="Button1bRaised.TButton", text='12M')
        self.Band12m.grid(column=1, ipady=5, padx=10, pady=10, row=2)
        def Band12m_cmd_(): self.action_quick_band("Band12m")

        self.Band12m.configure(command=Band12m_cmd_)
        self.Band10m = ttk.Button(
            self.quickHamBandSelect_Labelframe,
            name="band10m")
        self.Band10m.configure(style="Button1bRaised.TButton", text='10m')
        self.Band10m.grid(column=2, ipady=5, padx=10, pady=10, row=2)
        def Band10m_cmd_(): self.action_quick_band("Band10m")

        self.Band10m.configure(command=Band10m_cmd_)
        self.tooltip2 = Tooltip(self.quickHamBandSelect_Labelframe)
        self.tooltip2.configure(
            padx=8,
            relief="raised",
            text='Shortcut buttons to common HAM bands',
            wraplength=300)
        self.quickHamBandSelect_Labelframe.pack(
            anchor="w", padx=10, side="top")
        self.quickHamBandSelect_Labelframe.grid_anchor("w")
        self.modeChange_Labelframe = ttk.Labelframe(
            self.bandsAccordion_Frame, name="modechange_labelframe")
        self.modeChange_Labelframe.configure(
            style="Normal.TLabelframe", text='Mode')
        self.modeLSB_Button = ttk.Button(
            self.modeChange_Labelframe,
            name="modelsb_button")
        self.modeLSB_Button.configure(
            style="Button1bRaised.TButton", text='LSB')
        self.modeLSB_Button.grid(column=0, ipady=5, padx=10, pady=10, row=0)
        def modeLSB_Button_cmd_(): self.action_quick_mode("modeLSB_Button")

        self.modeLSB_Button.configure(command=modeLSB_Button_cmd_)
        self.modeUSB_Button = ttk.Button(
            self.modeChange_Labelframe,
            name="modeusb_button")
        self.modeUSB_Button.configure(
            style="Button1bRaised.TButton", text='USB')
        self.modeUSB_Button.grid(column=1, ipady=5, padx=10, pady=10, row=0)
        def modeUSB_Button_cmd_(): self.action_quick_mode("modeUSB_Button")

        self.modeUSB_Button.configure(command=modeUSB_Button_cmd_)
        self.modeCWL_Button = ttk.Button(
            self.modeChange_Labelframe,
            name="modecwl_button")
        self.modeCWL_Button.configure(
            style="Button1bRaised.TButton", text='CWL')
        self.modeCWL_Button.grid(column=2, ipady=5, padx=10, pady=10, row=0)
        def modeCWL_Button_cmd_(): self.action_quick_mode("modeCWL_Button")

        self.modeCWL_Button.configure(command=modeCWL_Button_cmd_)
        self.modeCWU_Button = ttk.Button(
            self.modeChange_Labelframe,
            name="modecwu_button")
        self.modeCWU_Button.configure(
            style="Button1bRaised.TButton", text='CWU')
        self.modeCWU_Button.grid(column=3, ipady=5, padx=10, pady=10, row=0)
        def modeCWU_Button_cmd_(): self.action_quick_mode("modeCWU_Button")

        self.modeCWU_Button.configure(command=modeCWU_Button_cmd_)
        self.tooltip4 = Tooltip(self.modeChange_Labelframe)
        self.tooltip4.configure(
            padx=8,
            relief="raised",
            text='Selects the mode for RX.CWL and CWU are mapped to CW on SDR++. ',
            wraplength=300)
        self.modeChange_Labelframe.pack(anchor="w", padx=10, pady="10 0")
        self.modeChange_Labelframe.grid_anchor("w")
        self.bandwidthManagement_Labelframe = ttk.Labelframe(
            self.bandsAccordion_Frame, name="bandwidthmanagement_labelframe")
        self.bandwidthManagement_Labelframe.configure(
            style="Normal.TLabelframe", text='IF Filter')
        frame1 = ttk.Frame(self.bandwidthManagement_Labelframe)
        frame1.configure(height=200, style="Normal.TFrame", width=200)
        self.widenFilter_Button = ttk.Button(frame1, name="widenfilter_button")
        self.widenFilter_Button.configure(
            style="Button1bRaised.TButton", text='Widen')
        self.tooltip5 = Tooltip(self.widenFilter_Button)
        self.tooltip5.configure(
            padx=8,
            relief="raised",
            text='Widens the bandwidth filter. 50 for CW and 500 for LSB/USB.',
            wraplength=300)
        self.widenFilter_Button.pack(ipady=5, padx=10, pady=10, side="left")
        self.widenFilter_Button.configure(command=self.action_filter_widen)
        self.narrowFilter_Button = ttk.Button(
            frame1, name="narrowfilter_button")
        self.narrowFilter_Button.configure(
            style="Button1bRaised.TButton", text='Narrow')
        self.tooltip6 = Tooltip(self.narrowFilter_Button)
        self.tooltip6.configure(
            padx=8,
            relief="raised",
            text='Narrows the bandwidth filter. 50 for CW and 500 for LSB/USB.',
            wraplength=300)
        self.narrowFilter_Button.pack(ipady=5, padx=10, pady=10, side="left")
        self.narrowFilter_Button.configure(command=self.action_filter_narrow)
        self.resetFilter_Button = ttk.Button(frame1, name="resetfilter_button")
        self.resetFilter_Button.configure(
            style="Button1bRaised.TButton", text='Reset')
        self.tooltip7 = Tooltip(self.resetFilter_Button)
        self.tooltip7.configure(
            padx=8,
            relief="raised",
            text='Resets filter to default for the mode. Can be tuned in the SDR Settings control panel.',
            wraplength=300)
        self.resetFilter_Button.pack(ipady=5, padx=10, pady=10, side="left")
        self.resetFilter_Button.configure(command=self.action_filter_reset)
        self.filterWidth_Label = ttk.Label(frame1, name="filterwidth_label")
        self.filterWidth_Label.configure(
            style="Heading3b.TLabel", text='Filter:')
        self.tooltip8 = Tooltip(self.filterWidth_Label)
        self.tooltip8.configure(
            padx=8,
            relief="raised",
            text='The current filter width reported by sdr++.',
            wraplength=300)
        self.filterWidth_Label.pack(padx=20, pady=5, side="left")
        self.currentFilterWidth_Label = ttk.Label(
            frame1, name="currentfilterwidth_label")
        self.currentFilterWidth_Label.configure(
            style="Heading3b.TLabel", width=5)
        self.currentFilterWidth_Label.pack(side="left")
        self.filterWidthHZ_Label = ttk.Label(
            frame1, name="filterwidthhz_label")
        self.filterWidthHZ_Label.configure(style="Heading3b.TLabel", text='HZ')
        self.filterWidthHZ_Label.pack(padx=5, pady=5, side="left")
        frame1.grid(column=0, row=0, sticky="ew")
        self.bandwidthManagement_Labelframe.pack(
            anchor="w", padx=10, pady="10 0")
        self.bandwidthManagement_Labelframe.grid_anchor("w")
        self.bandsAccordion_Frame.grid(column=0, row=1)
        self.band_all_Frame.pack(
            anchor="n",
            expand=True,
            fill="both",
            padx=5,
            pady=5,
            side="top")
        self.band_all_Frame.grid_anchor("nw")
        self.channels_all = ttk.Frame(
            self.sdrCommands_ScrolledFrame.innerframe,
            name="channels_all")
        self.channels_all.configure(style="Normal.TFrame")
        self.channels_Frame = ttk.Frame(
            self.channels_all, name="channels_frame")
        self.channels_Frame.configure(height=200, style="Normal.TFrame")
        self.channelsToggle_Button = ttk.Button(
            self.channels_Frame, name="channelstoggle_button")
        self.channelsToggle_Button.configure(
            state="normal", style="Custom.Toolbutton", text='Channels')
        self.channelsToggle_Button.pack(expand=True, fill="x", side="left")
        self.channelsToggle_Button.configure(command=self.toggleChannels_CB)
        self.channels_Frame.grid(column=0, row=0, sticky="nw")
        self.channelsAccordion_Frame = HideableFrame(
            self.channels_all, name="channelsaccordion_frame")
        self.channelsAccordion_Frame.configure(style="Normal.TFrame")
        frame4 = ttk.Frame(self.channelsAccordion_Frame)
        frame4.configure(height=200, style="Normal.TFrame", width=200)
        grid_wrapper = ttk.Frame(frame4)
        grid_wrapper.configure(style="Normal.TFrame")
        self.treeChannels = ttk.Treeview(grid_wrapper, name="treechannels")
        self.treeChannels.configure(
            height=10, selectmode="browse", show="headings")
        self.treeChannels.pack(expand=True, fill="both", side="left")
        self.treeChannels.bind(
            "<<TreeviewSelect>>",
            self.action_on_channel_row_click,
            add="+")
        self.treeScrollbar = ttk.Scrollbar(grid_wrapper, name="treescrollbar")
        self.treeScrollbar.configure(orient="vertical")
        self.treeScrollbar.pack(fill="y", side="right")
        grid_wrapper.pack(side="left")
        self.channelSearch_Labelframe = ttk.Labelframe(
            frame4, name="channelsearch_labelframe")
        self.channelSearch_Labelframe.configure(
            style="Normal.TLabelframe", text='Search')
        self.channelLookup_Entry = ttk.Entry(
            self.channelSearch_Labelframe,
            name="channellookup_entry")
        self.channelLookup_Entry.configure(
            style="Entry3b.TEntry", takefocus=False)
        self.channelLookup_Entry.grid(
            column=0, ipady=5, padx=5, pady=5, row=0, sticky="ew")
        self.channelLookup_Entry.bind(
            "<KeyRelease>", self.action_filter_search_grid, add="+")
        self.tooltip9 = Tooltip(self.channelSearch_Labelframe)
        self.tooltip9.configure(
            padx=8,
            relief="raised",
            text='Type in a few characters to find a channel in the current Bank.',
            wraplength=300)
        self.channelSearch_Labelframe.pack(anchor="center", side="right")
        frame4.pack()
        self.channelEdit_Labelframe = ttk.Labelframe(
            self.channelsAccordion_Frame, name="channeledit_labelframe")
        self.channelEdit_Labelframe.configure(
            height=200,
            style="Normal.TLabelframe",
            text='Channel Edit',
            width=200)
        self.addChanneltoBank_Button = ttk.Button(
            self.channelEdit_Labelframe, name="addchanneltobank_button")
        self.addChanneltoBank_Button.configure(
            style="Button1bRaised.TButton",
            takefocus=False,
            text='Copy to\nTarget\nBank')
        self.tooltip10 = Tooltip(self.addChanneltoBank_Button)
        self.tooltip10.configure(
            padx=8,
            relief="raised",
            text='Copies the selected Channel in list above to the Target Bank.',
            wraplength=300)
        self.addChanneltoBank_Button.grid(
            column=0, ipady=5, padx=10, pady=10, row=0)
        self.addChanneltoBank_Button.configure(
            command=self.action_copy_row_to_target_bank)
        self.deleteChannel_Button = ttk.Button(
            self.channelEdit_Labelframe, name="deletechannel_button")
        self.deleteChannel_Button.configure(
            style="Button1bRaised.TButton",
            takefocus=False,
            text='Erase\nChannel\nin Source\nBank')
        self.tooltip11 = Tooltip(self.deleteChannel_Button)
        self.tooltip11.configure(
            padx=8,
            relief="raised",
            text='Erases the currently selected channel in the list above. Only erases in the selected Source Bank.',
            wraplength=300)
        self.deleteChannel_Button.grid(
            column=0, ipady=5, padx=10, pady=10, row=1)
        self.deleteChannel_Button.configure(command=self.action_del_ch)
        self.newChannelFromVFO_Labelframe = ttk.Labelframe(
            self.channelEdit_Labelframe, name="newchannelfromvfo_labelframe")
        self.newChannelFromVFO_Labelframe.configure(
            height=200,
            style="Normal.TLabelframe",
            text='Save VFO to Channel and Target Bank',
            width=200)
        self.newVFOHeader_Frame = ttk.Frame(
            self.newChannelFromVFO_Labelframe,
            name="newvfoheader_frame")
        self.newVFOHeader_Frame.configure(
            height=200, style="Normal.TFrame", width=200)
        self.channelName_Label = ttk.Label(
            self.newVFOHeader_Frame, name="channelname_label")
        self.channelName_Label.configure(
            style="Heading3b.TLabel", text='Label:')
        self.tooltip12 = Tooltip(self.channelName_Label)
        self.tooltip12.configure(
            padx=8,
            relief="raised",
            text='Enter a short name for the channel being created based on the current VFO',
            wraplength=300)
        self.channelName_Label.grid(
            column=0, padx=10, pady=10, row=0, sticky="e")
        self.newChannel_Entry = ttk.Entry(
            self.newVFOHeader_Frame, name="newchannel_entry")
        self.newChannel_Entry.configure(
            style="Entry3b.TEntry", takefocus=False, width=10)
        self.newChannel_Entry.grid(
            column=1, ipady=5, pady=10, row=0, sticky="w")
        self.channelStation_Label = ttk.Label(
            self.newVFOHeader_Frame, name="channelstation_label")
        self.channelStation_Label.configure(
            style="Heading3b.TLabel", text='Desccription:')
        self.tooltip25 = Tooltip(self.channelStation_Label)
        self.tooltip25.configure(
            padx=8,
            relief="raised",
            text='Enter a longer more description name for the channel.',
            wraplength=300)
        self.channelStation_Label.grid(
            column=0, padx=10, pady=10, row=1, sticky="e")
        self.newStationDescription_Entry = ttk.Entry(
            self.newVFOHeader_Frame, name="newstationdescription_entry")
        self.newStationDescription_Entry.configure(
            style="Entry3b.TEntry", takefocus=False, width=15)
        self.newStationDescription_Entry.grid(
            column=1, ipady=5, padx="0 15", pady=10, row=1, sticky="w")
        self.newVFOHeader_Frame.pack()
        self.addNewChannel_Button = ttk.Button(
            self.newChannelFromVFO_Labelframe,
            name="addnewchannel_button")
        self.addNewChannel_Button.configure(
            style="Button1bRaised.TButton",
            takefocus=False,
            text='Save to\nSource\nBank')
        self.tooltip14 = Tooltip(self.addNewChannel_Button)
        self.tooltip14.configure(
            padx=8,
            relief="raised",
            text='Saves the current VFO and Mode to the Source Bank.',
            wraplength=300)
        self.addNewChannel_Button.pack(ipady=5, pady=10)
        self.addNewChannel_Button.configure(
            command=self.action_capture_live_vfo_to_channel)
        self.newChannelFromVFO_Labelframe.grid(
            column=1, padx=40, pady=10, row=0, rowspan=2, sticky="ns")
        self.channelEdit_Labelframe.pack(anchor="w", padx="20 10", side="top")
        self.bankRouting_Labelframe = ttk.Labelframe(
            self.channelsAccordion_Frame, name="bankrouting_labelframe")
        self.bankRouting_Labelframe.configure(
            style="Normal.TLabelframe",
            text='Channel Bank Management')
        self.sourceTargetLabelframe = ttk.Labelframe(
            self.bankRouting_Labelframe, name="sourcetargetlabelframe")
        self.sourceTargetLabelframe.configure(
            height=200,
            style="Normal.TLabelframe",
            text='Select Banks',
            width=200)
        lbl_src_bank = ttk.Label(self.sourceTargetLabelframe)
        lbl_src_bank.configure(style="Heading3b.TLabel", text='Source:')
        self.tooltip15 = Tooltip(lbl_src_bank)
        self.tooltip15.configure(
            padx=8,
            relief="raised",
            text='Selection of the Source bank. ',
            wraplength=300)
        lbl_src_bank.grid(column=0, row=1)
        self.sourceBank_VAR = tk.StringVar()
        __values = []
        self.sourceBank = ttk.OptionMenu(
            self.sourceTargetLabelframe,
            self.sourceBank_VAR,
            None,
            *__values,
            command=self.sourceBank_CB)
        self.sourceBank.grid(column=1, pady=10, row=1, sticky="ew")
        lbl_tgt_bank = ttk.Label(self.sourceTargetLabelframe)
        lbl_tgt_bank.configure(style="Heading3b.TLabel", text='Target:')
        self.tooltip16 = Tooltip(lbl_tgt_bank)
        self.tooltip16.configure(
            padx=8,
            relief="raised",
            text='Selection of the Target bank. ',
            wraplength=300)
        lbl_tgt_bank.grid(column=0, row=0)
        self.targetBank_VAR = tk.StringVar()
        __values = []
        self.targetBank = ttk.OptionMenu(
            self.sourceTargetLabelframe,
            self.targetBank_VAR,
            None,
            *__values,
            command=self.targetBank_CB)
        self.targetBank.grid(column=1, pady=10, row=0, sticky="ew")
        self.sourceTargetLabelframe.grid(column=0, row=0)
        self.channelControl_Frame = ttk.Frame(
            self.bankRouting_Labelframe,
            name="channelcontrol_frame")
        self.channelControl_Frame.configure(
            height=200, style="Normal.TFrame", width=200)
        self.newChannelBank_Button = ttk.Button(
            self.channelControl_Frame, name="newchannelbank_button")
        self.newChannelBank_Button.configure(
            style="Button1bRaised.TButton", takefocus=False, text='New')
        self.tooltip17 = Tooltip(self.newChannelBank_Button)
        self.tooltip17.configure(
            padx=8,
            relief="raised",
            text='Creates a new bank by name you enter in the entry field to the right.',
            wraplength=300)
        self.newChannelBank_Button.grid(
            column=0, ipady=5, padx=15, pady=10, row=0)
        self.newChannelBank_Button.configure(
            command=self.action_create_brand_new_bank)
        self.newBankName_Entry = ttk.Entry(
            self.channelControl_Frame, name="newbankname_entry")
        self.newBankName_Entry.configure(
            style="Entry3b.TEntry", takefocus=False, width=11)
        self.newBankName_Entry.grid(
            column=2, ipady=5, pady=10, row=0, sticky="w")
        self.bankCloneButton = ttk.Button(
            self.channelControl_Frame, name="bankclonebutton")
        self.bankCloneButton.configure(
            style="Button1bRaised.TButton",
            takefocus=False,
            text='Clone')
        self.tooltip18 = Tooltip(self.bankCloneButton)
        self.tooltip18.configure(
            padx=8,
            relief="raised",
            text='Adds the channels in the Source Bank to the Target Bank. Existing channels in Target Bank are preserved.',
            wraplength=300)
        self.bankCloneButton.grid(column=0, ipady=5, padx=15, pady=10, row=2)
        self.bankCloneButton.configure(
            command=self.action_bulk_clone_source_to_target)
        self.bankDelete_Button = ttk.Button(
            self.channelControl_Frame, name="bankdelete_button")
        self.bankDelete_Button.configure(
            style="Button1bRaised.TButton",
            takefocus=False,
            text='Delete\nSource\nBank')
        self.tooltip19 = Tooltip(self.bankDelete_Button)
        self.tooltip19.configure(
            padx=8,
            relief="raised",
            text='Deletes the bank currently selected in the Source Bank selector.',
            wraplength=300)
        self.bankDelete_Button.grid(column=0, ipady=5, padx=10, pady=10, row=3)
        self.bankDelete_Button.configure(
            command=self.action_delete_source_bank_profile)
        self.channelControl_Frame.grid(
            column=1,
            columnspan=3,
            padx=40,
            pady=10,
            row=0,
            sticky="ew")
        self.bankRouting_Labelframe.pack(anchor="w", padx=10, pady="20 10")
        self.channelsAccordion_Frame.grid(row=1)
        self.channels_all.pack(
            anchor="n",
            expand=True,
            fill="both",
            padx=5,
            pady=5,
            side="top")
        self.channels_all.grid_anchor("nw")
        self.scan_all = ttk.Frame(
            self.sdrCommands_ScrolledFrame.innerframe,
            name="scan_all")
        self.scan_all.configure(style="Normal.TFrame")
        self.scan_Frame = ttk.Frame(self.scan_all, name="scan_frame")
        self.scan_Frame.configure(style="Normal.TFrame")
        self.scanToggle_Button = ttk.Button(
            self.scan_Frame, name="scantoggle_button")
        self.scanToggle_Button.configure(
            state="normal", style="Custom.Toolbutton", text='Scan')
        self.scanToggle_Button.pack(expand=False, side="left")
        self.scanToggle_Button.configure(command=self.toggleScan_CB)
        self.scan_Frame.grid(column=0, row=0, sticky="nw")
        self.scanAccordion_Frame = HideableFrame(
            self.scan_all, name="scanaccordion_frame")
        self.scanAccordion_Frame.configure(style="Normal.TFrame")
        self.scanParameters_Labelframe = ttk.Labelframe(
            self.scanAccordion_Frame, name="scanparameters_labelframe")
        self.scanParameters_Labelframe.configure(
            style="Normal.TLabelframe", text='Settings')
        lbl_delay = ttk.Label(self.scanParameters_Labelframe)
        lbl_delay.configure(
            justify="right",
            style="Heading3b.TLabel",
            text='Scan Delay Period:\n(seconds)\n')
        self.tooltip20 = Tooltip(lbl_delay)
        self.tooltip20.configure(
            padx=8,
            relief="raised",
            text='Specify the time that the radio will stay on a channel during a scan. This defaults to a saved value in the Channels Setting screen. Changing it here is for only this run and does not change the default.',
            wraplength=300)
        lbl_delay.grid(column=0, padx=5, pady=10, row=0)
        self.scanTime_Entry = ttk.Entry(
            self.scanParameters_Labelframe,
            name="scantime_entry")
        self.scanTime_Entry.configure(
            style="Entry3b.TEntry", takefocus=False, width=6)
        self.scanTime_Entry.grid(
            column=1,
            ipady=5,
            padx=10,
            pady=10,
            row=0,
            sticky="w")
        self.scanBankSelect_Label = ttk.Label(
            self.scanParameters_Labelframe,
            name="scanbankselect_label")
        self.scanBankSelect_Label.configure(
            justify="right",
            style="Heading3b.TLabel",
            text='Bank to Scan:')
        self.tooltip21 = Tooltip(self.scanBankSelect_Label)
        self.tooltip21.configure(
            padx=8,
            relief="raised",
            text='Select the bank to scan.',
            wraplength=300)
        self.scanBankSelect_Label.grid(
            column=0, padx=5, pady=2, row=1, sticky="e")
        self.scanBank_VAR = tk.StringVar()
        __values = []
        self.scanBank = ttk.OptionMenu(
            self.scanParameters_Labelframe,
            self.scanBank_VAR,
            None,
            *__values,
            command=self.scanBank_CB)
        self.scanBank.grid(column=1, pady=10, row=1, sticky="ew")
        self.scanParameters_Labelframe.pack(padx=10)
        self.scanControl_Labelframe = ttk.Labelframe(
            self.scanAccordion_Frame, name="scancontrol_labelframe")
        self.scanControl_Labelframe.configure(
            style="Normal.TLabelframe", text='Control')
        self.scanStart_Button = ttk.Button(
            self.scanControl_Labelframe,
            name="scanstart_button")
        self.scanStart_Button.configure(
            style="Button1bRaised.TButton",
            takefocus=False,
            text='▶ Start Scan ')
        self.tooltip22 = Tooltip(self.scanStart_Button)
        self.tooltip22.configure(
            padx=8,
            relief="raised",
            text='Starts the channel scan using the channels in the Se;ector above.',
            wraplength=300)
        self.scanStart_Button.grid(
            column=0, ipadx=5, ipady=5, padx=10, pady=10, row=0)
        self.scanStart_Button.configure(command=self.action_start_scan)
        self.scanStop_Button = ttk.Button(
            self.scanControl_Labelframe,
            name="scanstop_button")
        self.scanStop_Button.configure(
            style="Button1bRaised.TButton",
            takefocus=False,
            text='⏹ Stop Scan')
        self.tooltip23 = Tooltip(self.scanStop_Button)
        self.tooltip23.configure(
            padx=8,
            relief="raised",
            text='Stops the scan. Stays on current channel.',
            wraplength=300)
        self.scanStop_Button.grid(
            column=1,
            ipadx=5,
            ipady=5,
            padx=10,
            pady=10,
            row=0)
        self.scanStop_Button.configure(command=self.stop_scan)
        self.scanControl_Labelframe.pack(anchor="w", padx=10, pady=10)
        self.scanAccordion_Frame.grid(row=1)
        self.scan_all.pack(
            anchor="n",
            expand=True,
            fill="both",
            padx=5,
            pady=5,
            side="top")
        self.scan_all.grid_anchor("nw")
        self.sdrCommands_ScrolledFrame.pack(
            anchor="n", expand=True, fill="both", side="top")
        self.connectionStatus_Frame = ttk.Labelframe(
            self, name="connectionstatus_frame")
        self.connectionStatus_Frame.configure(
            style="Normal.TLabelframe", text='Status')
        self.ipAddress_Label = ttk.Label(
            self.connectionStatus_Frame,
            name="ipaddress_label")
        self.ipAddress_Label.configure(
            style="Heading3b.TLabel",
            text='SDR IP Address:')
        self.ipAddress_Label.grid(
            column=0, padx="40 10", pady=5, row=0, sticky="e")
        self.portLabel = ttk.Label(
            self.connectionStatus_Frame,
            name="portlabel")
        self.portLabel.configure(
            style="Heading3b.TLabel",
            text='TCP Socket Port:')
        self.portLabel.grid(column=2, padx="20 10", pady=5, row=0)
        self.sdrStatus_Label = ttk.Label(
            self.connectionStatus_Frame,
            name="sdrstatus_label")
        self.sdrStatus_Label.configure(
            style="Heading3b.TLabel", text='SDR Status:')
        self.sdrStatus_Label.grid(column=0, row=2, sticky="e")
        self.linkStatus_Label = ttk.Label(
            self.connectionStatus_Frame,
            name="linkstatus_label")
        self.linkStatus_Label.configure(
            style="Heading3bRed.TLabel",
            takefocus=False,
            text='Disconnected')
        self.linkStatus_Label.grid(column=1, row=2)
        self.reconnect_Button = ttk.Button(
            self.connectionStatus_Frame,
            name="reconnect_button")
        self.reconnect_Button.configure(
            style="Button1bRaised.TButton",
            takefocus=False,
            text='Reconnect')
        self.tooltip24 = Tooltip(self.reconnect_Button)
        self.tooltip24.configure(
            padx=8,
            relief="raised",
            text='If the SDR becomes disconnected. Try clicking this button to reconnect.',
            wraplength=300)
        self.reconnect_Button.grid(
            column=2,
            columnspan=2,
            ipadx=5,
            ipady=5,
            padx=10,
            pady=10,
            row=2)
        self.reconnect_Button.configure(command=self.action_connect)
        self.sdrIPAddress_Label = ttk.Label(
            self.connectionStatus_Frame,
            name="sdripaddress_label")
        self.sdrIPAddress_Label.configure(
            state="normal", style="Heading3b.TLabel", width=11)
        self.sdrIPAddress_Label.grid(column=1, row=0, sticky="w")
        self.sdrPortNumber_Label = ttk.Label(
            self.connectionStatus_Frame,
            name="sdrportnumber_label")
        self.sdrPortNumber_Label.configure(
            style="Heading3b.TLabel", text='8000', width=5)
        self.sdrPortNumber_Label.grid(column=3, row=0)
        self.connectionStatus_Frame.pack(anchor="s", side="bottom")
        self.connectionStatus_Frame.grid_anchor("s")
        self.configure(height=800, style="Normal.TFrame", width=600)
        # Layout for 'primaryFrame' skipped in custom widget template.

    def action_on_volume_slider_move(self, event=None):
        pass

    def action_toggle_mute(self):
        pass

    def toggleBands_CB(self):
        pass

    def action_quick_band(self, widget_id):
        pass

    def action_quick_mode(self, widget_id):
        pass

    def action_filter_widen(self):
        pass

    def action_filter_narrow(self):
        pass

    def action_filter_reset(self):
        pass

    def toggleChannels_CB(self):
        pass

    def action_on_channel_row_click(self, event=None):
        pass

    def action_filter_search_grid(self, event=None):
        pass

    def action_copy_row_to_target_bank(self):
        pass

    def action_del_ch(self):
        pass

    def action_capture_live_vfo_to_channel(self):
        pass

    def sourceBank_CB(self, option):
        pass

    def targetBank_CB(self, option):
        pass

    def action_create_brand_new_bank(self):
        pass

    def action_bulk_clone_source_to_target(self):
        pass

    def action_delete_source_bank_profile(self):
        pass

    def toggleScan_CB(self):
        pass

    def scanBank_CB(self, option):
        pass

    def action_start_scan(self):
        pass

    def stop_scan(self):
        pass

    def action_connect(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    widget = sdrDashboardUI(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()

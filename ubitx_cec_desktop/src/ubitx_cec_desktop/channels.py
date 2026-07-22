#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import channelsui as baseui
from tkinter import messagebox
from configuration import ConfigurationManager
import globalvars as gv
import EEPROM as EEPROM
from delayWarning import delayWarning

#
# Manual user code
#



class channels(baseui.channelsUI):
    channelList = []
    currentChannel = 0

    def __init__(self, master=None, mainWindow=None, refreshCallback=None, **kw):

        self.master = master                # save parameters for re-use later
        self.mainWindow = mainWindow
        self.refreshCallback = refreshCallback

        channels.channelList = []           #initialize class variables
        channels.currentChannel = 0

        self.channelSlotCount = 0           #initialize instance variables to process channels
        self.channelSlotSelection = None
        #
        #   This pops up a warning dialog that this operation could take several seconds
        #
        self.delayDialog=delayWarning()
        self.delayDialog.warningLabel_VAR.set("Loading Channels from EEPROM...\n\nThis could take several seconds...")

        self.popup = tk.Toplevel(self.master)           # Create a top level window to contain the channel window

        super().__init__(self.popup, **kw)
        #
        #   Catch closes that happen thru Window Manager
        #
        self.popup.protocol("WM_DELETE_WINDOW", self.close_Channel_CB)
        #
        #   Attach variables
        #
        gv.make_widget_variable(self, "scan_Select_Channel", self.scan_Select_Channel_Menubutton)
        gv.make_widget_variable(self, "Time_On_Freq", self.Time_On_Freq_Spinbox)
        gv.make_widget_variable(self, "bankName", self.bankNameEntry)
        #
        #   Channels could have been created using any frequency. Need to use
        #   the smallest preset to avoid frequency being truncated. So capture it,
        #   reset it and late we will reset it.
        #
        self.mainWindow.theVFO_Object.savePresetState()
        self.mainWindow.theRadio.Set_Tuning_Preset(1)

        #
        #   Since we display the frequency using the selected Delimiter, need
        #   to register interest in its value in case it changes while channel window
        #   is open.
        gv.config.register_observer("NUMBER DELIMITER", self.reformatChannelFreq)

        #
        #   Initialize scanning functions.
        #
        self.scanRunning = False
        self.scanTimer = None
        self.scanSetSelected = None
        self.scanIndex = None
        self.scanList = []

        #
        #   Each channel is actually created from another object (frequencyChannel). So
        #   We create a list of those channels so we can access them later either.
        #   Also need to capture the callback of the particular frequencyChannel so when
        #   the user selects, we can know which one to use. The callaback stores pointer
        #   in channels.currentChannel
        #

        for child in self.scrolledChannelFrame.innerframe.winfo_children():
            channels.channelList.append(child)
            child.assignChannelSelect_CB(self.channelSlot_CB)
            child.assignChannelNum(self.channelSlotCount)
            #
            # Set defaults
            #
            child.channel_Number_Default()
            child.Label_Default()
            child.Freq_Default()
            child.Mode_Default()
            child.Showlabel_Default()
            child.ScanSet_Default(gv.config.get_ScanSet_Settings(self.channelSlotCount))

            self.channelSlotCount += 1

        self.scan_Select_Channel_Default()
        self.scan_Station_Time_Default()

    #
    #   This routine is called after the object has been created and initialized. Some tweaking
    #   happens to the user interface as well as an attempt to place the popup in a reasonable
    #   place on the screen. Unfortunately, many window managers defeat this good intention and
    #   will place it in the center of the screen
    #

    def initChannelsUX(self):
        self.update_Current_Frequency(self.mainWindow.theVFO_Object.getFormattedPrimaryVFO())
        self.update_Current_Mode(self.mainWindow.mode_Button['text'])
        self.mainWindow.theRadio.Req_Channel_Freqs()
        self.mainWindow.theRadio.Req_Channel_Labels()
        self.mainWindow.theRadio.Req_Channel_Show_Labels()
        #
        #   Since we are about to display the channel window, we can get rid of the warning dialog
        #
        self.delayDialog.destroy()
#
        #
        #   This places the popup a little down and over from o,o. This special treatment is needed becase of the height of
        #   the channel window
        #
        self.popup.geometry(gv.POPUP_WINDOW_OFFSET)
        self.popup.title("Frequency Channels")

        self.popup.wait_visibility()  # required on Linux

        # self.popup.transient(self.mainWindow)

        self.pack(expand=tk.YES, fill=tk.BOTH)


    #
    #   Handles reformating the frequencies in the case someone changes the number delimiter
    #   while the Channels window is open.
    #
    def reformatChannelFreq(self, new_delimiter):
        if new_delimiter  == ",":
            prior_delimiter = "."
        else:
            prior_delimiter = ","

        for child in channels.channelList:
            child.channel_Freq_VAR.set(child.channel_Freq_VAR.get().replace(prior_delimiter,new_delimiter))

        self.current_VFO_Label['text'] = self.current_VFO_Label['text'].replace(prior_delimiter,new_delimiter)

    #
    #   The following are just external visible methods to set/change various values
    #

    def update_Current_Frequency(self, freq):
        self.current_VFO_Label['text'] = freq

    def update_Current_Mode(self, mode):
        self.current_Mode_Label['text'] = mode


    def scan_Select_Channel_Default(self):
        self.scan_Select_Channel_VAR.set("None")

    #
    #   Time hanging around each channel during a scan is controllable via a configuration
    #   parameter that can also be set in settings
    #
    def scan_Station_Time_Default(self):
        self.scan_Time_On_Station = gv.config.get_Scan_On_Station_Time()
        self.Time_On_Freq_VAR.set(str(int(int(gv.config.get_Scan_On_Station_Time())/1000)))

    def update_Time_On_Station_CB(self, event=None):
        self.scan_Time_On_Station = int(self.Time_On_Freq_VAR.get()) * 1000
        gv.config.set_Scan_On_Station_Time(self.scan_Time_On_Station)



    #
    #   These routines are called from the routines in piCECNextion that process memory
    #   contents sent by the MCU. The format of the information in the EEPROM was originally
    #   designed to be concise so it needs to be reformated for humans
    #

    def EEPROM_SetChanneFreqMode(self, channelNum,freq, mode):

        channels.channelList[channelNum].Set_Freq(str(freq))

        channels.channelList[channelNum].Set_Mode(EEPROM.modeNum_To_TextDict[str(mode)])

    def EEPROM_SetChannelLabel(self, channelNum, label):
        channels.channelList[channelNum].Set_Label(label)

    def EEPROM_SetChannelShowLabel(self, channelNum, showFlag):
        channels.channelList[channelNum].Set_ShowLabel(showFlag)

    #
    # method called to implement Channel->VFO request
    #
    def ChannelToVFO_CB(self):

        if self.channelSlotSelection == None:
            messagebox.showinfo("Information", "Must SELECT a channel first.",
                                parent=self)
            return

        self.mainWindow.theRadio.Set_Mode(
            EEPROM.Text_To_ModeNum[channels.channelList[self.channelSlotSelection].Get_Mode()])
        theFreq = channels.channelList[self.channelSlotSelection].Get_Freq()
        theMode = EEPROM.Text_To_ModeNum[channels.channelList[self.channelSlotSelection].Get_Mode()]

        self.mainWindow.theRadio.Set_New_Frequency(theFreq)
        # self.mainWindow.theRadio.Set_Mode(EEPROM.Text_To_ModeNum[channels.channelList[self.channelSlotSelection].Get_Mode()])

        if theMode == "DFT":
            if theFreq >= 10000000:
                self.mainWindow.theRadio.Set_Mode("USB")
            else:
                self.mainWindow.theRadio.Set_Mode("LSB")
        else:
            self.mainWindow.theRadio.Set_Mode(theMode)



        self.current_Channel['text'] = channels.channelList[self.channelSlotSelection].Get_Label()

    #
    # method called to write current VFO to channel
    #

    def VFOToChannel_CB(self):
        if self.channelSlotSelection == None:
            messagebox.showinfo("Information", "Must SELECT a channel first.",
                                parent=self)
            return
        channels.channelList[self.channelSlotSelection].Set_Freq(self.current_VFO_Label['text'])
        channels.channelList[self.channelSlotSelection].Set_Mode(self.current_Mode_Label['text'])
        channels.channelList[self.channelSlotSelection].channel_Dirty()

    #
    #   Controls the scanning process. Builds the list of channels to scan and sends it to
    #   "performScan" to actually process the list.
    #

    def startScan(self):
        self.scanRunning = True
        self.scan_Button['text'] =  "Stop Scan"
        self.scanIndex = 0
        self.scanList = []

        if self.scan_Select_Channel_VAR.get() == "None":
            messagebox.showinfo("Information", "Must SELECT a set of Channels to Scan before clicking the Scan Button",
                                parent=self)
            self.stopScan()
            return

        for i in range(len(channels.channelList)):
            if self.scanSetSelected == channels.channelList[i].Get_ScanSet():
                self.scanList.append(i)

        if len(self.scanList) == 0:
            messagebox.showinfo("Information", "No Channels attached to this Scan Set.",
                                parent=self)
            self.stopScan()
            return
        self.performScan()
    #
    #   Actually performs the scan. Note that it calls itself after "scan_Time_On_Station" happens
    #

    def performScan(self):
        self.channelSlot_CB(self.scanList[self.scanIndex])
        self.ChannelToVFO_CB()
        self.scanIndex += 1

        if self.scanIndex == len(self.scanList):
            self.scanIndex = 0
        self.scanTimer = self.master.after(self.scan_Time_On_Station, self.performScan)

    #
    #   Just handles completion of the scan after the stop button is pressed.
    #
    def stopScan(self):
        self.scanRunning = False
        self.scan_Button['text'] = "Run Scan"
        if self.scanTimer != None:
            self.master.after_cancel(self.scanTimer)
            self.scanTimer = None
        self.scanIndex = 0

    def scan_Channel_CB(self):              # method called to start channel scanning
        if self.scanRunning:
            self.stopScan()
        else:
            self.startScan()

    def runScan_Selection_CB(self, itemid):
        self.scan_Select_Channel_VAR.set(itemid.replace("_Command",""))
        self.scanSetSelected = self.scan_Select_Channel_VAR.get()

    #
    #   Callback for the Refresh button. Checks for dirty info, and then does the referesh
    #

    def refresh_Channel_CB(self):           # method called when user wants to refresh channels from EEPROM
        self.confirmExitorWriteDirty()
        self.refreshCallback()

    #
    #   Handles the request to close window. Also called if the channels window is closed
    #   via the window manager
    #
    def close_Channel_CB(self):             # method called when window closed
        self.confirmExitorWriteDirty()
        self.mainWindow.theVFO_Object.restorePresetState()
        self.stopScan()                 # Stop any scan that might be running
        self.master.withdraw()

    #
    #   Called on close or refresh to check whether any information is "dirty". If so, a dialog
    #   is popped up asking the user whether they want to save the values before exiting.
    #
    def confirmExitorWriteDirty(self):
        for channelNum in range(len(self.channelList)):
            if (channels.channelList[channelNum].dirty):
                response = messagebox.askyesno("Confirmation",
                                               "Not all channels have been saved to EEPROM\nDo you want to save these channels?",
                                               parent=self)

                # Process the user's response
                if response:  # True if "Yes" is clicked
                    self.saveAllChannels_CB()
                break
    #
    #   This method is called when the user selects a particular channel. It is a little
    #   complicated because need to figure out which of 20 possible channels has been selected.
    #   This is where the list of channels (channels.channelList) comes in!
    #
    def channelSlot_CB(self, slotNumber):
        if self.channelSlotSelection != None:
            channels.channelList[self.channelSlotSelection].channel_Select_Button.configure(
                style="Button1bRaised.TButton")
            channels.channelList[self.channelSlotSelection].channel_Select_Button['text'] = "Select"  # unselect the prior one

        if self.channelSlotSelection == slotNumber:         #Unselect if already selected
            self.channelSlotSelection = None
        else:
            self.channelSlotSelection = slotNumber
            channels.channelList[self.channelSlotSelection].channel_Select_Button.configure(
                    style="Button1bPressed.TButton")
            channels.channelList[self.channelSlotSelection].channel_Select_Button['text'] = "Selected" # select the new one
    #
    #   Does the actual saving of a particular channel when a save is requested. A "save all"
    #   just calls this method repeatedly
    #

    def saveChannel(self,channelNum):
        if channelNum == None:
            messagebox.showinfo("Information", "No Channel Selected to Save",
                                parent=self)
            return
        if  (channels.channelList[channelNum].dirty):
            channels.channelList[channelNum].channel_Not_Dirty()

            self.mainWindow.theRadio.Write_EEPROM_Channel_FreqMode(
                channelNum,
                channels.channelList[channelNum].Get_Freq(),
                channels.channelList[channelNum].Get_Mode())

            self.mainWindow.theRadio.Write_EEPROM_Channel_Label(
                channelNum,
                channels.channelList[channelNum].Get_Label())

            self.mainWindow.theRadio.Write_EEPROM_Channel_ShowLabel(
                channelNum,
                channels.channelList[channelNum].Get_ShowLabel())

            gv.config.set_ScanSet_Settings(channelNum,
                                               channels.channelList[channelNum].Get_ScanSet())
    #
    #   The two save all and save one channel button callbacks
    #

    def saveChannel_CB(self):
        self.saveChannel(self.channelSlotSelection)

    def saveAllChannels_CB(self):
        for aChannel in range(len(self.channelList)):
            self.saveChannel(aChannel)
    #
    #   This is a set of routines to export the channels to the configuration file so they can be used by the sdr
    #

    #
    #   This row just creates a row
    #
    def create_row_data(self,
            bandwidth: int, freq_hz: int, label: str, mode: str, name: str
    ) -> dict:
        """Accepts parameters and constructs a validated row dictionary for a bank."""
        # Ensure correct data types (integers for frequency/bandwidth, strings for labels)
        return {
            "bandwidth": int(bandwidth),
            "freq_hz": int(freq_hz),
            "label": str(label),
            "mode": str(mode),
            "name": str(name),
        }

    def create_new_bank(self, registry, bank_name):

        # Modify the registry directly without assigning to a temporary variable
        if bank_name in registry:
            if(messagebox.askyesno("Warning", "Bank already exists!" +
                                           "Do you want to append channels to the Bank?", parent=self)):
                return True
        else:
            registry[bank_name] = []
            return True
        return False

    def add_row_to_bank(self, registry, bank_name, row_data):
        """Appends a new row to an existing bank."""
        # Safety check to ensure the structure and bank exist
        # queue = registry.get("Scan Channels Registry Queue", {})

        if bank_name in registry:
            registry[bank_name].append(row_data)
            return True
        return False

    def exportAllChannels_CB(self):
        theBankName = self.bankName_VAR.get()
        if theBankName == "":
            messagebox.showerror("Error", "Bank Name cannot be empty", parent=self)
            return
        registry = gv.config.get_scan_channels_registry()
        if self.create_new_bank(registry,theBankName):
            for channelNum in range(len(self.channelList)):
                theFreq = int(channels.channelList[channelNum].Get_Freq())
                #
                #   If a channel has a zero frequency, then it is not valid. Skip it
                #
                if theFreq == 0:
                    print("skipping channel:", channelNum)
                    pass
                else:
                    theMode = self.channelList[channelNum].Get_Mode()
                    #
                    #   CEC has the concept of a Default Mode. We just map it to USB if >=10mhz
                    #
                    if theMode == "DFT":
                        if theFreq >= 10000000:
                            theMode = "USB"
                        else:
                            theMode = "LSB"

                    #
                    #   CEC Channels don't track bandwidth. So just make an assumption based on mode
                    #

                    if theMode == "USB" or theMode == "LSB":
                        theBandwidth = 2600
                    else:
                        theBandwidth = 500

                    #
                    #   Finally clean up the labels and names
                    #
                    theLabel = "CH"+str(channelNum)
                    theName = channels.channelList[channelNum].Get_Label()
                    #
                    #   Labels in CEC are 5 characters, but only first 9 channels can have labels
                    #   So anything that is just blanks ot
                    if theName == "" or theName.replace(" ","") == "" or theName == "*N/A*":
                        theName = ""

                    newRow = self.create_row_data(
                        bandwidth=theBandwidth,
                        freq_hz=theFreq,
                        label=theLabel,
                        mode=theMode,
                        name=theName
                    )
                    print(newRow)
                    self.add_row_to_bank(registry, theBankName, newRow)
            gv.config.set_scan_channels_registry(registry)



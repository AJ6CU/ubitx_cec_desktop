#!/usr/bin/python3
"""
settingsSDR

Used to save of machines

UI source file: settingsSDR.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import settingsSDRui as baseui
from tkinter import messagebox

from entryFieldHandler import entryFieldHandler
from VirtualNumericKeyboard import VirtualNumericKeyboard
from VirtualKeyboard import VirtualKeyboard

import globalvars as gv


#
# Manual user code
#

class settingsSDR(baseui.settingsSDRUI):
    def __init__(self, master=None, mainWindow=None, **kw):
        self.master = master
        self.mainWindow = mainWindow
        #
        #   Create a toplevel window to contain the settings popup
        #
        self.popup = tk.Toplevel(self.master)
        super().__init__(self.popup, **kw)
        #
        #   Save entry values
        #
        self.saveSDR_Switch = gv.config.get_SDR_Switch()
        self.saveSDR_Software = gv.config.get_SDR_Software()
        # print("from config", gv.config.get_SDR_Autostart(), type(gv.config.get_SDR_Autostart()))
        self.saveSDR_Autostart = gv.config.get_SDR_Autostart()   ### need to add
        self.saveNetworkAddress = str(gv.config.get_sdr_server_ip())
        self.saveNetworkPort = str(gv.config.get_sdr_tcp_port())
        self.saveCW_Bandwidth = str(gv.config.get_sdr_cw_filter_default_hz())
        self.saveSSB_Bandwidth = str(gv.config.get_sdr_ssb_filter_default_hz())

        self.initUX()

    def initUX(self):
        self.popup.title("SDR Settings")
        self.popup.geometry(gv.POPUP_WINDOW_OFFSET)

        self.popup.wait_visibility()  # required on Linux
        self.popup.grab_set()
        self.popup.transient(self.mainWindow)
        #
        #   Assign Text Vars
        #
        gv.make_widget_variable(self, "SDR_Enable", self.SDR_Enable_Menubutton)
        gv.make_widget_variable(self, "SDR_Software", self.sdrSoftware_Menubutton)

        gv.make_widget_variable(self, "networkAddress", self.ipAddress_Entry)
        gv.make_widget_variable(self, "networkPort", self.networkPort_Entry)

        gv.make_widget_variable(self, "cwDefault", self.cwDefault_Spinbox)
        gv.make_widget_variable(self, "ssbDefault", self.ssbDefault_Spinbox)
#
        #
        # Have to handle this manually because it is a "variable" and not "textvariable"
        #
        self.autostartSDR_VAR = tk.StringVar(master=self.autostartSDR_Checkbox)
        self.autostartSDR_Checkbox.configure(variable=self.autostartSDR_VAR)



        self.SDR_Enable_VAR.set(self.saveSDR_Switch)
        self.SDR_Software_VAR.set(self.saveSDR_Software)
        self.autostartSDR_VAR.set(self.saveSDR_Autostart)
        self.networkAddress_VAR.set(self.saveNetworkAddress)
        self.networkPort_VAR.set(self.saveNetworkPort)
        self.cwDefault_VAR.set(self.saveCW_Bandwidth)
        self.ssbDefault_VAR.set(self.saveSSB_Bandwidth)

        self.networkPort_Object = entryFieldHandler(self, "networkPort", 5, VirtualNumericKeyboard, self.popup)



        self.pack(expand=tk.YES, fill=tk.BOTH)



    def selectSDR_On_CB(self):
        self.SDR_Enable_VAR.set("True")

    def selectSDR_Off_CB(self):
        self.SDR_Enable_VAR.set("False")

    def selectSDRPlusPlus_CB(self):
        pass

    def autostartSDR_CB(self):
        pass

    def cwDefault_CB(self):
        pass

    def ssbDefault_CB(self):
        pass

    def networkPort_validation(self):
        if gv.validateNumber(self.networkPort_VAR.get(), 0,65535):
            return True
        else:
            return False


    def networkPort_errorHandler(self):
        messagebox.showinfo("Error - Invalid Port",
                            "Ports must be in range of 0 - 65,535\n\n" +
                            " Input ignored, resetting to prior value", parent=self)


    def networkPort_preProcessor(self):
        return self.networkPort_VAR.get()


    def networkPort_postProcessor(self):
        return


    def apply_CB(self):
        if self.saveSDR_Switch != self.SDR_Enable_VAR.get():
            gv.config.set_SDR_Switch(self.SDR_Enable_VAR.get())

        if self.saveSDR_Software != self.SDR_Software_VAR.get():
            gv.config.set_SDR_Software(self.SDR_Software_VAR.get())
        print(self.saveSDR_Autostart,self.autostartSDR_VAR.get())
        if self.saveSDR_Autostart != self.autostartSDR_VAR.get():
            gv.config.set_SDR_Autostart(self.autostartSDR_VAR.get())  ### need to add

        if self.saveNetworkAddress != self.networkAddress_VAR.get():
            gv.config.set_sdr_server_ip(self.networkAddress_VAR.get())

        if self.saveNetworkPort != self.networkPort_VAR.get():
            gv.config.set_sdr_tcp_port(int(self.networkPort_VAR.get()))

        if self.saveCW_Bandwidth != self.cwDefault_VAR.get():
            gv.config.set_sdr_cw_filter_default_hz(int(self.cwDefault_VAR.get()))

        if self.saveSSB_Bandwidth != self.ssbDefault_VAR.get():
            gv.config.set_sdr_ssb_filter_default_hz(int(self.ssbDefault_VAR.get()))

        self.master.destroy()

    def cancel_CB(self):
        self.master.destroy()


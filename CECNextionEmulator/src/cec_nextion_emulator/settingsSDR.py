#!/usr/bin/python3
"""
settingsSDR

Used to save of machines

UI source file: settingsSDR.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import settingsSDRui as baseui
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

        self.SDR_Enable_VAR.set(self.saveSDR_Switch)
        self.SDR_Software_VAR.set(self.saveSDR_Software)
        self.autostartSDR_VAR.set(self.saveSDR_Autostart)
        self.networkAddress_VAR.set(self.saveNetworkAddress)
        self.networkPort_VAR.set(self.saveNetworkPort)
        self.cwDefault_VAR.set(self.saveCW_Bandwidth)
        self.ssbDefault_VAR.set(self.saveSSB_Bandwidth)



        self.pack(expand=tk.YES, fill=tk.BOTH)



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

    def exportEEPROMChannels_CB(self):
        pass

    def apply_CB(self):
        pass

    def cancel_CB(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    widget = settingsSDR(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()

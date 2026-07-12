#!/usr/bin/python3
"""
settingsAbout

Used to save general settings

UI source file: settingsAbout.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import settingsAboutui as baseui
import globalvars as gv
import os


#
# Manual user code
#

class settingsAbout(baseui.settingsAboutUI):

    def __init__(self, master=None, mainWindow=None, **kw):
        self.master = master
        self.mainWindow = mainWindow
        #
        #   Create a toplevel window to contain the settings popup
        #
        self.popup = tk.Toplevel(self.master)

        super().__init__(self.popup, **kw)
        #
        #   Make sure that a close by the Window manager goes to the same close callback
        #
        self.popup.protocol("WM_DELETE_WINDOW", self.close_CB)

        super().__init__(self.master, **kw)

        self.initUX()

    def initUX(self):
        self.popup.title("About CECNextionEmulator")

        self.popup.geometry(gv.POPUP_WINDOW_OFFSET)

        self.popup.wait_visibility()  # required on Linux
        self.popup.grab_set()
        self.popup.transient(self.mainWindow)

        self.versionID_Label['text'] = gv.APPVERSION
        self.releaseDate_Label['text'] = gv.APPDATE
        self.configurationFileLocation_Label['text'] = os.path.expanduser(os.path.join("~", ".ubitx_cec_desktop.ini"))
        self.logFileLocation_Label['text'] = os.path.expanduser(os.path.join(gv.config.get_Logbook_Location(),
                                                                             gv.config.get_Logbook_Name()))


        self.pack(expand=tk.YES, fill=tk.BOTH)


    def close_CB(self):
        self.popup.destroy()



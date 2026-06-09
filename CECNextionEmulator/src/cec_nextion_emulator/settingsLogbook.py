#!/usr/bin/python3
"""
settingsLogbook

Manages the settings for the logbook function

UI source file: settingsLogbook.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import settingsLogbookui as baseui
import globalvars as gv


#
# Manual user code
#

class settingsLogbook(baseui.settingsLogbookUI):
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
        self.popup.protocol("WM_DELETE_WINDOW", self.cancel_CB)

        self.initUX()

    def initUX(self):
        self.popup.title("Logbook Settings")

        self.logbookSwitch_VAR.set(gv.config.get_logbook_Switch())
        self.logbookType_VAR.set(gv.config.get_logbook_Type())
        self.logbookName_VAR.set(gv.config.get_logbook_Name())
        self.logbookLocation_Text.insert("1.0",gv.config.get_logbook_Location())
        self.logbookLocation_Text.configure(state="disabled")

        if self.logbookSwitch_VAR.get() == "False":
            self.logbookType_Menubutton.configure(state="disabled")
            self.logbookFileSelectorButton.configure(state="disabled")


        self.popup.geometry(gv.POPUP_WINDOW_OFFSET)

        self.popup.wait_visibility()  # required on Linux
        self.popup.grab_set()
        self.popup.transient(self.mainWindow)

        self.pack(expand=tk.YES, fill=tk.BOTH)

    def selectLogbookOn_CB(self):
        self.logbookSwitch_VAR.set("True")
        self.logbookType_Menubutton.configure(state="normal")
        self.logbookFileSelectorButton.configure(state="normal")


    def selectLogbookOff_CB(self):
        self.logbookSwitch_VAR.set("False")

        self.logbookType_Menubutton.configure(state="disabled")
        self.logbookFileSelectorButton.configure(state="disabled")



    def selectLogbookType_CSV_CB(self):
        self.logbookType_VAR.set("CSV")


    def selectLogbookType_ADI_CB(self):
        self.logbookType_VAR.set("ADI")


    def newLogbookLocation_CB(self, event=None):
        newpath = self.logbookFileSelectorButton.cget('path')
        self.logbookLocation_Text.configure(state="normal")
        self.logbookLocation_Text.delete("1.0", tk.END)
        self.logbookLocation_Text.insert("1.0",newpath)
        self.logbookLocation_Text.configure(state="disabled")


    def apply_CB(self):
        gv.config.set_logbook_Switch(self.logbookSwitch_VAR.get())
        gv.config.set_logbook_Type(self.logbookType_VAR.get())
        gv.config.set_logbook_Name(self.logbookName_VAR.get())
        gv.config.set_logbook_Location(self.logbookLocation_Text.get("1.0", "end-1c"))
        self.popup.destroy()

    def cancel_CB(self):
        self.popup.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    widget = settingsLogbook(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()

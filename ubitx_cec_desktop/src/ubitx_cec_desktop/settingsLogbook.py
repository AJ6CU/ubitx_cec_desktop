#!/usr/bin/python3
"""
settingsLogbook

Manages the settings for the Logbook function

UI source file: settingsLogbook.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import settingsLogbookui as baseui
import globalvars as gv
from QSOLogger import QSOLogger
from tkinter import messagebox
from VirtualKeyboard import VirtualKeyboard
import os
from pathvalidate import sanitize_filename, is_valid_filename


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

        self.LogbookSwitch_VAR.set(gv.config.get_Logbook_Switch())
        self.LogbookSwitchSave = gv.config.get_Logbook_Switch()

        self.LogbookType_VAR.set(gv.config.get_Logbook_Type())
        self.LogbookTypeSave = gv.config.get_Logbook_Type()

        self.Backup_Interval_VAR.set(gv.config.get_Logbook_Backup_Interval())
        self.Backup_Interval_Save = gv.config.get_Logbook_Backup_Interval()

        self.LogbookName_VAR.set(gv.config.get_Logbook_Name())
        self.LogbookNameSave = gv.config.get_Logbook_Name()

        self.LogbookLocation_Text.insert("1.0",gv.config.get_Logbook_Location())
        self.LogbookLocationSave = gv.config.get_Logbook_Location()

        self.LogbookLocation_Text.configure(state="disabled")

        if self.LogbookSwitch_VAR.get() == "False":
            self.LogbookType_Menubutton.configure(state="disabled")
            self.LogbookFileSelectorButton.configure(state="disabled")
            self.backupInterval_Spinbox.configure(state="disabled")
            self.mainWindow.logQSO_Button.configure(state="disabled")


        self.popup.geometry(gv.POPUP_WINDOW_OFFSET)

        self.popup.wait_visibility()  # required on Linux
        self.popup.grab_set()
        self.popup.transient(self.mainWindow)

        self.pack(expand=tk.YES, fill=tk.BOTH)

    def selectLogbookOn_CB(self):
        self.LogbookSwitch_VAR.set("True")
        self.LogbookType_Menubutton.configure(state="normal")
        self.LogbookFileSelectorButton.configure(state="normal")
        self.backupInterval_Spinbox.configure(state="normal")
        self.mainWindow.logQSO_Button.configure(state="normal")


    def selectLogbookOff_CB(self):
        self.LogbookSwitch_VAR.set("False")

        self.LogbookType_Menubutton.configure(state="disabled")
        self.LogbookFileSelectorButton.configure(state="disabled")
        self.backupInterval_Spinbox.configure(state="disabled")
        self.mainWindow.logQSO_Button.configure(state="disabled")



    def selectLogbookType_CSV_CB(self):
        self.LogbookType_VAR.set("csv")


    def selectLogbookType_ADI_CB(self):
        self.LogbookType_VAR.set("adi")


    def newLogbookLocation_CB(self, event=None):
        newpath = self.LogbookFileSelectorButton.cget('path')
        self.LogbookLocation_Text.configure(state="normal")
        self.LogbookLocation_Text.delete("1.0", tk.END)
        self.LogbookLocation_Text.insert("1.0",newpath)
        self.LogbookLocation_Text.configure(state="disabled")


    def apply_CB(self):

        newType = False
        newName = False
        newBackup_Interval = False

        if self.LogbookSwitchSave != self.LogbookSwitch_VAR.get():
            gv.config.set_Logbook_Switch(self.LogbookSwitch_VAR.get())

        if self.LogbookTypeSave != self.LogbookType_VAR.get():
            gv.config.set_Logbook_Type(self.LogbookType_VAR.get())
            newType = True

        if self.LogbookNameSave != self.LogbookName_VAR.get():
            if len(self.LogbookName_VAR.get()) > 0:
                gv.config.set_Logbook_Name(self.LogbookName_VAR.get())
                newName = True
            else:
                messagebox.showerror("Error - Zero Length Logfile Name ", "Logbook File Name cannot be empty", parent=self)
                self.LogbookName_VAR.set(gv.config.get_Logbook_Name())
                return


        if self.LogbookLocationSave != self.LogbookLocation_Text.get("1.0", "end-1c"):
            gv.config.set_Logbook_Location(self.LogbookLocation_Text.get("1.0", "end-1c"))
            newName = True

        if self.Backup_Interval_VAR.get() != self.Backup_Interval_Save:
            gv.config.set_Logbook_BackupInterval(self.Backup_Interval_VAR.get())
            newBackup_Interval = True

        if (gv.config.get_Logbook_Switch() == "False"):
            if (self.mainWindow.QSOLogger_Object != None):  # If turnoff logger, destroy the object
                self.mainWindow.QSOLogger_Object = None
                self.mainWindow.logQSO_Button.configure(state="disabled")

        else:
            theLogbook = os.path.expanduser(os.path.join(gv.config.get_Logbook_Location(),gv.config.get_Logbook_Name()))

            if self.mainWindow.QSOLogger_Object == None:           # Create new object
                self.mainWindow.QSOLogger_Object = QSOLogger(gv.config.get_Logbook_Type(), theLogbook)
                self.mainWindow.QSOLogger_Object.set_backup_interval(int(gv.config.get_Logbook_Backup_Interval()))
            else:
                if newType:
                    self.mainWindow.QSOLogger_Object.change_format(gv.config.get_Logbook_Type())
                if newName:
                    self.mainWindow.QSOLogger_Object.set_filename(theLogbook)
                if newBackup_Interval:
                    self.mainWindow.QSOLogger_Object.set_backup_interval(int(gv.config.get_Logbook_BackupInterval()))

        self.popup.destroy()

    #
    #   The following callbacks handle the entry of the filename for the log.
    #   Logbook_Name_Entered_CB is fired when the user clicks down on the entry field. If
    #   the virtual keyboard switch is true, a virtual keyboard will be popped up on the screen.
    #   After the user enters the new filename, the LogbookName_VKeyboard_Validate is called.
    #   It checks the validity of the entry and if not valid, calls the Logbook_Name_Invalid_CB to
    #   eliminate bad characters and set the file name.
    #
    #   If there is no virtual keyboard in use, the user enters via the keyboard and when focus goes out, the
    #   Logbook_Name_Validation_CB is fired to check the entry. If it returns, False, then the Logbook_Name_Invalid_CB
    #   is used to delete bad characters and make a best quess
    #

    def Logbook_Name_Entered_CB(self, event=None):
        if gv.config.get_Virtual_Keyboard_Switch() == "True":
            self.vKeyboard = VirtualKeyboard(self, self.LogbookName_VAR, self.LogbookName_Vkeyboard_Validate, 40)

    def Logbook_Name_Validation_CB(self, p_entry_value, v_condition):
        if is_valid_filename(p_entry_value):
            return True
        else:
            return False

    def Logbook_Name_Invalid_CB(self, p_entry_value):
        self.validFname = sanitize_filename(p_entry_value)

        self.LogbookName_Entry.delete(0, "end")
        self.LogbookName_Entry.insert(0, self.validFname)
        messagebox.showinfo("Error Illegal Filename", p_entry_value + "\n\nis not a legal filename.\n\n" +
                            self.validFname + "\n\nis the closest legal name and will be used.", parent=self)

    def LogbookName_Vkeyboard_Validate(self):
        if is_valid_filename(self.LogbookName_VAR.get()) == False:
            self.Logbook_Name_Invalid_CB(self.LogbookName_VAR.get())


    def cancel_CB(self):
        self.popup.destroy()


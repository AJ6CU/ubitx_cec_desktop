#!/usr/bin/python3
"""
generalSettings_sCTk

first try at settings dialog

UI source file: generalSettings_sCTk.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import generalSettings_sCTkui as baseui
import customtkinter as ctk
from sCTkDialogMixin import sCTkDialogMixin


#
# Manual user code
#

class generalSettings_sCTk(sCTkDialogMixin, baseui.generalSettings_sCTkUI):
    def __init__(self, master=None, dialogType=None, **kw):

        super().__init__(master, **kw)

        self.setHeading("mark and sue", "W")
        # self.setTwoButton()
        self.setApplyButton("Please", self.easyCB)
        self.setCancelButton("Kill", self.easyCB)
        self.setResetButton("do over")
        self.setResetButton(None,self.easyCB)

    def apply_CB(self):
        print("apply_CB")

    def easyCB(self):
        print("easyCB")

    def reset_CB(self):
        print("reset_CB")

if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()
    widget = generalSettings_sCTk(root)
    widget.setTitle("generalSettings_sCTk test")
    # widget.runAndWait()
    # widget.pack(expand=True, fill="both")
    root.mainloop()

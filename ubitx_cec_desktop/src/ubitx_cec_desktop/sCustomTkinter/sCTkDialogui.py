#!/usr/bin/python3
"""
sCTkDialog

a special widget deciated to making popup dialogs consistent

UI source file: sCTkDialog.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import CTkToplevel
from sCTkButtonPrimary import sCTkButtonPrimary
from sCTkButtonSecondary import sCTkButtonSecondary
from sCTkFrame import sCTkFrame
from sCTkLabelPrimary import sCTkLabelPrimary


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
class sCTkDialogUI(CTkToplevel):
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

        sctkframe3 = sCTkFrame(self)
        # First object created
        on_first_object_cb(sctkframe3)

        self.titleFrame = sCTkFrame(sctkframe3)
        self.titleLabel = sCTkLabelPrimary(self.titleFrame)
        self.titleLabel.configure(text='Settings Title')
        self.titleLabel.pack(side="top")
        self.titleFrame.grid(column=0, row=0)
        self.contentFrame = sCTkFrame(sctkframe3)
        self.contentFrame.configure(width=500)
        sctkbuttonprimary2 = sCTkButtonPrimary(self.contentFrame)
        sctkbuttonprimary2.configure(text='sctkbuttonprimary2')
        sctkbuttonprimary2.pack(side="top")
        self.contentFrame.grid(column=0, row=1)
        self.actionFrame = sCTkFrame(sctkframe3)
        sctkbuttonprimary1 = sCTkButtonPrimary(self.actionFrame)
        sctkbuttonprimary1.configure(text='Apply')
        sctkbuttonprimary1.grid(column=0, padx=10, row=0)
        sctkbuttonprimary1.configure(command=self.apply_CB)
        sctkbuttonsecondary1 = sCTkButtonSecondary(self.actionFrame)
        sctkbuttonsecondary1.configure(text='Cancel')
        sctkbuttonsecondary1.grid(column=1, padx=10, row=0)
        sctkbuttonsecondary1.configure(command=self.cancel_CB)
        sctkbuttonsecondary2 = sCTkButtonSecondary(self.actionFrame)
        sctkbuttonsecondary2.configure(text='Reset')
        sctkbuttonsecondary2.grid(column=2, padx=10, row=0)
        sctkbuttonsecondary2.configure(command=self.reset_CB)
        self.actionFrame.grid(column=0, row=2)
        self.actionFrame.grid_anchor("s")
        sctkframe3.pack(side="top")
        self.title("settings window title")
        # Layout for 'ctktoplevel1' skipped in custom widget template.

    def apply_CB(self):
        pass

    def cancel_CB(self):
        pass

    def reset_CB(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkDialogUI(root)
    root.mainloop()

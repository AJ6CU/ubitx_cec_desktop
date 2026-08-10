#!/usr/bin/python3
"""
sCTkDialogCore

a special widget deciated to making popup dialogs consistent

UI source file: sCTkDialogCore.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
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
class sCTkDialogCoreUI(sCTkFrame):
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

        self.titleFrame = sCTkFrame(self)
        # First object created
        on_first_object_cb(self.titleFrame)

        self.heading_Label = sCTkLabelPrimary(self.titleFrame)
        self.heading_VAR = tk.StringVar(value='Heading Title')
        self.heading_Label.configure(
            anchor="center",
            text='Heading Title',
            textvariable=self.heading_VAR)
        self.heading_Label.pack(expand=True, fill="x", side="top")
        self.titleFrame.pack(
            anchor="n",
            expand=True,
            fill="x",
            padx=10,
            pady="20 10",
            side="top")
        self.contentFrame = sCTkFrame(self)
        self.contentFrame.configure(width=500)
        self.contentFrame.pack(expand=True, fill="both", padx=5, side="top")
        self.actionFrame = sCTkFrame(self)
        self.apply_Button = sCTkButtonPrimary(self.actionFrame)
        self.applyText_VAR = tk.StringVar(value='Apply')
        self.apply_Button.configure(
            text='Apply', textvariable=self.applyText_VAR)
        self.apply_Button.grid(column=0, padx=10, row=0)
        self.apply_Button.configure(command=self.apply_CB)
        self.cancel_Button = sCTkButtonSecondary(self.actionFrame)
        self.cancelText_VAR = tk.StringVar(value='Cancel')
        self.cancel_Button.configure(
            text='Cancel', textvariable=self.cancelText_VAR)
        self.cancel_Button.grid(column=1, padx=10, row=0)
        self.cancel_Button.configure(command=self.cancel_CB)
        self.reset_Button = sCTkButtonSecondary(self.actionFrame)
        self.resetText_VAR = tk.StringVar(value='Reset')
        self.reset_Button.configure(
            text='Reset', textvariable=self.resetText_VAR)
        self.reset_Button.grid(column=2, padx=10, row=0)
        self.reset_Button.configure(command=self.reset_CB)
        self.actionFrame.pack(
            anchor="s",
            expand=True,
            fill="x",
            padx=5,
            pady="10 20",
            side="top")
        self.actionFrame.grid_anchor("s")
        # Layout for 'sCTkDialogCoreFrame' skipped in custom widget template.

    def apply_CB(self):
        pass

    def cancel_CB(self):
        pass

    def reset_CB(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkDialogCoreUI(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()

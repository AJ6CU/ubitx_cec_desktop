#!/usr/bin/python3
"""
newdeleteme

newdeleteme

UI source file: newdeleteme.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import (CTkLabel, CTkProgressBar, CTkToplevel)
from sCTkDialog import sCTkDialog


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
class newdeletemeUI(CTkToplevel):
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

        sctkdialog1 = sCTkDialog(self)
        # First object created
        on_first_object_cb(sctkdialog1)

        ctklabel1 = CTkLabel(sctkdialog1)
        ctklabel1.configure(text='ctklabel1')
        ctklabel1.pack(side="top")
        ctkprogressbar1 = CTkProgressBar(sctkdialog1)
        ctkprogressbar1.pack(side="top")
        ctkprogressbar2 = CTkProgressBar(sctkdialog1)
        ctkprogressbar2.pack(side="top")
        sctkdialog1.pack(side="top")
        # Layout for 'ctktoplevel1' skipped in custom widget template.


if __name__ == "__main__":
    root = tk.Tk()
    widget = newdeletemeUI(root)
    root.mainloop()

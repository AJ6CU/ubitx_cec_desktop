#!/usr/bin/python3
"""
dialogCommand

test

UI source file: dialogCommand.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import (CTkEntry, CTkLabel)
from dialogBase import dialogBase


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
class dialogFrameUI(dialogBase):
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

        frame2 = ttk.Frame(self.contentFrame)
        frame2.configure(height=200, width=200)
        # First object created
        on_first_object_cb(frame2)

        ctklabel1 = CTkLabel(frame2)
        ctklabel1.configure(text='Test Label')
        ctklabel1.pack(side="top")
        ctkentry1 = CTkEntry(frame2)
        ctkentry1.delete(0, "end")
        ctkentry1.insert(0, 'enter data')
        ctkentry1.pack(side="top")
        frame2.pack(side="top")
        # Layout for 'dialogbase1' skipped in custom widget template.


if __name__ == "__main__":
    root = tk.Tk()
    widget = dialogFrameUI(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()

#!/usr/bin/python3
"""
radioButton

derived from radioButton

UI source file: radioButton.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import CTkRadioButton


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
class radioButtonUI(CTkRadioButton):
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

        self.configure(text='ctkradiobutton1')
        # Layout for 'radioButtonTemplate' skipped in custom widget template.


if __name__ == "__main__":
    root = tk.Tk()
    widget = radioButtonUI(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()

#!/usr/bin/python3
"""
Progress Warning Dialog

Just pops up a warning dialog

UI source file: progress_warning.ui
"""
import tkinter as tk
import tkinter.ttk as ttk


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
class delayWarningUI(tk.Toplevel):
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

        self.warningFrame = ttk.Frame(self, name="warningframe")
        self.warningFrame.configure(
            height=200, style="Normal.TFrame", width=200)
        # First object created
        on_first_object_cb(self.warningFrame)

        self.warningLabel = ttk.Label(self.warningFrame, name="warninglabel")
        self.warningLabel_VAR = tk.StringVar(
            value='Loading...\n\nThis could take several seconds...')
        self.warningLabel.configure(
            anchor="w",
            justify="center",
            style="Heading2bi.TLabel",
            text='Loading...\n\nThis could take several seconds...',
            textvariable=self.warningLabel_VAR)
        self.warningLabel.pack(padx=10, pady=10, side="top")
        self.warningFrame.pack(expand=True, fill="both", side="top")
        self.configure(height=200, width=200)
        self.title("Warning... Delay")
        # Layout for 'delay_warning' skipped in custom widget template.



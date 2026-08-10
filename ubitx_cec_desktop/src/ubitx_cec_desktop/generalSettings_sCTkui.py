#!/usr/bin/python3
"""
generalSettings_sCTk

first try at settings dialog

UI source file: generalSettings_sCTk.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from sCTkCheckBox import sCTkCheckBox
from sCTkComboBox import sCTkComboBox
from sCTkDialogCore import sCTkDialogCore
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
class generalSettings_sCTkUI(sCTkDialogCore):
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

        sctkcheckbox1 = sCTkCheckBox(self.contentFrame)
        sctkcheckbox1.configure(text='sctkcheckbox1')
        # First object created
        on_first_object_cb(sctkcheckbox1)

        sctkcheckbox1.grid(column=0, row=0)
        sctkcheckbox1.configure(command=self.checked_CB)
        sctkcombobox1 = sCTkComboBox(self.contentFrame)
        sctkcombobox1.grid(column=1, row=0)
        sctkcombobox1.configure(command=self.selected_CB)
        sctklabelprimary1 = sCTkLabelPrimary(self.contentFrame)
        self.test_label_VAR = tk.StringVar(value='sctklabelprimary1')
        sctklabelprimary1.configure(
            text='sctklabelprimary1',
            textvariable=self.test_label_VAR)
        sctklabelprimary1.grid(column=0, row=1)
        # Layout for 'sctkdialogcore1' skipped in custom widget template.

    def checked_CB(self):
        pass

    def selected_CB(self, value):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    widget = generalSettings_sCTkUI(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()

#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


def i18n_translator_noop(value):
    """i18n - Setup translator in derived class file"""
    return value


def first_object_callback_noop(widget):
    """on first objec callback - Setup callback in derived class file."""
    pass


def image_loader_default(master, image_name: str):
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
class Classic_uBITX_ControlUI(ttk.Labelframe):
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
            translator = i18n_translator_noop
        _ = translator  # i18n string marker.
        if image_loader is None:
            image_loader = image_loader_default
        if on_first_object_cb is None:
            on_first_object_cb = first_object_callback_noop

        super().__init__(master, **kw)

        self.greenBoxSelection_Label = ttk.Label(
            self, name="greenboxselection_label")
        self.greenBoxSelection_VAR = tk.StringVar()
        self.greenBoxSelection_Label.configure(
            style="GreenBox.TLabel",
            textvariable=self.greenBoxSelection_VAR,
            width=22)
        # First object created
        on_first_object_cb(self.greenBoxSelection_Label)

        self.greenBoxSelection_Label.pack(
            expand=True, fill="x", padx=5, pady="10 0", side="top")
        self.greenBoxInstructions_Label = ttk.Label(
            self, name="greenboxinstructions_label")
        self.greenBoxInstructions_VAR = tk.StringVar()
        self.greenBoxInstructions_Label.configure(
            style="GreenBoxi.TLabel",
            textvariable=self.greenBoxInstructions_VAR,
            width=22)
        self.greenBoxInstructions_Label.pack(
            expand=True, fill="x", padx=5, pady="15 5", side="bottom")
        self.configure(
            height=200,
            style="GreenBox.TLabelframe",
            text='Classic uBITX Control',
            width=200)
        # Layout for 'greenBox_Labelframe' skipped in custom widget template.


if __name__ == "__main__":
    root = tk.Tk()
    widget = Classic_uBITX_ControlUI(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()

#!/usr/bin/python3
"""
customCTK_WidgetTesterPart4

just tests each widget

UI source file: customCTK_WidgetTesterPart4.ui
"""
from customtkinter import (CTk, CTkComboBox, CTkEntry, CTkFrame)
from sCTkFrame import sCTkFrame
from sCTkSMeter import sCTkSMeter
from sCTkTableview import sCTkTableview


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


class customCTK_WidgetTesterPart4UI:
    def __init__(
        self,
        master=None,
        *,
        translator=None,
        on_first_object_cb=None,
        data_pool=None,
        image_loader=None
    ):
        if translator is None:
            translator = safe_i18n_translator
        _ = translator  # i18n string marker.
        if image_loader is None:
            image_loader = safe_image_loader
        if on_first_object_cb is None:
            on_first_object_cb = safe_fo_callback
        # build ui
        ctk1 = CTk(None)
        # First object created
        on_first_object_cb(ctk1)

        ctkframe1 = CTkFrame(ctk1)
        sctkframe5 = sCTkFrame(ctkframe1)
        sctktableview1 = sCTkTableview(sctkframe5)
        sctktableview1.configure(
            columns="AJ6CU, Frequency, Mode, Power, Station",
            grid_mode="zebra",
            header_line_width=4,
            num_columns=3,
            num_rows=8,
            show_headers=True)
        sctktableview1.pack(side="top")
        sctkframe5.grid(column=0, row=0)
        sctkframe6 = sCTkFrame(ctkframe1)
        sctkframe6.configure(bg_color="green", height=200, width=200)
        ctkentry2 = CTkEntry(sctkframe6)
        ctkentry2.delete(0, "end")
        ctkentry2.insert(0, 'ctkentry2')
        ctkentry2.pack(side="top")
        ctkcombobox3 = CTkComboBox(sctkframe6)
        ctkcombobox3.pack(side="top")
        sctkframe6.grid(column=1, row=0)
        sctkframe6.pack_propagate(0)
        sctkframe1 = sCTkFrame(ctkframe1)
        sctksmeter1 = sCTkSMeter(sctkframe1)
        sctksmeter1.configure(sig_max_value=60, sig_min_value=0)
        sctksmeter1.pack(side="top")
        sctkframe1.grid(column=2, row=0)
        ctkframe1.pack(side="top")

        # Main widget
        self.mainwindow = ctk1

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = customCTK_WidgetTesterPart4UI()
    app.run()

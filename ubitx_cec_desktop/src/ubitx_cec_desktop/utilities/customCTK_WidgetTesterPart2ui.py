#!/usr/bin/python3
"""
customCTK_WidgetTesterPart2

just tests eah widget

UI source file: customCTK_WidgetTesterPart2.ui
"""
from checkBox import checkBox
from comboBox import comboBox
from customtkinter import (
    CTk,
    CTkCheckBox,
    CTkComboBox,
    CTkFrame,
    CTkLabel,
    CTkProgressBar,
    CTkRadioButton,
    CTkSegmentedButton,
    CTkSlider,
    CTkSwitch)
from frameLabeledPrimary import frameLabeledPrimary
from progressBar import progressBar
from radioButton import radioButton
from segmentedButton import segmentedButton
from slider import slider
from switch import switch


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


class customCTK_WidgetTesterPart2UI:
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
        ctkframe1.configure(border_color="green", border_width=2)
        framelabeledprimary5 = frameLabeledPrimary(ctkframe1)
        framelabeledprimary5.configure(
            label_anchor="w", label_text="CheckBox and ComboBox")
        ctklabel1 = CTkLabel(framelabeledprimary5)
        ctklabel1.configure(text='ctk:')
        ctklabel1.grid(column=0, padx="0 5", row=0, sticky="e")
        ctkcheckbox1 = CTkCheckBox(framelabeledprimary5)
        ctkcheckbox1.configure(text='ctkCheckbox')
        ctkcheckbox1.grid(column=1, row=0, sticky="w")
        ctklabel2 = CTkLabel(framelabeledprimary5)
        ctklabel2.configure(text='subCTk:')
        ctklabel2.grid(column=0, padx="0 5", row=1, sticky="e")
        checkbox1 = checkBox(framelabeledprimary5)
        checkbox1.configure(text='subCheckbox')
        checkbox1.grid(column=1, row=1, sticky="w")
        ctklabel3 = CTkLabel(framelabeledprimary5)
        ctklabel3.configure(text='ctk:')
        ctklabel3.grid(column=0, padx="0 5", pady="20 0", row=2, sticky="e")
        ctkcombobox1 = CTkComboBox(framelabeledprimary5)
        ctkcombobox1.grid(column=1, pady="20 0", row=2)
        ctklabel4 = CTkLabel(framelabeledprimary5)
        ctklabel4.configure(text='subCTk:')
        ctklabel4.grid(column=0, padx="0 5", row=3, sticky="e")
        combobox1 = comboBox(framelabeledprimary5)
        combobox1.configure(values=["apple", "pear", "grape"])
        combobox1.grid(column=1, row=3)
        framelabeledprimary5.grid(
            column=0,
            padx="20 10",
            pady=20,
            row=0,
            sticky="ew")
        framelabeledprimary5.bind("<MouseWheel>", self.callback, add="")
        framelabeled1 = frameLabeledPrimary(ctkframe1)
        framelabeled1.configure(
            label_anchor="w",
            label_text="Progressbars and Sliders")
        ctklabel5 = CTkLabel(framelabeled1)
        ctklabel5.configure(text='ctk:')
        ctklabel5.pack()
        ctkprogressbar1 = CTkProgressBar(framelabeled1)
        ctkprogressbar1.pack(side="top")
        ctklabel6 = CTkLabel(framelabeled1)
        ctklabel6.configure(text='subCTk:')
        ctklabel6.pack()
        progressbar1 = progressBar(framelabeled1)
        progressbar1.pack(side="top")
        ctklabel7 = CTkLabel(framelabeled1)
        ctklabel7.configure(text='ctk:')
        ctklabel7.pack(pady="20 0")
        ctkslider1 = CTkSlider(framelabeled1)
        ctkslider1.pack(side="top")
        ctklabel8 = CTkLabel(framelabeled1)
        ctklabel8.configure(text='subCTk:')
        ctklabel8.pack()
        slider1 = slider(framelabeled1)
        slider1.pack(side="top")
        framelabeled1.grid(column=1, padx="20 10", pady=20, row=0, sticky="ew")
        framelabeled1.bind("<MouseWheel>", self.callback, add="")
        framelabeledprimary6 = frameLabeledPrimary(ctkframe1)
        framelabeledprimary6.configure(
            label_anchor="w",
            label_text="RadioButton and Switch")
        ctklabel9 = CTkLabel(framelabeledprimary6)
        ctklabel9.configure(text='ctk:')
        ctklabel9.grid(column=0, padx="0 5", row=0, sticky="e")
        ctklabel10 = CTkLabel(framelabeledprimary6)
        ctklabel10.configure(text='subCTk:')
        ctklabel10.grid(column=0, padx="0 5", row=1, sticky="e")
        ctklabel11 = CTkLabel(framelabeledprimary6)
        ctklabel11.configure(text='ctk:')
        ctklabel11.grid(column=0, padx="0 5", pady="20 0", row=2, sticky="e")
        ctklabel12 = CTkLabel(framelabeledprimary6)
        ctklabel12.configure(text='subCTk:')
        ctklabel12.grid(column=0, padx="0 5", row=3, sticky="e")
        self.ctkradiobutton = CTkRadioButton(framelabeledprimary6)
        self.ctkradiobutton.configure(text='ctkradiobutton')
        self.ctkradiobutton.grid(column=1, row=0, sticky="w")
        radiobutton1 = radioButton(framelabeledprimary6)
        radiobutton1.configure(text='subradiobutton')
        radiobutton1.grid(column=1, row=1, sticky="w")
        ctkswitch1 = CTkSwitch(framelabeledprimary6)
        ctkswitch1.configure(text='ctkswitch')
        ctkswitch1.grid(column=1, pady="20 0", row=2, sticky="w")
        switch1 = switch(framelabeledprimary6)
        switch1.configure(text='subswitch')
        switch1.grid(column=1, row=3, sticky="w")
        framelabeledprimary6.grid(
            column=2,
            padx="20 10",
            pady=20,
            row=0,
            sticky="ew")
        framelabeledprimary6.bind("<MouseWheel>", self.callback, add="")
        framelabeledprimary2 = frameLabeledPrimary(ctkframe1)
        framelabeledprimary2.configure(
            label_anchor="w", label_text="Segmented Button")
        ctklabel13 = CTkLabel(framelabeledprimary2)
        ctklabel13.configure(text='ctk:')
        ctklabel13.pack()
        ctksegmentedbutton1 = CTkSegmentedButton(framelabeledprimary2)
        ctksegmentedbutton1.configure(values=["apple", "orange", "pear"])
        ctksegmentedbutton1.pack(side="top")
        ctklabel14 = CTkLabel(framelabeledprimary2)
        ctklabel14.configure(text='subctk:')
        ctklabel14.pack(pady="20 0")
        segmentedbutton1 = segmentedButton(framelabeledprimary2)
        segmentedbutton1.configure(values=["VW", "Audi", "Porsche"])
        segmentedbutton1.pack(side="top")
        framelabeledprimary2.grid(column=0, row=1)
        framelabeledprimary4 = frameLabeledPrimary(ctkframe1)
        framelabeledprimary4.configure(
            label_anchor="w", label_text="textboxes secondary")
        framelabeledprimary4.grid(column=1, row=1)
        framelabeledprimary3 = frameLabeledPrimary(ctkframe1)
        framelabeledprimary3.configure(
            label_anchor="w", label_text="outline frame")
        framelabeledprimary3.grid(column=2, row=1)
        ctkframe1.grid(column=0, row=0)

        # Main widget
        self.mainwindow = ctk1

    def run(self):
        self.mainwindow.mainloop()

    def callback(self, event=None):
        pass


if __name__ == "__main__":
    app = customCTK_WidgetTesterPart2UI()
    app.run()

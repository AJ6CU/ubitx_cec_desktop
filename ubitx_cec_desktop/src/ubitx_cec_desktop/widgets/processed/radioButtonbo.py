#!/usr/bin/python3
"""
radioButton

A custom widget.

UI source file: my_ctk_label.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import CTkRadioButton
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from radioButton import radioButton

from pygubu.plugins.customtkinter import nsctk
from pygubu.plugins.customtkinter.widgets import CTkRadioButtonBO
from pygubu.api.v1 import copy_custom_property


#
# Builder definition section
#
widget_namespace = "radioButton"
widget_classname = "radioButton"
builder_namespace = "custom_widgets"
section_name = "Project Widgets"


class radioButtonBO(CTkRadioButtonBO):
    class_ = radioButton

    def code_imports(self):
        # should return an iterable of (module, classname/function) to import
        # or None
        imports = [(widget_namespace, widget_classname)]
        imports.extend(self.code_extra_imports())
        return imports



builder_id = f"{builder_namespace}.{widget_classname}"
register_widget(
    builder_id, radioButtonBO, widget_classname, ("ttk", section_name)
)

# Copy properties before we define our own properties.
#
# nsctk is the customtkinter plugin namespace
# nsctk.CTkRadioButton is the registered name for CTkRadioButtonBO builder.
for pname in CTkRadioButtonBO.properties:
    copy_custom_property(nsctk.CTkRadioButton, pname, builder_id)

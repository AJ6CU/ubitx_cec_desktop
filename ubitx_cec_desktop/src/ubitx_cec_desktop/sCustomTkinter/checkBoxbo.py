#!/usr/bin/python3
"""
checkBox

A custom widget.

UI source file: my_ctk_label.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import CTkCheckBox
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from checkBox import checkBox

from pygubu.plugins.customtkinter import nsctk
from pygubu.plugins.customtkinter.widgets import CTkCheckBoxBO
from pygubu.api.v1 import copy_custom_property


#
# Builder definition section
#
widget_namespace = "checkBox"
widget_classname = "checkBox"
builder_namespace = "custom_widgets"
section_name = "Project Widgets"


class checkBoxBO(CTkCheckBoxBO):
    class_ = checkBox

    def code_imports(self):
        # should return an iterable of (module, classname/function) to import
        # or None
        imports = [(widget_namespace, widget_classname)]
        imports.extend(self.code_extra_imports())
        return imports



builder_id = f"{builder_namespace}.{widget_classname}"
register_widget(
    builder_id, checkBoxBO, widget_classname, ("ttk", section_name)
)

# Copy properties before we define our own properties.
#
# nsctk is the customtkinter plugin namespace
# nsctk.CTkCheckBox is the registered name for CTkCheckBoxBO builder.
for pname in CTkCheckBoxBO.properties:
    copy_custom_property(nsctk.CTkCheckBox, pname, builder_id)

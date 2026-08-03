#!/usr/bin/python3
"""
buttonPrimary

A custom widget.

UI source file: my_ctk_label.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import CTkButton
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from buttonPrimary import buttonPrimary

from pygubu.plugins.customtkinter import nsctk
from pygubu.plugins.customtkinter.widgets import CTkButtonBO
from pygubu.api.v1 import copy_custom_property


#
# Builder definition section
#
widget_namespace = "buttonPrimary"
widget_classname = "buttonPrimary"
builder_namespace = "custom_widgets"
section_name = "Project Widgets"


class buttonPrimaryBO(CTkButtonBO):
    class_ = buttonPrimary

    def code_imports(self):
        # should return an iterable of (module, classname/function) to import
        # or None
        imports = [(widget_namespace, widget_classname)]
        imports.extend(self.code_extra_imports())
        return imports



builder_id = f"{builder_namespace}.{widget_classname}"
register_widget(
    builder_id, buttonPrimaryBO, widget_classname, ("ttk", section_name)
)

# Copy properties before we define our own properties.
#
# nsctk is the customtkinter plugin namespace
# nsctk.CTkButton is the registered name for CTkButtonBO builder.
for pname in CTkButtonBO.properties:
    copy_custom_property(nsctk.CTkButton, pname, builder_id)

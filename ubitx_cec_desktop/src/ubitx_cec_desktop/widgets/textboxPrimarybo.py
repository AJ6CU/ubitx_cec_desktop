#!/usr/bin/python3
"""
textboxPrimary

A custom widget.

UI source file: my_ctk_label.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import CTkLabel
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from textboxPrimary import textboxPrimary

from pygubu.plugins.customtkinter import nsctk
from pygubu.plugins.customtkinter.widgets import CTkTextboxBO
from pygubu.api.v1 import copy_custom_property


#
# Builder definition section
#
widget_namespace = "textboxPrimary"
widget_classname = "textboxPrimary"
builder_namespace = "custom_widgets"
section_name = "Project Widgets"


class textboxPrimaryBO(CTkTextboxBO):
    class_ = textboxPrimary

    def code_imports(self):
        # should return an iterable of (module, classname/function) to import
        # or None
        imports = [(widget_namespace, widget_classname)]
        imports.extend(self.code_extra_imports())
        return imports


builder_id = f"{builder_namespace}.{widget_classname}"
register_widget(
    builder_id, textboxPrimaryBO, widget_classname, ("ttk", section_name)
)

# Copy properties before we define our own properties.
#
# nsctk is the customtkinter plugin namespace
# nsctk.CTkLabel is the registered name for BO builder.
for pname in CTkTextboxBO.properties:
    copy_custom_property(nsctk.CTkLabel, pname, builder_id)

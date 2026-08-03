#!/usr/bin/python3
"""
progressBar

A custom widget.

UI source file: my_ctk_label.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import CTkProgressBar
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from progressBar import progressBar

from pygubu.plugins.customtkinter import nsctk
from pygubu.plugins.customtkinter.widgets import CTkProgressBarBO
from pygubu.api.v1 import copy_custom_property


#
# Builder definition section
#
widget_namespace = "progressBar"
widget_classname = "progressBar"
builder_namespace = "custom_widgets"
section_name = "Project Widgets"


class progressBarBO(CTkProgressBarBO):
    class_ = progressBar

    def code_imports(self):
        # should return an iterable of (module, classname/function) to import
        # or None
        imports = [(widget_namespace, widget_classname)]
        imports.extend(self.code_extra_imports())
        return imports



builder_id = f"{builder_namespace}.{widget_classname}"
register_widget(
    builder_id, progressBarBO, widget_classname, ("ttk", section_name)
)

# Copy properties before we define our own properties.
#
# nsctk is the customtkinter plugin namespace
# nsctk.CTkProgressBar is the registered name for CTkProgressBarBO builder.
for pname in CTkProgressBarBO.properties:
    copy_custom_property(nsctk.CTkProgressBar, pname, builder_id)

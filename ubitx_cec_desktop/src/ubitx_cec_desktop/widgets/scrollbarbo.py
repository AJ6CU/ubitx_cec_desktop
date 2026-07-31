#!/usr/bin/python3
"""
scrollbar

A custom widget.

UI source file: my_ctk_label.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import CTkScrollbar
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from scrollbar import scrollbar

from pygubu.plugins.customtkinter import nsctk
from pygubu.plugins.customtkinter.widgets import CTkScrollbarBO
from pygubu.api.v1 import copy_custom_property


#
# Builder definition section
#
widget_namespace = "scrollbar"
widget_classname = "scrollbar"
builder_namespace = "custom_widgets"
section_name = "Project Widgets"


class scrollbarBO(CTkScrollbarBO):
    class_ = scrollbar

    def code_imports(self):
        # should return an iterable of (module, classname/function) to import
        # or None
        imports = [(widget_namespace, widget_classname)]
        imports.extend(self.code_extra_imports())
        return imports



builder_id = f"{builder_namespace}.{widget_classname}"
register_widget(
    builder_id, scrollbarBO, widget_classname, ("ttk", section_name)
)

# Copy properties before we define our own properties.
#
# nsctk is the customtkinter plugin namespace
# nsctk.CTkScrollbar is the registered name for CTkScrollbarBO builder.
for pname in CTkScrollbarBO.properties:
    copy_custom_property(nsctk.CTkScrollbar, pname, builder_id)

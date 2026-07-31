#!/usr/bin/python3
"""
canvas

A custom widget.

UI source file: my_ctk_label.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import CTkCanvas
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from canvas import canvas

from pygubu.plugins.customtkinter import nsctk
from pygubu.plugins.customtkinter.widgets import CTkCanvasBO
from pygubu.api.v1 import copy_custom_property


#
# Builder definition section
#
widget_namespace = "canvas"
widget_classname = "canvas"
builder_namespace = "custom_widgets"
section_name = "Project Widgets"


class canvasBO(CTkCanvasBO):
    class_ = canvas

    def code_imports(self):
        # should return an iterable of (module, classname/function) to import
        # or None
        imports = [(widget_namespace, widget_classname)]
        imports.extend(self.code_extra_imports())
        return imports



builder_id = f"{builder_namespace}.{widget_classname}"
register_widget(
    builder_id, canvasBO, widget_classname, ("ttk", section_name)
)

# Copy properties before we define our own properties.
#
# nsctk is the customtkinter plugin namespace
# nsctk.CTkCanvas is the registered name for CTkCanvasBO builder.
for pname in CTkCanvasBO.properties:
    copy_custom_property(nsctk.CTkCanvas, pname, builder_id)

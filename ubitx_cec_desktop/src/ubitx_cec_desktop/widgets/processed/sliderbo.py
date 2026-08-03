#!/usr/bin/python3
"""
slider

A custom widget.

UI source file: my_ctk_label.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import CTkSlider
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from slider import slider

from pygubu.plugins.customtkinter import nsctk
from pygubu.plugins.customtkinter.widgets import CTkSliderBO
from pygubu.api.v1 import copy_custom_property


#
# Builder definition section
#
widget_namespace = "slider"
widget_classname = "slider"
builder_namespace = "custom_widgets"
section_name = "Project Widgets"


class sliderBO(CTkSliderBO):
    class_ = slider

    def code_imports(self):
        # should return an iterable of (module, classname/function) to import
        # or None
        imports = [(widget_namespace, widget_classname)]
        imports.extend(self.code_extra_imports())
        return imports



builder_id = f"{builder_namespace}.{widget_classname}"
register_widget(
    builder_id, sliderBO, widget_classname, ("ttk", section_name)
)

# Copy properties before we define our own properties.
#
# nsctk is the customtkinter plugin namespace
# nsctk.CTkSlider is the registered name for CTkSliderBO builder.
for pname in CTkSliderBO.properties:
    copy_custom_property(nsctk.CTkSlider, pname, builder_id)

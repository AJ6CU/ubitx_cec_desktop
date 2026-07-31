#!/usr/bin/python3
"""
tabview

A custom widget.

UI source file: my_ctk_label.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import CTkTabview
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from tabview import tabview

from pygubu.plugins.customtkinter import nsctk
from pygubu.plugins.customtkinter.tabview import CTkTabviewBO
from pygubu.api.v1 import copy_custom_property


#
# Builder definition section
#
widget_namespace = "tabview"
widget_classname = "tabview"
builder_namespace = "custom_widgets"
section_name = "Project Widgets"


class tabviewBO(CTkTabviewBO):
    class_ = tabview

    def code_imports(self):
        # should return an iterable of (module, classname/function) to import
        # or None
        imports = [(widget_namespace, widget_classname)]
        imports.extend(self.code_extra_imports())
        return imports



builder_id = f"{builder_namespace}.{widget_classname}"
register_widget(
    builder_id, tabviewBO, widget_classname, ("ttk", section_name)
)

# Copy properties before we define our own properties.
#
# nsctk is the customtkinter plugin namespace
# nsctk.CTkTabview is the registered name for CTkTabviewBO builder.
for pname in CTkTabviewBO.properties:
    copy_custom_property(nsctk.CTkTabview, pname, builder_id)

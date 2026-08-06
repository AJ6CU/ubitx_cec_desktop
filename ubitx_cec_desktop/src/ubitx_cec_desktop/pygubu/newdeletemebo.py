#!/usr/bin/python3
"""
newdeleteme

newdeleteme

UI source file: newdeleteme.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import (CTkLabel, CTkProgressBar, CTkToplevel)
from sCTkDialog import sCTkDialog
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from newdeleteme import newdeleteme


#
# Builder definition section
#
widget_namespace = "newdeleteme"
widget_classname = "newdeleteme"
builder_namespace = "custom_widgets"
section_name = "Project Widgets"


class newdeletemeBO(BuilderObject):
    class_ = newdeleteme

    def code_imports(self):
        # should return an iterable of (module, classname/function) to import
        # or None
        return [(widget_namespace, widget_classname)]


builder_id = f"{builder_namespace}.{widget_classname}"
register_widget(
    builder_id, newdeletemeBO, widget_classname, ("ttk", section_name)
)

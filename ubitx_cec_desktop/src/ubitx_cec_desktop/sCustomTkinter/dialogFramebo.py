#!/usr/bin/python3
"""
dialogCommand

test

UI source file: dialogCommand.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import (CTkEntry, CTkLabel)
from dialogBase import dialogBase
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from dialogFrame import dialogFrame


#
# Builder definition section
#
widget_namespace = "dialogFrame"
widget_classname = "dialogFrame"
builder_namespace = "custom_widgets"
section_name = "Project Widgets"


class dialogFrameBO(BuilderObject):
    class_ = dialogFrame

    def code_imports(self):
        # should return an iterable of (module, classname/function) to import
        # or None
        return [(widget_namespace, widget_classname)]


builder_id = f"{builder_namespace}.{widget_classname}"
register_widget(
    builder_id, dialogFrameBO, widget_classname, ("ttk", section_name)
)

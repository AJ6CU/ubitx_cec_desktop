#!/usr/bin/python3
"""
generalSettings_sCTk

first try at settings dialog

UI source file: generalSettings_sCTk.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from sCTkDialogCore import sCTkDialogCore
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from generalSettings_sCTk import generalSettings_sCTk


#
# Builder definition section
#
widget_namespace = "generalSettings_sCTk"
widget_classname = "generalSettings_sCTk"
builder_namespace = "custom_widgets"
section_name = "Project Widgets"


class generalSettings_sCTkBO(BuilderObject):
    class_ = generalSettings_sCTk

    def code_imports(self):
        # should return an iterable of (module, classname/function) to import
        # or None
        return [(widget_namespace, widget_classname)]


builder_id = f"{builder_namespace}.{widget_classname}"
register_widget(
    builder_id, generalSettings_sCTkBO, widget_classname, ("ttk", section_name)
)

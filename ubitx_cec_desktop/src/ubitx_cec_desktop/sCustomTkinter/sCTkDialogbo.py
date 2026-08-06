#!/usr/bin/python3
"""
sCTkDialog

a special widget deciated to making popup dialogs consistent

UI source file: sCTkDialog.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import CTkToplevel
from sCTkButtonPrimary import sCTkButtonPrimary
from sCTkButtonSecondary import sCTkButtonSecondary
from sCTkFrame import sCTkFrame
from sCTkLabelPrimary import sCTkLabelPrimary
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
# from pygubu.builders.toplevel import ToplevelPreviewBuilder
from sCTkDialog import sCTkDialog


#
# Builder definition section
#
widget_namespace = "sCTkDialog"
widget_classname = "sCTkDialog"
builder_namespace = "custom_widgets"
section_name = "Project Widgets"


class sCTkDialogBO(BuilderObject):
    class_ = sCTkDialog

    container = True


    def code_imports(self):
        # should return an iterable of (module, classname/function) to import
        # or None
        return [(widget_namespace, widget_classname)]

    # 1. Force Pygubu to cleanly build your widget before handling children
    def realize(self, parent, extra_init_args: dict = None):
        # Call the base class builder setup
        self.widget = super().realize(parent, extra_init_args)
        return self.widget

    # 2. Pygubu calls this to get the container target
    def get_child_master(self):
        # Double check that contentFrame exists on the live widget object
        if hasattr(self.widget, 'contentFrame'):
            return self.widget.contentFrame

        # Safe fallback to prevent canvas rendering crashes
        return self.widget


builder_id = f"{builder_namespace}.{widget_classname}"
register_widget(
    builder_id, sCTkDialogBO, widget_classname, ("ttk", section_name)
)

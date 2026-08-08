#!/usr/bin/python3
"""
sCTkDialog

a special widget deciated to making popup dialogs consistent

UI source file: dialogBase.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from sCTkButtonPrimary import sCTkButtonPrimary
from sCTkButtonSecondary import sCTkButtonSecondary
from sCTkFrame import sCTkFrame
from sCTkLabelPrimary import sCTkLabelPrimary
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from dialogBase import dialogBase


#
# Builder definition section
#
widget_namespace = "dialogBase"
widget_classname = "dialogBase"
builder_namespace = "custom_widgets"
section_name = "sCustomTkinter"


class dialogBaseBO(BuilderObject):
    class_ = dialogBase
    container = True

    def get_child_master(self):
        return self.widget.contentFrame

    def code_child_master(self):
        return f"{self.code_identifier()}.contentFrame"

    def code_imports(self):
        # should return an iterable of (module, classname/function) to import
        # or None
        return [(widget_namespace, widget_classname)]



    def code_imports(self):
        # should return an iterable of (module, classname/function) to import
        # or None
        return [(widget_namespace, widget_classname)]


builder_id = f"{builder_namespace}.{widget_classname}"
register_widget(
    builder_id, dialogBaseBO, widget_classname, ("ttk", section_name)
)

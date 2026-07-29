#!/usr/bin/python3
"""
optionMenuPrimary

Tailored version of the standard ctkOptionMenu

UI source file: optionMenuPrimary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import CTkOptionMenu
from pygubu.api.v1 import (
    BuilderObject,
    register_widget, register_custom_property
)
from optionMenuPrimary import optionMenuPrimary


#
# Builder definition section
#
widget_namespace = "optionMenuPrimary"
widget_classname = "optionMenuPrimary"
builder_namespace = "custom_widgets"
section_name = "Project Widgets"


class optionMenuPrimaryBO(BuilderObject):
    class_ = optionMenuPrimary
    OPTIONS_CUSTOM = {
        "command",
        "state",
        "variable",
        "height",
        "width"
    }
    command_properties = ("command",)
    properties = OPTIONS_CUSTOM

    def _process_property_value(self, pname, value):
        if pname in ("height", "width"):
            return int(value)
        return super()._process_property_value(pname, value)

    def code_imports(self):
        # should return an iterable of (module, classname/function) to import
        # or None
        return [(widget_namespace, widget_classname)]

    def _can_set_tcl_widget_name(self) -> bool:
        """Returns True if widget accepts the tcl "name" init argument."""
        return False


builder_id = f"{builder_namespace}.{widget_classname}"
register_widget(
    builder_id, optionMenuPrimaryBO, widget_classname, ("ttk", section_name)
)

register_custom_property (
    builder_id,
    "command",
    "commandentry"
)

register_custom_property (
    builder_id,
    "state",
    "choice",
    values=("normal", "disabled")
)


register_custom_property (
    builder_id,
    "variable",
    "tkvarentry"
)

register_custom_property (
    builder_id,
    "height",
    "integernumber"
)
register_custom_property (
    builder_id,
    "width",
    "integernumber"
)

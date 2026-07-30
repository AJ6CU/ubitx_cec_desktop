#!/usr/bin/python3
"""
buttonPrimary

primary button

UI source file: buttonPrimary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import CTkButton
from pygubu.api.v1 import (
    BuilderObject,
    register_widget, register_custom_property
)
from buttonPrimary import buttonPrimary


#
# Builder definition section
#
widget_namespace = "buttonPrimary"
widget_classname = "buttonPrimary"
builder_namespace = "custom_widgets"
section_name = "Project Widgets"


class buttonPrimaryBO(BuilderObject):
    class_ = buttonPrimary
    OPTIONS_CUSTOM = {
        "anchor",
        "image",
        "command",
        "state",
        "text",
        "textvariable",
        "height",
        "width",
    }
    command_properties = ("command",)
    properties = OPTIONS_CUSTOM

    # virtual_events = ("<<primaryButtonSelected>>",)

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
    builder_id, buttonPrimaryBO, widget_classname, ("ttk", section_name)
)

register_custom_property (
    builder_id,
    "anchor",
    "choice",
    values=("n", "ne", "nw", "e", "w", "s", "se", "sw",  "center"),
)

register_custom_property (
    builder_id,
    "image",
    "imageentry"
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
    "text",
    "entry"
)

register_custom_property (
    builder_id,
    "textvariable",
    "tkvarentry"
)

register_custom_property (
    builder_id,
    "height",
    "naturalnumber"
)

register_custom_property (
    builder_id,
    "width",
    "naturalnumber"
)

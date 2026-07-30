#!/usr/bin/python3
"""
labelTertiary

3rd level Label used for notes

UI source file: labelTertiary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import CTkLabel
from pygubu.api.v1 import (
    BuilderObject,
    register_widget, register_custom_property
)
from labelTertiary import labelTertiary


#
# Builder definition section
#
widget_namespace = "labelTertiary"
widget_classname = "labelTertiary"
builder_namespace = "custom_widgets"
section_name = "Project Widgets"


class labelTertiaryBO(BuilderObject):
    class_ = labelTertiary
    OPTIONS_CUSTOM = {
        "anchor",
        "image",
        "state",
        "justify",
        "padx",
        "pady",
        "takefocus",
        "text",
        "textvariable",
        "height",
        "width"
    }
    properties = OPTIONS_CUSTOM

    def _process_property_value(self, pname, value):
        if pname in ("height", "width", "padx", "pady"):
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
    builder_id, labelTertiaryBO, widget_classname, ("ttk", section_name)
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
    "state",
    "choice",
    values=("normal", "disabled")
)

register_custom_property (
    builder_id,
    "justify",
    "choice",
    values=("", "left", "center", "right"),
)

register_custom_property (
    builder_id,
    "padx",
    "naturalnumber"
)

register_custom_property (
    builder_id,
    "pady",
    "naturalnumber"
)

register_custom_property (
    builder_id,
    "takefocus",
    "choice",
    values=("false", "true")
)

register_custom_property (
    builder_id,
    "text",
    "text"
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

#!/usr/bin/python3
"""
frameLabeledPrimary

Similer to ttk.labelframe built on ctkscrollableframe with scrollbars hidden

UI source file: frameLabeledSecondary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import CTkScrollableFrame
from pygubu.api.v1 import (
    BuilderObject,
    register_widget, register_custom_property
)
from frameLabeledSecondary import frameLabeledSecondary


#
# Builder definition section
#
widget_namespace = "frameLabeledSecondary"
widget_classname = "frameLabeledSecondary"
builder_namespace = "custom_widgets"
section_name = "Project Widgets"


class frameLabeledSecondaryBO(BuilderObject):
    class_ = frameLabeledSecondary
    container = True
    # CTkScrollableFrame does some weird things
    # with layout so I disable container layout here on purpose.
    container_layout = False

    OPTIONS_CUSTOM = {
        "label_anchor",
        "label_text",
        "border_color",
        "border_width",
        "fg_color",
        "height",
        "width",
    }

    properties = OPTIONS_CUSTOM

    def _process_property_value(self, pname, value):
        if pname in ("height", "width", "border_width"):
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
    builder_id, frameLabeledSecondaryBO, widget_classname, (
        "ttk", section_name)
)

register_custom_property (
    builder_id,
    "label_anchor",
    "choice",
    values=("n", "ne", "nw", "e", "w", "s", "se", "sw",  "center"),
)

register_custom_property (
    builder_id,
    "label_text",
    "entry"
)

register_custom_property (
    builder_id,
    "border_width",
    "naturalnumber"
)

register_custom_property (
    builder_id,
    "border_color",
    "colorentry"
)

register_custom_property (
    builder_id,
    "fg_color",
    "colorentry"
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

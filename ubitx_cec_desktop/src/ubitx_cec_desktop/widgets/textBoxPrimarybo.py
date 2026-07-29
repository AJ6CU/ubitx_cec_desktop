#!/usr/bin/python3
"""
frameLabeledPrimary

Similer to ttk.labelframe built on ctkscrollableframe with scrollbars hidden

UI source file: textBoxPrimary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import CTkTextbox
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,register_custom_property
)
from textBoxPrimary import textBoxPrimary


#
# Builder definition section
#
widget_namespace = "textBoxPrimary"
widget_classname = "textBoxPrimary"
builder_namespace = "custom_widgets"
section_name = "Project Widgets"


class textBoxPrimaryBO(BuilderObject):
    class_ = textBoxPrimary
    OPTIONS_CUSTOM = {
        "activate_scrollbars",
        "autoseparators",
        "bg_color",
        "border_spacing",
        "border_width",
        "border_color"
        "border_width",
        "corner_radius",
        "cursor",
        "exportselection",
        "fg_color",
        "font",
        "height",
        "insertborderwidth"
        "insertofftime",
        "insertwidth",
        "maxundo",
        "padx",
        "pady",
        "scrollbar_button_color",
        "scrollbar_button_hover_color,
        "selectborderwidth",
        "spacing1",
        "spacing2",
        "spacing3",
        "state",
        "tabs",
        "takefocus",
        "text",
        "text_color",
        "undo",
        "width",
        "wrap"
    }


    properties = OPTIONS_CUSTOM

    def _process_property_value(self, pname, value):
        if pname in ("height", "width", border_spacing,):
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
    builder_id, textBoxPrimaryBO, widget_classname, ("ttk", section_name)
)

register_custom_property (
    builder_id,
    "activate_scrollbars",
    "choice",
    values=("","True", "False")
)

register_custom_property (
    builder_id,
    "autoseparators",
    "choice",
    values=("","false", "true")
)

register_custom_property (
    builder_id,
    "state",
    "choice",
    values=("normal", "disabled")
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

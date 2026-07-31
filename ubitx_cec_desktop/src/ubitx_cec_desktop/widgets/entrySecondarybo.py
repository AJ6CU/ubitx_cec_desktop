#!/usr/bin/python3
"""
entrySecondary

Customized ctk Entry field. - Secondary version

UI source file: entrySecondary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import CTkEntry
from pygubu.api.v1 import (
    BuilderObject,
    register_widget, register_custom_property
)
from entrySecondary import entrySecondary


#
# Builder definition section
#
widget_namespace = "entrySecondary"
widget_classname = "entrySecondary"
builder_namespace = "custom_widgets"
section_name = "Project Widgets"


class entrySecondaryBO(BuilderObject):
    class_ = entrySecondary
    OPTIONS_CUSTOM = {
        "bg_color",
        "border_color",
        "border_width",
        "corner_radius",
        "cursor",
        "exportselection",
        "fg_color",
        "font",
        "height",
        "insertborderwidth",
        "insertofftime",
        "insertontime",
        "insertwidth",
        "justify",
        "placeholder_text",
        "placeholder_text_color",
        "readonlybackground",
        "selectborderwidth",
        "show",
        "state",
        "takefocus",
        "text",
        "text_color",
        "textvariable",
        "width",
        "xscrollcommand"
    }
    command_properties = ("xscrollcommand")
    properties = OPTIONS_CUSTOM

    def _process_property_value(self, pname, value):
        if pname in ("height", "width", "border_width", "corner_radius"):
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
    builder_id, entrySecondaryBO, widget_classname, ("ttk", section_name)
)


register_custom_property (
    builder_id,
    "bg_color",
    "colorentry"
)

register_custom_property (
    builder_id,
    "border_color",
    "colorentry"
)

register_custom_property (
    builder_id,
    "border_width",
    "naturalnumber"
)

register_custom_property (
    builder_id,
    "corner_radius",
    "naturalnumber"
)

register_custom_property (            # rejected by pygubu-designer
    builder_id,
    "cursor",
    "choice",
        values= (                   # pygubu-designer rejected the cursor property
            "arrow", "clock", "cross", "hand1", "hand2",
            "heart", "pencil", "sieve", "watch", "xterm"
        )
)

register_custom_property (
    builder_id,
    "exportselection",
    "choice",
    values=("","true", "false")
)

register_custom_property (
    builder_id,
    "fg_color",
    "colorentry"
)

register_custom_property (
    builder_id,
    "font",
    "fontentry"
)

register_custom_property (                # rejected by pygubu-designer
    builder_id,
    "insertborderwidth",
    "spinbox",
"0",                # The default initialization string
    values=tuple(str(x) for x in range(0, 21, 1))
# values=tuple(str(x) for x in range(0, 1000, 1))
)

register_custom_property (
    builder_id,
    "insertofftime",
    "spinbox",
"0",                # The default initialization string
    values=tuple(str(x) for x in range(0, 5000, 500)) # Passes the clean, sequentially scrollable numbers
# values=tuple(str(x) for x in range(0, 10000, 100)) # Passes the clean, sequentially scrollable numbers
)

register_custom_property(
    builder_id,
    "insertontime",
    "spinbox",          # Pygubu renders the field with spin up/down buttons
    "0",                # The default initialization string
    values=tuple(str(x) for x in range(0, 5000, 500)) # Passes the clean, sequentially scrollable numbers
# values=tuple(str(x) for x in range(0, 10000, 100)) # Passes the clean, sequentially scrollable numbers
)


register_custom_property (
    builder_id,
    "insertwidth",
    "spinbox",
"0",                # The default initialization string
    values=tuple(str(x) for x in range(0, 50, 1))
# values=tuple(str(x) for x in range(0, 1000, 1))
)


register_custom_property (
    builder_id,
    "justify",
    "choice",
    values=("left", "center", "right"),
)

register_custom_property (
    builder_id,
    "placeholder_text",
    "entry"
)

register_custom_property (
    builder_id,
    "placeholder_text_color",
    "colorentry"
)

register_custom_property (
    builder_id,
    "readonlybackground",
    "colorentry"
)

register_custom_property (
    builder_id,
    "selectborderwidth",
    "spinbox",
"0",                # The default initialization string
    values=tuple(str(x) for x in range(0, 50, 1))
# values=tuple(str(x) for x in range(0, 1000, 1))
)


register_custom_property(
    builder_id,
    "show",
    "entry",
    "",
)  # For passwords (e.g., "*")

register_custom_property (
    builder_id,
    "state",
    "choice",
    values=("normal", "disabled")
)


register_custom_property (
    builder_id,
    "takefocus",
    "choice",
    values=("","false", "true")
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
    "text_color",
    "colorentry"
)



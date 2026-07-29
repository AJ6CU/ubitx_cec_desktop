#!/usr/bin/python3
"""
entryPrimary

Customized ctk Entry field. - Primary version

UI source file: entryPrimary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import CTkEntry
from pygubu.api.v1 import (
    BuilderObject,
    register_widget, register_custom_property
)
from entryPrimary import entryPrimary


#
# Builder definition section
#
widget_namespace = "entryPrimary"
widget_classname = "entryPrimary"
builder_namespace = "custom_widgets"
section_name = "Project Widgets"


class entryPrimaryBO(BuilderObject):
    class_ = entryPrimary

    OPTIONS_CUSTOM = {
        "justify",
        "placeholder_text",
        "state",
        "textvariable",

        "height",
        "width",
    }

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
    builder_id, entryPrimaryBO, widget_classname, ("ttk", section_name)
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
    "state",
    "choice",
    values=("normal", "disabled")
)

register_custom_property (
    builder_id,
    "textvariable",
    "tkvarentry"
)

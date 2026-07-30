#!/usr/bin/python3
"""
textBoxSecondary

Similer to ttk.labelframe built on ctkscrollableframe with scrollbars hidden. This textBox is typically used for user information or explanations as there is no border and the font is smaller.

UI source file: textBoxSecondary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import CTkTextbox
from pygubu.api.v1 import (
    BuilderObject,
    register_widget, register_custom_property
)
from textBoxSecondary import textBoxSecondary


#
# Builder definition section
#
widget_namespace = "textBoxSecondary"
widget_classname = "textBoxSecondary"
builder_namespace = "custom_widgets"
section_name = "Project Widgets"

CTK_CURSORS = [
    "arrow", "clock", "cross", "hand1", "hand2",
    "heart", "pencil", "sieve", "watch", "xterm"
]


class textBoxSecondaryBO(BuilderObject):
    class_ = textBoxSecondary
    OPTIONS_CUSTOM = {
        "activate_scrollbars",
        "autoseparators",
        "bg_color",
        "border_spacing",
        "border_width",
        "border_color",
        "corner_radius",
        # "cursor"                      # rejected by pygubu designer
        "exportselection",
        "fg_color",
        "font",
        "height",
        # "insertborderwidth"           # rejected by pygubu-designer
        "insertofftime",
        "insertontime",
        "insertwidth",
        "maxundo",
        "padx",
        "pady",
        "scrollbar_button_color",
        "scrollbar_button_hover_color",
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
        if pname in ("height", "width", "border_spacing", "border_width", "corner_radius", "maxundo",
                     "padx", "pady", "spacing1", "spacing2", "spacing3"):
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
    builder_id, textBoxSecondaryBO, widget_classname, ("ttk", section_name)
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
    "border_spacing",
    "naturalnumber"
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


# register_custom_property (            # rejected by pygubu-designer
#     builder_id,
#     "cursor",
#     "choice",
#         values= CTK_CURSORS
# )


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

register_custom_property (
    builder_id,
    "height",
    "naturalnumber"
)


# register_custom_property (                # rejected by pygubu-designer
#     builder_id,
#     "insertborderwidth",
#     "spinbox",
# "0",                # The default initialization string
#     values=tuple(str(x) for x in range(0, 21, 1))
# # values=tuple(str(x) for x in range(0, 1000, 1))
# )


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
    "maxundo",
    "naturalnumber"
)

register_custom_property (
    builder_id,
    "padx",
    "naturalnumber"
)

register_custom_property (
    builder_id,"pady",
    "naturalnumber"
)

register_custom_property (
    builder_id,
    "scrollbar_button_color",
    "colorentry"
)

register_custom_property (
    builder_id,
    "scrollbar_button_hover_color",
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

register_custom_property (
    builder_id,"spacing1",
    "naturalnumber"
)

register_custom_property (
    builder_id,"spacing2",
    "naturalnumber"
)

register_custom_property (
    builder_id,"spacing3",
    "naturalnumber"
)

register_custom_property (
    builder_id,
    "state",
    "choice",
    values=("normal", "disabled")
)

register_custom_property (
    builder_id,
    "tabs",
    "entry"
)

register_custom_property (
    builder_id,
    "text",
    "text"
)

register_custom_property (
    builder_id,
    "text_color",
    "colorentry"
)

register_custom_property (
    builder_id,
    "undo",
    "choice",
    values=("","false", "true")
)

register_custom_property (
    builder_id,
    "width",
    "naturalnumber"
)


register_custom_property (
    builder_id,
    "width",
    "naturalnumber"
)

register_custom_property (
    builder_id,
    "undo",
    "choice",
    values=("","char", "word", "none")
)
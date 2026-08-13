#!/usr/bin/python3
"""
sCTkSeparatorBuilder

Pygubu Builder Object for the custom themeable sCTkSeparator widget line.
"""
import pygubu

from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property
)

# Import the native custom class
from sCTkSeparator import sCTkSeparator

#
# Builder definition section
#
widget_namespace = "sCTkSeparator"
widget_classname = "sCTkSeparator"
builder_namespace = "custom_widgets"
section_name = "sCustomTkinter"


class sCTkSeparatorBuilder(BuilderObject):
    class_ = sCTkSeparator

    # Expose custom structural separator attributes
    OPTIONS_CUSTOM = ("length", "width", "corner_radius", "orientation", "bg_color", "fg_color")
    properties = OPTIONS_CUSTOM

    def _process_property_value(self, pname, value):
        """Passes values directly to allow core widget validations to handle exceptions."""
        return super()._process_property_value(pname, value)


# Register the widget into Pygubu's parsing engine
builder_id = f"{builder_namespace}.{widget_classname}"

register_widget(builder_id, sCTkSeparatorBuilder, 'sCTkSeparator', ("ttk", section_name))


# Register custom attribute fields to display inside the Designer properties panel

register_custom_property(
    builder_id,
    "length",
    "naturalnumber",
    help="Set total span length of the separator line in pixels"
)

register_custom_property(
    builder_id,
    "width",
    "naturalnumber",
    help="Set visual thickness profile width of the separator line in pixels"
)

register_custom_property(
    builder_id,
    "corner_radius",
    "naturalnumber",
    help="Define roundness sharpness limit token value for divider tips"
)

register_custom_property(
    builder_id,
    "orientation",
    "choice",
    values=("", "vertical", "horizontal"),
    state="readonly",
    help="Select spatial directional positioning alignment"
)

register_custom_property(
    builder_id,
    "bg_color",
    "color",
    help="Override background mask field token color (defaults to transparent)"
)

register_custom_property(
    builder_id,
    "fg_color",
    "color",
    help="Override line paint stroke color (defaults onto master sCTkFrame styles)"
)

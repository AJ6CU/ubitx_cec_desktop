#!/usr/bin/python3
"""
sCTkSMeter.py

Pygubu Builder Object for a S Meter.
"""
import ast
import pygubu

from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property
)

# Import the native custom class
from sCTkSMeter import sCTkSMeter


#
# Builder definition section
#
widget_namespace = "sCTkSMeter"
widget_classname = "sCTkSMeter"
builder_namespace = "custom_widgets"
section_name = "sCustomTkinter"


class sCTkSMeterBO(BuilderObject):
    class_ = sCTkSMeter

    # Expose custom compound parameters alongside theme state configurations
    OPTIONS_CUSTOM = ("width", "height", "sig_min_value", "sig_max_value")
    properties = OPTIONS_CUSTOM

    def _process_property_value(self, pname, value):
        if pname in ("width", "height", "sig_min_value", "sig_max_value"):
            return int(value)
        return super()._process_property_value(pname, value)


# Register the widget into Pygubu's parsing engine
builder_id = f"{builder_namespace}.{widget_classname}"

register_widget(builder_id, sCTkSMeterBO, 'sCTkSMeter', ("ttk", section_name))



# Register custom attribute fields to display inside the Designer properties panel

register_custom_property(
    builder_id,
    "width",
    "naturalnumber",
    help="Set total width in pixels of the meter"
)

register_custom_property(
    builder_id,
    "height",
    "naturalnumber",
    help="Set height in pixels of the meter"
)


register_custom_property(
    builder_id,
    "sig_min_value",
    "integernumber",default_value=0,
    help="Smallest value for signal on scale"
)

register_custom_property(
    builder_id,
    "sig_max_value",
    "integernumber",default_value=60,
    help="largest value for signal on scale"
)


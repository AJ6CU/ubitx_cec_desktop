#!/usr/bin/python3
"""
sCTkSeparatorBuilder

Pygubu Builder Object for the custom themeable sCTkSeparator widget line.
"""
# import pygubu
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property
)
from pygubu.plugins.customtkinter.widgets import CTkCanvasBO
# from pygubu.plugins.customtkinter import nsctk
# from pygubu.api.v1 import copy_custom_property

# Import the native custom class
from sCTkSeparator import sCTkSeparator

#
# Builder definition section
#
widget_namespace = "sCTkSeparator"
widget_classname = "sCTkSeparator"
builder_namespace = "sCTkSeparator"
section_name = "sCustomTkinter"


class sCTkSeparatorBuilder(CTkCanvasBO):
    class_ = sCTkSeparator

    OPTIONS_CUSTOM = ("length", "width", "corner_radius", "orientation")
    properties = OPTIONS_CUSTOM

    def realize(self, parent, extra_init_args: dict = None):
        """Constructs our custom class safely using extracted parameter inputs."""
        args = self._get_init_args(extra_init_args)

        length = int(args.get("length", 100)) if args.get("length") else 100
        width = int(args.get("width", 4)) if args.get("width") else 4
        corner_radius = int(args.get("corner_radius")) if args.get("corner_radius") else None
        orientation = args.get("orientation", "vertical") or "vertical"
        bg_color = args.get("bg_color", None)
        fg_color = args.get("fg_color", None)

        # FIX: Force the separator to use the exact widget instance of its parent
        # instead of letting get_child_master() leak back up to the root window.
        master = parent.widget

        self.widget = sCTkSeparator(
            master=master,
            length=length,
            width=width,
            corner_radius=corner_radius,
            bg_color=bg_color,
            fg_color=fg_color,
            orientation=orientation
        )
        return self.widget
    def code_imports(self):
        # should return an iterable of (module, classname/function) to import
        # or None
        imports = [(widget_namespace, widget_classname)]
        imports.extend(self.code_extra_imports())
        return imports

    def _process_property_value(self, pname, value):
        """Passes values directly to allow core widget validations to handle exceptions."""
        return super()._process_property_value(pname, value)


# Register the widget into Pygubu's parsing engine
builder_id = f"{builder_namespace}.{widget_classname}"

register_widget(builder_id, sCTkSeparatorBuilder, 'sCTkSeparator', ("ttk", section_name))

# Register custom attribute fields to display inside the Designer properties panel
register_custom_property(
    builder_id, "length", "naturalnumber",
    help="Set total span length of the separator line in pixels"
)
register_custom_property(
    builder_id, "width", "naturalnumber",
    help="Set visual thickness profile width of the separator line in pixels"
)
register_custom_property(
    builder_id, "corner_radius", "naturalnumber",
    help="Define roundness sharpness limit token value for divider tips"
)
register_custom_property(
    builder_id, "orientation", "choice", values=("vertical", "horizontal") #, # state="readonly",
    # help="Select spatial directional positioning alignment"
)


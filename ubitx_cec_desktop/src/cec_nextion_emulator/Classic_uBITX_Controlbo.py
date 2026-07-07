#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from Classic_uBITX_Control import Classic_uBITX_Control


#
# Builder definition section
#
_widget_namespace = "Classic_uBITX_Control"
_widget_classname = "Classic_uBITX_Control"
_builder_namespace = "projectcustom"
_section_name = "Project Widgets"


class Classic_uBITX_ControlBO(BuilderObject):
    class_ = Classic_uBITX_Control


_builder_id = f"{_builder_namespace}.{_widget_classname}"
register_widget(
    _builder_id, Classic_uBITX_ControlBO, _widget_classname, (
        "ttk", _section_name)
)

#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from settingsMachine import settingsMachine


#
# Builder definition section
#
_widget_namespace = "settingsMachine"
_widget_classname = "settingsMachine"
_builder_namespace = "projectcustom"
_section_name = "Project Widgets"


class settingsMachineBO(BuilderObject):
    class_ = settingsMachine


_builder_id = f"{_builder_namespace}.{_widget_classname}"
register_widget(
    _builder_id, settingsMachineBO, _widget_classname, ("ttk", _section_name)
)

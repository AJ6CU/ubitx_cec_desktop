#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from JogwheelCustom import JogwheelCustom
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from mainScreen import mainScreen


#
# Builder definition section
#
_widget_namespace = "mainScreen"
_widget_classname = "mainScreen"
_builder_namespace = "projectcustom"
_section_name = "Project Widgets"


class mainScreenBO(BuilderObject):
    class_ = mainScreen


_builder_id = f"{_builder_namespace}.{_widget_classname}"
register_widget(
    _builder_id, mainScreenBO, _widget_classname, ("ttk", _section_name)
)

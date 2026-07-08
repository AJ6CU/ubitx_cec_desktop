#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from comportManager import comportManager


#
# Builder definition section
#
_widget_namespace = "comportManager"
_widget_classname = "comportManager"
_builder_namespace = "projectcustom"
_section_name = "Project Widgets"


class comportManagerBO(BuilderObject):
    class_ = comportManager


_builder_id = f"{_builder_namespace}.{_widget_classname}"
register_widget(
    _builder_id, comportManagerBO, _widget_classname, ("ttk", _section_name)
)

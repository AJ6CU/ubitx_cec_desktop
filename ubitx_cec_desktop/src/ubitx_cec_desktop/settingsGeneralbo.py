#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.combobox import Combobox
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from settingsGeneral import settingsGeneral


#
# Builder definition section
#
_widget_namespace = "settingsGeneral"
_widget_classname = "settingsGeneral"
_builder_namespace = "projectcustom"
_section_name = "Project Widgets"


class settingsGeneralBO(BuilderObject):
    class_ = settingsGeneral


_builder_id = f"{_builder_namespace}.{_widget_classname}"
register_widget(
    _builder_id, settingsGeneralBO, _widget_classname, ("ttk", _section_name)
)

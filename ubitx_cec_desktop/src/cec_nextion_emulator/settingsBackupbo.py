#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from settingsBackup import settingsBackup


#
# Builder definition section
#
_widget_namespace = "settingsBackup"
_widget_classname = "settingsBackup"
_builder_namespace = "projectcustom"
_section_name = "Project Widgets"


class settingsBackupBO(BuilderObject):
    class_ = settingsBackup


_builder_id = f"{_builder_namespace}.{_widget_classname}"
register_widget(
    _builder_id, settingsBackupBO, _widget_classname, ("ttk", _section_name)
)

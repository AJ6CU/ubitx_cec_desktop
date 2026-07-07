#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from settings import settings


#
# Builder definition section
#

class settingsBO(BuilderObject):
    class_ = settings


_builder_id = "projectcustom.settings"
register_widget(
    _builder_id, settingsBO, "settings", ("ttk", "Project Widgets")
)

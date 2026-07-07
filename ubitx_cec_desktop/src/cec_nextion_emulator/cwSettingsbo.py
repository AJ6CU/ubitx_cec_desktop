#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from cwSettings import cwSettings


#
# Builder definition section
#

class cwSettingsBO(BuilderObject):
    class_ = cwSettings


_builder_id = "projectcustom.cwSettings"
register_widget(
    _builder_id, cwSettingsBO, "cwSettings", ("ttk", "Project Widgets")
)

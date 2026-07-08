#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.combobox import Combobox
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from frequencyChannel import frequencyChannel


#
# Builder definition section
#

class frequencyChannelBO(BuilderObject):
    class_ = frequencyChannel


_builder_id = "projectcustom.frequencyChannel"
register_widget(
    _builder_id, frequencyChannelBO, "frequencyChannel", (
        "ttk", "Project Widgets")
)

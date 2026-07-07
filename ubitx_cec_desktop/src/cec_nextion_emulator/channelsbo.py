#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from frequencyChannel import frequencyChannel
from pygubu.widgets.combobox import Combobox
from pygubu.widgets.scrolledframe import ScrolledFrame
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from channels import channels


#
# Builder definition section
#

class channelsBO(BuilderObject):
    class_ = channels


_builder_id = "projectcustom.channels"
register_widget(
    _builder_id, channelsBO, "channels", ("ttk", "Project Widgets")
)

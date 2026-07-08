import tkinter as tk


from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)
from tkdial import Dial


#
# Builder definition section
#

class Dial_UXbo(BuilderObject):
    class_ = Dial


_builder_id = "projectcustom.Dial"
register_widget(
    _builder_id, Dial_UXbo, "Dial", ("tk", "Project Widgets")
)

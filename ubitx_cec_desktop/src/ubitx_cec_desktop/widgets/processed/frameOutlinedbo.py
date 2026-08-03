"""
frameOutlined

A custom widget.

UI source file: my_ctk_label.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import CTkFrame
from pygubu.api.v1 import (
    BuilderObject,
    register_widget, register_custom_property
)
from frameOutlined import frameOutlined

from pygubu.plugins.customtkinter import nsctk
from pygubu.plugins.customtkinter.widgets import CTkFrameBO
from pygubu.api.v1 import copy_custom_property


#
# Builder definition section
#
widget_namespace = "frameOutlined"
widget_classname = "frameOutlined"
builder_namespace = "custom_widgets"
section_name = "Project Widgets"


class frameOutlinedBO(CTkFrameBO):
    class_ = frameOutlined

    def code_imports(self):
        # should return an iterable of (module, classname/function) to import
        # or None
        imports = [(widget_namespace, widget_classname)]
        imports.extend(self.code_extra_imports())
        return imports


builder_id = f"{builder_namespace}.{widget_classname}"
register_widget(
    builder_id, frameOutlinedBO, widget_classname, ("ttk", section_name)
)

# Copy properties before we define our own properties.
#
# nsctk is the customtkinter plugin namespace
# nsctk.CTkFrame is the registered name for CTkFrameBO builder.
for pname in CTkFrameBO.properties:
    # try:
        copy_custom_property(nsctk.CTkFrame, pname, builder_id)
    # except:
    #     pass

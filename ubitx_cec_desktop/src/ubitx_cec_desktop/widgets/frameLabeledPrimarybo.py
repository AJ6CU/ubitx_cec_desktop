"""
frameLabeledPrimary

A custom widget.

UI source file: my_ctk_label.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import CTkScrollableFrame
from pygubu.api.v1 import (
    BuilderObject,
    register_widget, register_custom_property
)
from frameLabeledPrimary import frameLabeledPrimary

from pygubu.plugins.customtkinter import nsctk
from pygubu.plugins.customtkinter.scrollableframe import CTkScrollableFrameBO
from pygubu.api.v1 import copy_custom_property


#
# Builder definition section
#
widget_namespace = "frameLabeledPrimary"
widget_classname = "frameLabeledPrimary"
builder_namespace = "custom_widgets"
section_name = "Project Widgets"


class frameLabeledPrimaryBO(CTkScrollableFrameBO):
    class_ = frameLabeledPrimary

    def code_imports(self):
        # should return an iterable of (module, classname/function) to import
        # or None
        imports = [(widget_namespace, widget_classname)]
        imports.extend(self.code_extra_imports())
        return imports


builder_id = f"{builder_namespace}.{widget_classname}"
register_widget(
    builder_id, frameLabeledPrimaryBO, widget_classname, ("ttk", section_name)
)

# Copy properties before we define our own properties.
#
# nsctk is the customtkinter plugin namespace
# nsctk.CTkScrollableFrame is the registered name for CTkScrollableFrameBO builder.
for pname in CTkScrollableFrameBO.properties:
    try:
        copy_custom_property(nsctk.CTkScrollableFrame, pname, builder_id)
    except:
        pass

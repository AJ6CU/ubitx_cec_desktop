#!/usr/bin/python3
"""
optionMenuSecondary

Tailored version of the standard ctkOptionMenu for secondary

UI source file: sCTkOptionMenuSecondary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
from customtkinter import CTkOptionMenu
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
)

from pygubu.plugins.customtkinter import nsctk
from pygubu.plugins.customtkinter.widgets import CTkOptionMenuBO
from pygubu.api.v1 import copy_custom_property

from sCTkOptionMenuSecondary import sCTkOptionMenuSecondary


#
# Builder definition section
#
widget_namespace = "sCTkOptionMenuSecondary"
widget_classname = "sCTkOptionMenuSecondary"
builder_namespace = "custom_widgets"
section_name = "sCustomTkinter"


class sCTkOptionMenuSecondaryBO(CTkOptionMenuBO):
    class_ = sCTkOptionMenuSecondary

    def code_imports(self):
        # should return an iterable of (module, classname/function) to import
        # or None
        imports = [(widget_namespace, widget_classname)]
        imports.extend(self.code_extra_imports())
        return imports


builder_id = f"{builder_namespace}.{widget_classname}"
register_widget(
    builder_id, sCTkOptionMenuSecondaryBO, widget_classname, ("ttk", section_name)
)

# Copy properties before we define our own properties.
#
# nsctk is the customtkinter plugin namespace
# nsctk.CTkLabel is the registered name for BO builder.
for pname in CTkOptionMenuBO.properties:
    copy_custom_property(nsctk.CTkOptionMenu, pname, builder_id)
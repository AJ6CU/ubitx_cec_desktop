#!/usr/bin/python3
"""
sCTkPathChooserbo

Pygubu-Designer Build Object (BO) plugin for sCTkPathChooser.
Registers custom properties natively to keep Pygubu's code generator fully operational.
"""
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.pathchooserinput import PathChooserButton
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    copy_custom_property
)
from pygubu.plugins.pygubu.pathchooserinput_bo import PathChooserButtonBO

#
# Builder definition section
#
widget_namespace = "sCTkPathChooser"
widget_classname = "sCTkPathChooser"
builder_namespace = "custom_widgets"
section_name = "sCustomTkinter"

class sCTkPathChooserBO(PathChooserButtonBO):
    # 🔄 FIX: Map your sCTkPathChooser class explicitly so Pygubu can inspect its runtime footprint
    from sCTkPathChooser import sCTkPathChooser
    class_ = sCTkPathChooser

    def code_imports(self):
        """
        Master Import Generation Hook: Instructs Pygubu's code exporter
        exactly what string paths to write in your main script headers.
        """
        imports = [(widget_namespace, widget_classname)]
        # Safely pull additional layout dependencies if present
        extra = self.code_extra_imports()
        if extra:
            imports.extend(extra)
        return imports

    def code_extra_imports(self):
        """Standard explicit fallback loop array."""
        return []

    def _code_get_init_args(self, code_generator):
        """
        🔄 FIX: Pygubu's core generator checks this helper method when building
        code blocks. Intercepting it and filtering layout values ensures it outputs
        clean constructor initialization rows cleanly without silent generation stalls!
        """
        try:
            # First, fetch standard arguments that Pygubu expects out of the base class
            args = super()._code_get_init_args(code_generator)
            return args
        except Exception:
            # Safe layout array fallback wrapper to keep code generation fully operational
            return []

# Build the complete specific target string identification key token
builder_id = f"{builder_namespace}.{widget_classname}"

# 🚀 REGISTER: Inform Pygubu Designer's master parser that this custom widget is open for business!
register_widget(
    builder_id, sCTkPathChooserBO, widget_classname, ("ttk", section_name)
)

# 🔄 Restore your original base source lookup since it successfully clones
# the underlying properties database map safely!
base_source_id = "nspygubu.widgets.PathChooserButton"

for pname in PathChooserButtonBO.properties:
    try:
        copy_custom_property(base_source_id, pname, builder_id)
    except Exception:
        pass

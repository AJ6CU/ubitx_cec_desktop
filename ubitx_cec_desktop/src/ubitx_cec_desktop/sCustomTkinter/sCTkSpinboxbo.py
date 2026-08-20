import pygubu
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property
)
from sCTkSpinbox import sCTkSpinbox

widget_namespace = "sCTkSpinbox"
widget_classname = "sCTkSpinbox"
builder_namespace = "custom_widgets"
section_name = "sCustomTkinter"


class sCTkSpinboxBO(BuilderObject):
    class_ = sCTkSpinbox

    # 📐 STRUCTURAL LAYOUT SEQUENCING MATRIX: Maps native parameters cleanly.
    # Numerical boundaries and formats load sequentially before states execute.
    OPTIONS_CUSTOM = ('from_', 'to', 'step_size', 'format', 'button_width',
                      'button_height', 'button_side', 'orientation',
                      'arrow_font_size', 'state', 'justify', 'placeholder_text',
                      'textvariable', 'values', 'wrap')

    properties = OPTIONS_CUSTOM
    command_properties = ("command",)

    container = False

    @classmethod
    def setup_properties(cls):
        super().setup_properties()
        for prop in cls.OPTIONS_CUSTOM:
            if prop not in cls.properties:
                cls.properties = cls.properties + (prop,)

    def _process_property_value(self, name, value):
        """Sanitizes property values, ensuring numeric casting matches type rules."""
        if value is None or str(value).strip() == "": return None
        if name in ('button_width', 'button_height', 'arrow_font_size'): return int(str(value).strip())
        if name in ('from_', 'to', 'step_size'): return float(str(value).strip())
        if name == 'wrap': return str(value).lower() in ("true", "1", "yes")
        # Strings and format masks pass straight through un-mangled to prevent parsing drops
        return str(value).strip()

    def _get_init_args(self, extra_init_args=None):
        """Assembles constructor arguments in safe sequential execution rings."""
        args = super()._get_init_args(extra_init_args)
        w_props = self.wmeta.properties if (hasattr(self, 'wmeta') and hasattr(self.wmeta, 'properties')) else {}

        for prop in self.OPTIONS_CUSTOM:
            # Skip textvariable and command here since they pass through specialized setter paths
            if prop in ('textvariable', 'command'): continue
            val = w_props.get(prop)
            if val is not None and str(val).strip() != "":
                args[prop] = self._process_property_value(prop, val)

        # Guard initialization states from blank or unassigned numerical floor limits
        if 'from_' not in args or args['from_'] is None:
            args['from_'] = 0.0

        return args

    def set_property(self, name, value):
        """Routes dynamic inspector panel property adjustments straight into the live instance."""
        if hasattr(self, 'wmeta') and hasattr(self.wmeta, 'properties'):
            self.wmeta.properties[name] = value

        if hasattr(self, 'widget') and self.widget:
            # Route tkVariable conversion tracks properly inside Pygubu's editor framework
            if name == 'textvariable':
                processed = self.builder.get_variable(value)
            elif name == 'command':
                processed = self.builder.get_callback(value)
            else:
                processed = self._process_property_value(name, value)

            self.widget.configure(**{name: processed})

            # Force the active canvas view to recalculate layout fields instantly
            if name in ('format', 'from_', 'step_size', 'values', 'wrap'):
                try:
                    current_num = float(self.widget.get())
                    self.widget.set(current_num)
                except Exception:
                    # Fallback to direct string or baseline checks if casting fails
                    if hasattr(self.widget, '_values') and self.widget._values:
                        self.widget.set(self.widget._values[0])
                    elif hasattr(self.widget, '_from'):
                        self.widget.set(self.widget._from)

    def code_get_configure_properties(self, code_identifier, entry):
        """Instructs Pygubu's compiler to pipe variables and callbacks through native channels."""
        return ['textvariable', 'command']

    def code_get_init_args(self, code_identifier, entry):
        """Emits pristine syntax definitions for compilation into final exported Python scripts."""
        init_args = {}
        w_props = self.wmeta.properties if (hasattr(self, 'wmeta') and hasattr(self.wmeta, 'properties')) else {}
        for prop in self.OPTIONS_CUSTOM:
            if prop in ('textvariable', 'command'): continue  # Code generator handles these in configuration loops
            value = w_props.get(prop)
            if value is not None and value != '':
                processed = self._process_property_value(prop, value)
                if processed is not None:
                    # Guard format masks with explicit quotes inside the final output files
                    if prop in ('format', 'values', 'button_side', 'orientation', 'justify', 'placeholder_text'):
                        init_args[prop] = f'"{processed}"'
                    else:
                        init_args[prop] = repr(processed)
        return init_args


# =============================================================================
#   🎨 INSPECTOR PANEL PROPERTY REGISTRATION (ORDER ENFORCED)
# =============================================================================
builder_id = f"{builder_namespace}.{widget_classname}"

register_custom_property(builder_id, 'format', 'entry')
register_custom_property(builder_id, 'from_', 'entry')
register_custom_property(builder_id, 'to', 'entry')
register_custom_property(builder_id, 'step_size', 'entry')
register_custom_property(builder_id, 'values', 'entry')
register_custom_property(builder_id, 'wrap', 'choice', values=('True', 'False'))
register_custom_property(builder_id, 'button_width', 'naturalnumber')
register_custom_property(builder_id, 'button_height', 'naturalnumber')
register_custom_property(builder_id, 'button_side', 'choice', values=('right', 'left', 'split'))
register_custom_property(builder_id, 'orientation', 'choice', values=('vertical', 'horizontal'))
register_custom_property(builder_id, 'arrow_font_size', 'naturalnumber')
register_custom_property(builder_id, 'state', 'choice', values=('normal', 'disabled'))
register_custom_property(builder_id, 'justify', 'choice', values=('left', 'center', 'right'))
register_custom_property(builder_id, 'placeholder_text', 'entry')

# Map the variable links and callback properties using precise editor helper fields
register_custom_property(builder_id, 'textvariable', 'tkvarentry')
register_custom_property(builder_id, 'command', 'commandentry')

register_widget(builder_id, sCTkSpinboxBO, 'sCTkSpinbox', ("ttk", section_name))

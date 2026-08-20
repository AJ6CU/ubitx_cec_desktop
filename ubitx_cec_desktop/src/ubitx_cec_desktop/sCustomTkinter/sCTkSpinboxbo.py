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

    # 📐 FIXED CODE GENERATION TRACKING MATRIX: Include properties inside custom options
    # to notify Pygubu's emission loop engine that these must generate layout code!
    OPTIONS_CUSTOM = ('from_', 'to', 'step_size', 'format', 'button_width',
                      'button_height', 'button_side', 'orientation',
                      'arrow_font_size', 'state', 'justify', 'placeholder_text',
                      'textvariable', 'command')
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
        if value is None or str(value).strip() == "": return None
        if name in ('button_width', 'button_height', 'arrow_font_size'): return int(str(value).strip())
        if name in ('from_', 'to', 'step_size'): return float(str(value).strip())
        return str(value)

    def _get_init_args(self, extra_init_args=None):
        args = super()._get_init_args(extra_init_args)
        w_props = self.wmeta.properties if (hasattr(self, 'wmeta') and hasattr(self.wmeta, 'properties')) else {}

        # Pull properties sequentially out of your OPTIONS_CUSTOM table row mapping layout
        for prop in self.OPTIONS_CUSTOM:
            # Skip textvariable and command here since they pass through specialized setter tracking paths
            if prop in ('textvariable', 'command'): continue
            val = w_props.get(prop)
            if val is not None and str(val).strip() != "":
                args[prop] = self._process_property_value(prop, val)
        return args

    def set_property(self, name, value):
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

            if name in ('format', 'from_', 'step_size'):
                try:
                    current_num = float(self.widget.get())
                    self.widget.set(current_num)
                except Exception:
                    if hasattr(self.widget, '_from'):
                        self.widget.set(self.widget._from)

    def code_get_configure_properties(self, code_identifier, entry):
        # Let Pygubu's script compiler pipe variables and callbacks through native channels
        return ['textvariable', 'command']

    def code_get_init_args(self, code_identifier, entry):
        init_args = {}
        w_props = self.wmeta.properties if (hasattr(self, 'wmeta') and hasattr(self.wmeta, 'properties')) else {}
        for prop in self.OPTIONS_CUSTOM:
            if prop in ('textvariable', 'command'): continue  # Code generator handles these in configuration loops
            value = w_props.get(prop)
            if value is not None and value != '':
                processed = self._process_property_value(prop, value)
                if processed is not None:
                    if prop == 'format':
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
register_custom_property(builder_id, 'button_width', 'naturalnumber')
register_custom_property(builder_id, 'button_height', 'naturalnumber')
register_custom_property(builder_id, 'button_side', 'choice', values=('right', 'left', 'split'))
register_custom_property(builder_id, 'orientation', 'choice', values=('vertical', 'horizontal'))
register_custom_property(builder_id, 'arrow_font_size', 'naturalnumber')
register_custom_property(builder_id, 'state', 'choice', values=('normal', 'disabled'))
register_custom_property(builder_id, 'justify', 'choice', values=('left', 'center', 'right'))
register_custom_property(builder_id, 'placeholder_text', 'entry')

# Natively map the variable links and callback properties inside Pygubu
register_custom_property(builder_id, 'textvariable', 'tkvarentry')
register_custom_property(builder_id, 'command', 'commandentry')

register_widget(builder_id, sCTkSpinboxBO, 'sCTkSpinbox', ("ttk", section_name))

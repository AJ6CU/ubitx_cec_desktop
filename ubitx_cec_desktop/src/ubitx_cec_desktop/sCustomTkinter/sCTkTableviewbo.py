import pygubu
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property
)
from sCTkTableview import sCTkTableview

TRACKING_ID = "sCTkTableview"
section_name = "sCustomTkinter"


class sCTkTableviewBO(BuilderObject):
    """
    Pygubu Designer visual studio object builder registration helper subclass.
    🚀 PROPERTY SEQUENCE PATCH: Rearranged so that structural grid counts
    load and evaluate BEFORE the string column parser executes!
    """
    class_ = sCTkTableview
    WIDGET_TAG = TRACKING_ID
    import_modules = ['sCTkTableview']

    # 📐 Structural options declared first, layout payload definitions placed dead last!
    OPTIONS_CUSTOM = ('num_columns', 'num_rows', 'grid_mode', 'show_headers', 'header_line_width', 'outline_width',
                      'outline_radius', 'state', 'cell_bg_color', 'cell_alt_bg_color', 'columns')
    properties = OPTIONS_CUSTOM

    container = True
    allowed_parents = ('root', 'frame', 'toplevel', 'panedwindow', 'notebook', 'scrollableframe')

    @classmethod
    def setup_properties(cls):
        super().setup_properties()
        for prop in cls.OPTIONS_CUSTOM:
            if prop not in cls.properties:
                cls.properties = cls.properties + (prop,)

    def get_layout_properties(self):
        props = super().get_layout_properties() if hasattr(super(), 'get_layout_properties') else {}
        for custom_prop in self.OPTIONS_CUSTOM:
            props.pop(custom_prop, None)
        return props

    def layout(self):
        if hasattr(self, 'wmeta') and hasattr(self.wmeta, 'layout_properties'):
            clean_properties = dict(self.wmeta.layout_properties)
            for custom_prop in self.OPTIONS_CUSTOM:
                clean_properties.pop(custom_prop, None)
            self.wmeta.layout_properties = clean_properties
        super().layout()

    def _process_property_value(self, name, value):
        if name == 'columns':
            if not value or not str(value).strip(): return []
            return [col.strip() for col in str(value).split(',') if col.strip()]
        if value is None or str(value).strip() == "":
            return None
        if name in ('num_columns', 'num_rows', 'header_line_width', 'outline_radius'):
            return int(str(value).strip())
        if name == 'show_headers':
            return str(value).lower() in ("true", "1", "yes")
        return str(value)

    def _get_init_args(self, extra_init_args=None):
        args = super()._get_init_args(extra_init_args)
        w_props = self.wmeta.properties if (hasattr(self, 'wmeta') and hasattr(self.wmeta, 'properties')) else {}

        args['num_columns'] = int(w_props.get('num_columns') if w_props.get('num_columns') else 3)
        args['num_rows'] = int(w_props.get('num_rows') if w_props.get('num_rows') else 1)
        args['grid_mode'] = str(w_props.get('grid_mode') if w_props.get('grid_mode') else "zebra")

        raw_cols = w_props.get('columns')
        if raw_cols:
            args['columns'] = self._process_property_value('columns', raw_cols)
            args['num_columns'] = len(args['columns'])

        args['show_headers'] = self._process_property_value('show_headers', w_props.get('show_headers') or True)
        return args

    def set_property(self, name, value):
        super().set_property(name, value)
        if hasattr(self, "builder") and hasattr(self.builder, "recreate_widget"):
            try:
                self.builder.recreate_widget(self)
            except Exception:
                pass

    def code_get_configure_properties(self, code_identifier, entry):
        return []

    def code_get_init_args(self, code_identifier, entry):
        init_args = {}
        w_props = self.wmeta.properties if (hasattr(self, 'wmeta') and hasattr(self.wmeta, 'properties')) else {}
        for prop in self.OPTIONS_CUSTOM:
            value = w_props.get(prop)
            if value is not None and value != '':
                processed = self._process_property_value(prop, value)
                if processed is not None:
                    init_args[prop] = repr(processed)
        return init_args


# =============================================================================
#   🎨 INSPECTOR PANEL PROPERTY REGISTRATION (ORDER ENFORCED)
# =============================================================================
register_custom_property(TRACKING_ID, 'num_columns', 'naturalnumber')
register_custom_property(TRACKING_ID, 'num_rows', 'naturalnumber')
register_custom_property(TRACKING_ID, 'grid_mode', 'choice', values=('zebra', 'grid', 'none'))
register_custom_property(TRACKING_ID, 'show_headers', 'choice', values=('True', 'False'))
register_custom_property(TRACKING_ID, 'header_line_width', 'naturalnumber')
register_custom_property(TRACKING_ID, 'outline_width', 'integernumber')
register_custom_property(TRACKING_ID, 'outline_radius', 'naturalnumber')
register_custom_property(TRACKING_ID, 'state', 'choice', values=('normal', 'disabled'))
register_custom_property(TRACKING_ID, 'cell_bg_color', 'entry')
register_custom_property(TRACKING_ID, 'cell_alt_bg_color', 'entry')

# 👑 Columns text registration placed dead last!
register_custom_property(TRACKING_ID, 'columns', 'entry')

register_widget(TRACKING_ID, sCTkTableviewBO, 'sCTkTableview', ("ttk", section_name))

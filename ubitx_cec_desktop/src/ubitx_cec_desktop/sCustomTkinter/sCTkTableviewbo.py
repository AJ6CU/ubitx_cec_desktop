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
    Uses the synchronous post-connection lifecycle sweep to firmly lock
    and repaint custom header text elements on every sidebar switch mutation pass.
    """
    class_ = sCTkTableview
    WIDGET_TAG = TRACKING_ID

    import_modules = ['sCTkTableview']
    OPTIONS_CUSTOM = ('columns', 'num_columns', 'num_rows', 'show_headers', 'grid_mode', 'cell_bg_color',
                      'cell_alt_bg_color', 'header_line_width', 'outline_width', 'outline_radius', 'state')
    properties = OPTIONS_CUSTOM

    container = True
    allowed_parents = ('root', 'frame', 'toplevel', 'panedwindow', 'notebook', 'scrollableframe')
    allowed_children = ()

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
            if isinstance(value, list): return value
            if not value or not str(value).strip(): return []
            raw_str = str(value).replace("'", "").replace('"', "").replace("[", "").replace("]", "").strip()
            return [col.strip() for col in raw_str.split(',') if col.strip()]

        if value is None or str(value).strip() == "":
            return None

        if name in ('num_columns', 'num_rows', 'header_line_width', 'outline_radius'):
            return int(str(value).replace("'", "").replace('"', "").strip())
        if name == 'outline_width':
            return float(str(value).replace("'", "").replace('"', "").strip())
        if name == 'show_headers':
            return str(value).replace("'", "").replace('"', "").strip().lower() in ("true", "1", "yes")
        if name == 'grid_mode':
            return str(value).replace("'", "").replace('"', "").strip().lower()
        if name in ('cell_bg_color', 'cell_alt_bg_color'):
            val_str = str(value).strip()
            if val_str.startswith("(") and val_str.endswith(")"):
                try:
                    return eval(val_str)
                except Exception:
                    pass
            return val_str
        return super()._process_property_value(name, value)

    def _get_init_args(self, extra_init_args=None):
        args = super()._get_init_args(extra_init_args)
        w_props = self.wmeta.properties if (hasattr(self, 'wmeta') and hasattr(self.wmeta, 'properties')) else {}

        args['num_columns'] = int(w_props.get('num_columns') if w_props.get('num_columns') else 3)
        args['num_rows'] = int(w_props.get('num_rows') if w_props.get('num_rows') else 1)
        args['grid_mode'] = str(w_props.get('grid_mode') if w_props.get('grid_mode') else "zebra")
        args['header_line_width'] = int(w_props.get('header_line_width') if w_props.get('header_line_width') else 2)
        args['outline_width'] = float(w_props.get('outline_width') if w_props.get('outline_width') else 1.0)
        args['outline_radius'] = int(w_props.get('outline_radius') if w_props.get('outline_radius') else 4)
        args['state'] = str(w_props.get('state') if w_props.get('state') else "normal")

        # Safe constructor baseline assignments
        raw_cols = w_props.get('columns')
        if raw_cols:
            processed_cols = self._process_property_value('columns', raw_cols)
            if processed_cols and len(processed_cols) > 0:
                args['columns'] = processed_cols
                args['num_columns'] = len(processed_cols)

        if w_props.get('cell_bg_color'): args['cell_bg_color'] = self._process_property_value('cell_bg_color',
                                                                                              w_props.get(
                                                                                                  'cell_bg_color'))
        if w_props.get('cell_alt_bg_color'): args['cell_alt_bg_color'] = self._process_property_value(
            'cell_alt_bg_color', w_props.get('cell_alt_bg_color'))

        raw_show = w_props.get('show_headers')
        args['show_headers'] = self._process_property_value('show_headers', raw_show if raw_show is not None else True)
        return args

    def _connect_widget(self):
        """
        ⚡ THE POST-RECREATION LIFECYCLE REPAINT SWEEP:
        Runs synchronously the exact millisecond Pygubu finishes re-attaching the widget
        to the live design tree canvas view. At this point, Pygubu releases its data locks,
        allowing us to safely extract your column string values and force them to paint!
        """
        # 1. Let Pygubu's master process baseline application linkages first
        super()._connect_widget()

        # 2. Extract and forcefully restore the column header texts
        w_props = self.wmeta.properties if (hasattr(self, 'wmeta') and hasattr(self.wmeta, 'properties')) else {}
        raw_cols_value = w_props.get('columns')

        if self.widget and raw_cols_value and str(raw_cols_value).strip() != "":
            try:
                processed_cols = self._process_property_value('columns', raw_cols_value)
                if processed_cols and len(processed_cols) > 0:
                    self.widget.configure(columns=processed_cols)
            except Exception:
                pass

    def set_property(self, name, value):
        super().set_property(name, value)

        preview_master = self.widget.master if (self.widget and hasattr(self.widget, 'master')) else None

        if hasattr(self, "builder") and hasattr(self.builder, "recreate_widget"):
            try:
                self.builder.recreate_widget(self)
            except Exception:
                pass

        if preview_master and hasattr(preview_master, "update_idletasks"):
            try:
                preview_master.update_idletasks()
                if hasattr(preview_master, "grid_slaves"):
                    for slave in preview_master.grid_slaves():
                        slave.update_idletasks()
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

        if 'num_columns' not in init_args: init_args['num_columns'] = "3"
        if 'num_rows' not in init_args: init_args['num_rows'] = "1"
        if 'show_headers' not in init_args: init_args['show_headers'] = "True"
        if 'grid_mode' not in init_args: init_args['grid_mode'] = "'zebra'"
        if 'columns' not in init_args or str(init_args['columns']).strip() in (None, "None", "''", '""', "[]"):
            init_args['columns'] = "None"

        return init_args


# =============================================================================
#   🎨 INSPECTOR PANEL PROPERTY REGISTRATION
# =============================================================================
register_custom_property(TRACKING_ID, 'columns', 'entry')
register_custom_property(TRACKING_ID, 'num_columns', 'naturalnumber')
register_custom_property(TRACKING_ID, 'num_rows', 'naturalnumber')
register_custom_property(TRACKING_ID, 'show_headers', 'choice', values=('True', 'False'))
register_custom_property(TRACKING_ID, 'grid_mode', 'choice', values=('zebra', 'grid', 'none'))
register_custom_property(TRACKING_ID, 'cell_bg_color', 'entry')
register_custom_property(TRACKING_ID, 'cell_alt_bg_color', 'entry')
register_custom_property(TRACKING_ID, 'header_line_width', 'naturalnumber')
register_custom_property(TRACKING_ID, 'outline_width', 'integernumber')
register_custom_property(TRACKING_ID, 'outline_radius', 'naturalnumber')
register_custom_property(TRACKING_ID, 'state', 'choice', values=('normal', 'disabled'))

register_widget(TRACKING_ID, sCTkTableviewBO, 'sCTkTableview', ("ttk", section_name))

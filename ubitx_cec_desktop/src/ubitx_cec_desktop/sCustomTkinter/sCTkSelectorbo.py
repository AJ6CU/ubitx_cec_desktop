#!/usr/bin/python3
"""
sCTkSelector Builder Object
"""
import ast
import pygubu
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property
)
from sCTkSelector import sCTkSelector


widget_namespace = "sCTkSelector"
widget_classname = "sCTkSelector"
builder_namespace = "custom_widgets"


class sCTkSelectorBO(BuilderObject):
    class_ = sCTkSelector

    OPTIONS_STANDARD=('height','width')
    OPTIONS_CUSTOM = ('items', 'multiple_choices')
    properties = BuilderObject.properties + OPTIONS_CUSTOM + OPTIONS_STANDARD

    OPTIONS_CUSTOM_DEFAULTS = {
        'multiple_choices': 'True',
        'items': "['Item 1', 'Item 2']"
    }

    container = True
    container_layout = False

    def code_imports(self):
        return [(widget_namespace, widget_classname)]

    def realize(self, parent, extra_init_args: dict = None):
        if extra_init_args is None:
            extra_init_args = {}

        items_val = self.wmeta.properties.get('items', "['Item 1', 'Item 2']")
        try:
            items_arg = ast.literal_eval(items_val)
        except Exception:
            items_arg = ["Item 1", "Item 2"]

        mult_choice = self.wmeta.properties.get('multiple_choices', 'True')
        mult_choice_arg = str(mult_choice).lower() in ['true', '1', 'yes']

        init_args = {
            'items': items_arg,
            'multiple_choices': mult_choice_arg
        }

        for prop in self.OPTIONS_CUSTOM:
            extra_init_args.pop(prop, None)

        init_args.update(extra_init_args)

        real_master = parent.widget if hasattr(parent, 'widget') else parent
        self.widget = self.class_(real_master, **init_args)
        return self.widget

    def _code_set_property(self, targetid, pname, value, code_bag):
        """
        The low-level code generation interception layer.
        Assigning raw text blocks to code_bag removes the outer double quotes.
        """
        if pname == 'items':
            # Pygubu passes value down pre-escaped. We clean up the outside tracking quotes.
            clean_list_string = str(value).strip("'\"")

            # Registering the raw unquoted value to the code_bag dictionary maps it
            # as a live python array token instead of an escaped string sequence
            code_bag[pname] = clean_list_string

        elif pname == 'multiple_choices':
            clean_bool_string = str(value).strip("'\"")
            code_bag[pname] = clean_bool_string

        else:
            super()._code_set_property(targetid, pname, value, code_bag)


builder_id = f"{builder_namespace}.{widget_classname}"

register_widget(
    builder_id, sCTkSelectorBO, widget_classname, ('sCustomTkinter', 'My Widgets')
)

register_custom_property(
    builder_id,
    'items',
    'entry',
    help="Python list format: ['A', 'B', 'C']"
)

register_custom_property(
    builder_id,
    'multiple_choices',
    'choice',
    values=('True', 'False')
)



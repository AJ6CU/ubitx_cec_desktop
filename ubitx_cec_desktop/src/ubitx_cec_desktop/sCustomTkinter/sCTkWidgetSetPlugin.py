import tkinter as tk
from pygubu.component.plugin_engine import IDesignerPlugin
from pygubu.component.plugin_manager import PluginManager
from customtkinter import (CTkScrollableFrame)

from sCTkFrame import sCTkFrame
from sCTkFramebo import (
    sCTkFrameBO,
    builder_id as sCTkFrame_builder_id
)

from sCTkFrameOutlined import sCTkFrameOutlined
from sCTkFrameOutlinedbo import (
    sCTkFrameOutlinedBO,
    builder_id as sCTkFrameOutlined_builder_id
)

from sCTkFrameLabeledPrimary import sCTkFrameLabeledPrimary
from sCTkFrameLabeledPrimarybo import (
    sCTkFrameLabeledPrimaryBO,
    builder_id as sCTkFrameLabeledPrimary_builder_id
)

from sCTkPathChooser import sCTkPathChooser
from sCTkPathChooserbo import (
    sCTkPathChooserBO,
    builder_id as sCTkPathChooser_builder_id
)


from sCTkTableview import sCTkTableview
from sCTkTableviewbo import (
    sCTkTableviewBO,
    builder_id as sCTkTableview_builder_id
)

from sCTkSelector import sCTkSelector
from sCTkCheckBox import sCTkCheckBox

from sCTkSelectorbo import (
    sCTkSelectorBO,
    builder_id as sCTkSelector_builder_id
)

from sCTkOptionMenuSecondary import sCTkOptionMenuSecondary
from sCTkOptionMenuSecondarybo import (
    sCTkOptionMenuSecondaryBO,
    builder_id as sCTkOptionMenuSecondary_builder_id
)


# from sCTkDial import sCTkDialContinuous
# from sCTkDialbo import (
#     sCTkDialContinuousBO,
#     builder_id as sCTkDialContinuous_builder_id
# )

#
# Preview class for sCTkFrame
#
class sCTkFrameForPreview(sCTkFrame):
    def winfo_children(self):
        # CTkFrame has a hidden canvas inside. So, to make it
        #  clickable on preview we need a hack.
        return super(tk.Frame, self).winfo_children()

class sCTkFrameOutlinedForPreview(sCTkFrameOutlined):
    def winfo_children(self):
        # CTkFrameOUtline has a hidden canvas inside. So, to make it
        #  clickable on preview we need a hack.
        return super(tk.Frame, self).winfo_children()


class sCTkFrameLabeledPrimaryForPreview(sCTkFrameLabeledPrimary):
    def winfo_children(self):
        # CTkFrameOUtline has a hidden canvas inside. So, to make it
        #  clickable on preview we need a hack.
        return super(tk.Frame, self).winfo_children()

class sCTkPathChooserForPreview(sCTkPathChooser):
    def winfo_children(self):
        # CTkFrameOUtline has a hidden canvas inside. So, to make it
        #  clickable on preview we need a hack.
        return super(tk.Frame, self).winfo_children()

class sCTkTableviewForPreview(sCTkTableview):
    def winfo_children(self):
        internal = []
        internal.extend(self._header_widgets)
        for row in self._cell_widgets:
            internal.extend(row)
        clist = [self._scrollbar]
        for widget in internal:
            for cwidget in widget.winfo_children():
                clist.append(cwidget)
        return clist


class sCTkSelectorForPreview(sCTkSelector):
    def winfo_children(self):
        internal = [
            self.search_bar,
            self.checkboxes_frame,
            self.checkboxes_frame._parent_frame,
            self.checkboxes_frame._parent_canvas,
        ]
        clist = []
        for widget in internal:
            for cwidget in widget.winfo_children():
                clist.append(cwidget)
                if isinstance(cwidget, sCTkCheckBox):
                    clist.append(cwidget._text_label)
                    clist.append(cwidget._canvas)
        return clist
import sys
class sCTkOptionMenuSecondaryForPreview(sCTkOptionMenuSecondary):
    def winfo_children(self):
        internal = [
            self._menu,
        ]
        clist = []
        for widget in internal:
            for cwidget in widget.winfo_children():
                clist.append(cwidget)
        return clist


# class sCTkDialContinuousForPreview(sCTkDialContinuous):
#     def winfo_children(self):
#         return super(tk.Frame, self).winfo_children()

#
# Builder for Preview
#
class sCTkFramePreviewBO(sCTkFrameBO):
    class_ = sCTkFrameForPreview

class sCTkFrameOutlinedForPreviewBO(sCTkFrameOutlinedBO):
    class_ = sCTkFrameOutlinedForPreview

class sCTkFrameLabeledPrimaryForPreviewBO(sCTkFrameLabeledPrimaryBO):
    class_ = sCTkFrameLabeledPrimaryForPreview

class sCTkPathChooserForPreviewBO(sCTkPathChooserBO):
    class_ = sCTkPathChooserForPreview

class sCTkTableviewForPreviewBO(sCTkTableviewBO):
    class_ = sCTkTableviewForPreview

class sCTkSelectorForPreviewBO(sCTkSelectorBO):
    class_ = sCTkSelectorForPreview

class sCTkOptionMenuSecondaryForPreviewBO(sCTkOptionMenuSecondaryBO):
    class_ = sCTkOptionMenuSecondaryForPreview
#
# class sCTkDialContinuousForPreviewBO(sCTkSelectorBO):
#     class_ = sCTkDialContinuousForPreview


#
# A Designer plugin for sCTk custom widgets
#
class sCTkPlugin(IDesignerPlugin):

    def get_preview_builder(self, builder_uid: str):
        """Return a BuilderObject subclass used to build a preview
        for the target builder_uid"""

        if builder_uid == sCTkFrame_builder_id:
            return sCTkFramePreviewBO
        elif builder_uid == sCTkFrameOutlined_builder_id:
            return sCTkFrameOutlinedForPreviewBO
        elif builder_uid == sCTkFrameLabeledPrimary_builder_id:
            return sCTkFrameLabeledPrimaryForPreviewBO
        elif builder_uid == sCTkPathChooser_builder_id:
            return sCTkPathChooserForPreviewBO
        elif builder_uid == sCTkTableview_builder_id:
            return sCTkTableviewForPreviewBO
        elif builder_uid == sCTkSelector_builder_id:
            return sCTkSelectorForPreviewBO
        elif builder_uid == sCTkOptionMenuSecondary_builder_id:
            return sCTkOptionMenuSecondaryForPreviewBO

        # elif builder_uid == sCTkDialContinuous_builder_id:
        #     return sCTkDialContinuousForPreviewBO
        return None


#
# Create a plugin instance and inject it.
#
custom_plugin = sCTkPlugin()
PluginManager.designer_plugins.append(custom_plugin)


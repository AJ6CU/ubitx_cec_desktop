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
from sCTkSelectorbo import (
    sCTkSelectorBO,
    builder_id as sCTkSelector_builder_id
)

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
        return super(tk.Frame, self).winfo_children()


class sCTkSelectorForPreview(sCTkSelector):
    def winfo_children(self):
        return super(tk.Frame, self).winfo_children()

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
        return None


#
# Create a plugin instance and inject it.
#
custom_plugin = sCTkPlugin()
PluginManager.designer_plugins.append(custom_plugin)


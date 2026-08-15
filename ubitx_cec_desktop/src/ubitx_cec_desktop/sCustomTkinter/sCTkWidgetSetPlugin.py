import tkinter as tk
from pygubu.component.plugin_engine import IDesignerPlugin
from pygubu.component.plugin_manager import PluginManager

from sCTkFrame import sCTkFrame
from sCTkFramebo import (
    sCTkFrameBO,
    builder_id as sctk_frame_builder_id
)

from sCTkFrameOutlined import sCTkFrameOutlined
from sCTkFrameOutlinedbo import (
    sCTkFrameOutlinedBO,
    builder_id as sctk_frameOutlined_builder_id
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


#
# Builder for Preview
#
class sCTkFramePreviewBO(sCTkFrameBO):
    class_ = sCTkFrameForPreview

class CTkFrameOutlinedForPreviewBO(sCTkFrameOutlinedBO):
    class_ = sCTkFrameOutlinedForPreview


#
# A Designer plugin for sCTk custom widgets
#
class sCTkPlugin(IDesignerPlugin):

    def get_preview_builder(self, builder_uid: str):
        """Return a BuilderObject subclass used to build a preview
        for the target builder_uid"""

        if builder_uid == sctk_frame_builder_id:
            return sCTkFramePreviewBO
        elif builder_uid == sctk_frameOutlined_builder_id:
            return CTkFrameOutlinedForPreviewBO
        return None


#
# Create a plugin instance and inject it.
#
custom_plugin = sCTkPlugin()
PluginManager.designer_plugins.append(custom_plugin)


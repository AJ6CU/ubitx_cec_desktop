# Derived from Selector class by Fastattack, 2024).
# https://github.com/fastattackv/MoreCustomTkinterWidgets
#

import customtkinter as ctk
from typing import Literal, Union, Tuple, Optional

# ==========================================
#   Themeable / Project Custom Fallbacks
#   (Remove or adjust these based on your absolute import paths)
# ==========================================
from ThemeableWidget import ThemeableWidget
from sCTkThemes import THEME_DEFAULTS
from ThemeableWidget import ThemeableWidget


class sCTkSeparator(ctk.CTkBaseClass, ThemeableWidget):
    """
    Separator widget to mark a separation between 2 other widgets.
    Fully integrated with centralized theme tracking (ThemeableWidget)
    and smooth dynamic scaling support.
    """

    def __init__(self,
                 master: any,
                 length: int = 100,
                 width: float = 4,
                 corner_radius: Optional[int] = None,
                 bg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 orientation: Literal["vertical", "horizontal"] = "vertical"
                 ):

        # 1. Capture initialization parameters into a localized dictionary for processing
        local_kwargs = {
            "corner_radius": corner_radius,
            "bg_color": bg_color,
            "fg_color": fg_color
        }

        # 2. Invoke the ThemeableWidget engine to scrub parameters and construct self.final_kw
        ThemeableWidget.__init__(
            self,
            theme_defaults=THEME_DEFAULTS.get("sCTkSeparator", {}),
            kwargs=local_kwargs
        )

        # 3. Orient layout dimension profiles safely
        if orientation == "vertical":
            height = length
        elif orientation == "horizontal":
            height = width
            width = length
        else:
            raise ValueError(
                f"The value for orientation is incorrect: \"{orientation}\". Should be \"vertical\" or \"horizontal\"")

        # 4. Initialize CustomTkinter's base structure using finalized parameters
        ctk.CTkBaseClass.__init__(
            self,
            master=master,
            width=width,
            height=height,
            bg_color=self.final_kw.get("bg_color", "transparent")
        )

        # 5. Extract finalized properties out of the sanitized theme dictionary layer
        self._corner_radius = self.final_kw.get("corner_radius", 6)
        self._fg_color = self._check_color_type(self.final_kw.get("fg_color"))
        self._orientation = orientation

        # 6. Canvas and render configurations
        self._canvas = ctk.CTkCanvas(self, highlightthickness=0)
        self._canvas.place(x=0, y=0, relwidth=1, relheight=1)

        self._canvas.configure(bg=self._apply_appearance_mode(self._detect_color_of_master()))
        self._draw_engine = ctk.DrawEngine(self._canvas)

        # 7. Bind layout adjustments to bypass CTkBaseClass strict bind filters safely
        super(ctk.CTkBaseClass, self).bind("<Configure>", self._on_resize, add="+")
        self._draw(no_color_updates=True)

    def _on_resize(self, event):
        """Callback to handle dynamic physical frame adjustments."""
        self._draw()

    def _set_scaling(self, *args, **kwargs):
        super()._set_scaling(*args, **kwargs)
        self._draw()

    def _set_dimensions(self, width=None, height=None):
        super()._set_dimensions(width, height)
        self._draw()

    def _draw(self, no_color_updates=False):
        super()._draw(no_color_updates)

        # Read layout panel allocations explicitly to adapt seamlessly during resize actions
        current_w = self.winfo_width() if self.winfo_width() > 1 else self._current_width
        current_h = self.winfo_height() if self.winfo_height() > 1 else self._current_height

        requires_recoloring = self._draw_engine.draw_rounded_rect_with_border(
            current_w,
            current_h,
            self._apply_widget_scaling(self._corner_radius),
            0
        )

        if no_color_updates is False or requires_recoloring:
            self._canvas.itemconfig("inner_parts",
                                    outline=self._apply_appearance_mode(self._fg_color),
                                    fill=self._apply_appearance_mode(self._fg_color))

    def configure(self, require_redraw=False, **kwargs):
        """ Reconfigures structural/theming elements (length, width, corner_radius, bg_color, fg_color) """
        if "height" in kwargs:
            raise ValueError("Cannot modify directly the height of the widget. Use length and width arguments instead.")

        if "length" in kwargs or "width" in kwargs:
            width, height = None, None

            if "length" in kwargs:
                if self._orientation == "vertical":
                    height = kwargs.pop("length")
                else:
                    width = kwargs.pop("length")
            if "width" in kwargs:
                if self._orientation == "vertical":
                    width = kwargs.pop("width")
                else:
                    height = kwargs.pop("width")

            if width is not None:
                kwargs["width"] = width
            if height is not None:
                kwargs["height"] = height

        if "corner_radius" in kwargs:
            corner_radius = kwargs.pop("corner_radius")
            if type(corner_radius) is int:
                self._corner_radius = corner_radius
                require_redraw = True
            elif corner_radius is None:
                self._corner_radius = 1000
                require_redraw = True
            else:
                raise ValueError(f"corner_radius should be int or NoneType, not {type(corner_radius)}")

        if "fg_color" in kwargs:
            fg_color = kwargs.pop("fg_color")
            if isinstance(fg_color, (str, Tuple[str, str])):
                self._fg_color = self._check_color_type(fg_color)
                require_redraw = True
            elif fg_color is None:
                # Re-fetch default theme settings upon null request
                default_fg = THEME_DEFAULTS.get("sCTkSeparator", {}).get("fg_color")
                self._fg_color = self._check_color_type(default_fg)
                require_redraw = True
            else:
                raise ValueError(f"fg_color should be str, Tuple[str, str] or NoneType, not {type(fg_color)}")

        super().configure(require_redraw=require_redraw, **kwargs)

    def cget(self, attribute_name: str):
        """ Returns structural or styling custom attributes """
        if attribute_name == "height":
            raise ValueError("Cannot directly get height of the widget. Use length and width arguments instead.")
        elif attribute_name == "length":
            return self._desired_height if self._orientation == "vertical" else self._desired_width
        elif attribute_name == "width":
            return self._desired_width if self._orientation == "vertical" else self._desired_height
        elif attribute_name == "corner_radius":
            return self._corner_radius
        elif attribute_name == "fg_color":
            return self._fg_color
        elif attribute_name == "orientation":
            return self._orientation
        else:
            return super().cget(attribute_name)

    def bind(self, sequence=None, command=None, add=True):
        if not (add == "+" or add is True):
            raise ValueError("'add' argument can only be '+' or True to preserve internal callbacks")
        self._canvas.bind(sequence, command, add=True)

    def unbind(self, sequence=None, funcid=None):
        if funcid is not None:
            raise ValueError("'funcid' argument can only be None")
        self._canvas.unbind(sequence, None)


from sCTkFrame import sCTkFrame
from sCTkButtonPrimary import sCTkButtonPrimary

# ==========================================
#   Main Execution Entry Point
# ==========================================
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("sCTkSeparator (System Themed Build)")
    root.geometry("600x500")

    # ------------------------------------------
    #   Grid Layout Panel
    # ------------------------------------------
    grid_Frame = sCTkFrame(root)
    grid_Frame.pack(side="top", fill="both", expand=True, padx=25, pady=(15, 0))

    grid_Frame.grid_columnconfigure(0, weight=1)
    grid_Frame.grid_columnconfigure(1, weight=0)
    grid_Frame.grid_columnconfigure(2, weight=1)

    grid_Frame.grid_rowconfigure(0, weight=1)
    grid_Frame.grid_rowconfigure(1, weight=1)

    b1 = sCTkButtonPrimary(grid_Frame, text="First Grid button", width=200)
    b1.grid(row=0, column=0, padx=5, pady=5, sticky="nswe")

    b3 = sCTkButtonPrimary(grid_Frame, text="Third Grid button", width=200)
    b3.grid(row=1, column=0, padx=5, pady=5, sticky="nswe")

    sep = sCTkSeparator(grid_Frame, orientation="vertical", width=4)
    sep.grid(row=0, column=1, padx=8, rowspan=2, sticky="ns", pady=5)

    b2 = sCTkButtonPrimary(grid_Frame, text="Second Grid Button", width=200)
    b2.grid(row=0, column=2, padx=5, pady=5, sticky="nswe")

    b4 = sCTkButtonPrimary(grid_Frame, text="Fourth Grid Button", width=200)
    b4.grid(row=1, column=2, padx=5, pady=5, sticky="nswe")

    # ------------------------------------------
    #   Horizontal Middle Divider Line
    # ------------------------------------------
    sepHorizontal = sCTkSeparator(root, orientation="horizontal", width=4)
    sepHorizontal.pack(side="top", fill="x", pady=15, padx=25)

    # ------------------------------------------
    #   Pack Layout Panel
    # ------------------------------------------
    pack_frame = sCTkFrame(root)
    pack_frame.pack(side="bottom", fill="both", expand=True, pady=(0, 25), padx=25)

    left_column = sCTkFrame(pack_frame)
    left_column.pack(side="left", fill="both", expand=True)

    sep2 = sCTkSeparator(pack_frame, orientation="vertical", width=4)
    sep2.pack(side="left", fill="y", padx=5, pady=5)

    right_column = sCTkFrame(pack_frame)
    right_column.pack(side="right", fill="both", expand=True)

    b1_pack = sCTkButtonPrimary(left_column, text="First Pack Button", width=200)
    b1_pack.pack(side="top", fill="both", expand=True, padx=5, pady=5)

    b3_pack = sCTkButtonPrimary(right_column, text="Third Pack Button", width=200)
    b3_pack.pack(side="top", fill="both", expand=True, padx=5, pady=5)

    b2_pack = ctk.CTkButton(left_column, text="Second Pack Button", width=200)
    b2_pack.pack(side="bottom", fill="both", expand=True, padx=5, pady=5)

    b4_pack = sCTkButtonPrimary(right_column, text="Fourth Pack Button", width=200)
    b4_pack.pack(side="bottom", fill="both", expand=True, padx=5, pady=5)

    root.mainloop()

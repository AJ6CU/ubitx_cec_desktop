#
# Derived from Selector class by Fastattack, 2024).
# https://github.com/fastattackv/MoreCustomTkinterWidgets
#

import customtkinter as ctk
from typing import Literal, Union, Tuple, Optional
from sCTkThemes import THEME_DEFAULTS
from ThemeableWidget import ThemeableWidget


class sCTkSeparator(ctk.CTkBaseClass, ThemeableWidget):
    """
    Advanced Separator widget supporting custom section header text,
    dashed line patterns, corner roundness, and responsive orientation modes.
    """

    def __init__(self,
                 master: any,
                 length: int = 100,
                 width: float = 4,
                 corner_radius: Optional[int] = None,
                 bg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 orientation: Literal["vertical", "horizontal"] = "vertical",
                 text: str = "",
                 font: Optional[Union[tuple, ctk.CTkFont]] = None,
                 text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 dash: Optional[Tuple[int, ...]] = None
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
        self._orientation = orientation
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

        # 6. Extract font and text styling attributes directly from the ThemeableWidget dictionary output layer
        self._text = text
        self._font = font if font is not None else self.final_kw.get("font", ("Arial", 11, "bold"))

        if text_color is not None:
            self._text_color = self._check_color_type(text_color)
        else:
            fallback_text_color = self.final_kw.get("text_color", ctk.ThemeManager.theme["CTkLabel"]["text_color"])
            self._text_color = self._check_color_type(fallback_text_color)

        self._dash = dash

        # 7. Canvas and render configurations
        self._canvas = ctk.CTkCanvas(self, highlightthickness=0)
        self._canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self._draw_engine = ctk.DrawEngine(self._canvas)

        # 8. Bind layout adjustments to bypass CTkBaseClass strict bind filters safely
        super(ctk.CTkBaseClass, self).bind("<Configure>", lambda e: self._draw(), add="+")

        # 9. Trigger the initial render loop pass
        self._draw(no_color_updates=True)

    def _draw(self, no_color_updates=False):
        super()._draw(no_color_updates)
        current_w = self.winfo_width() if self.winfo_width() > 1 else self._current_width
        current_h = self.winfo_height() if self.winfo_height() > 1 else self._current_height
        self._canvas.delete("all")

        detected_bg = self._detect_color_of_master()
        if detected_bg == "transparent" or detected_bg is None:
            detected_bg = ctk.ThemeManager.theme["CTk"]["fg_color"]

        fg_rendered = self._apply_appearance_mode(self._fg_color)
        self._canvas.configure(bg=self._apply_appearance_mode(detected_bg))

        # FIX: Explicitly clamp the baseline dash line thickness to the intended 4px / 6px configuration.
        # This completely strips out the inflated text window dimensions inside Pygubu's editor view.
        if self._orientation == "horizontal":
            # For a horizontal line, thickness is the true minimal vertical allocation height profile
            line_thickness = self._current_height if self._current_height < current_h else 4
            if line_thickness > 10:  # Safety guard if Pygubu hardcoded the widget height attributes
                line_thickness = 4
        else:
            # For a vertical line, thickness is the true minimal horizontal allocation width profile
            line_thickness = self._current_width if self._current_width < current_w else 4
            if line_thickness > 10:
                line_thickness = 4

        if self._text:
            t_id = self._canvas.create_text(
                current_w / 2, current_h / 2,
                text=self._text,
                font=self._font,
                fill=self._apply_appearance_mode(self._text_color)
            )
            bbox = self._canvas.bbox(t_id)
            if bbox:
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                # Apply safe padding buffers around the text block
                tw, th = text_width + 16, text_height + 8

                # Calculate the exact center bounding box coordinates for the text frame capsule
                x1 = (current_w / 2) - (tw / 2)
                x2 = (current_w / 2) + (tw / 2)

                if self._orientation == "horizontal":
                    y1 = 1
                    y2 = current_h - 1

                    # Draw vertical left and right brackets bounding the horizontal text split
                    self._canvas.create_line(x1, y1, x1, y2, fill=fg_rendered, width=2)
                    self._canvas.create_line(x2, y1, x2, y2, fill=fg_rendered, width=2)

                    mid_y = current_h / 2
                    # Use the isolated, safe line_thickness to force thin dashes
                    self._canvas.create_line(0, mid_y, x1, mid_y, fill=fg_rendered, width=line_thickness,
                                             dash=self._dash)
                    self._canvas.create_line(x2, mid_y, current_w, mid_y, fill=fg_rendered, width=line_thickness,
                                             dash=self._dash)
                else:
                    # Vertical mode capsule coordinates
                    y1 = (current_h / 2) - (th / 2)
                    y2 = (current_h / 2) + (th / 2)

                    self._canvas.create_line(x1, y1, x2, y1, fill=fg_rendered, width=2)  # Top border cap line
                    self._canvas.create_line(x1, y2, x2, y2, fill=fg_rendered, width=2)  # Bottom border cap line

                    mid_x = current_w / 2
                    self._canvas.create_line(mid_x, 0, mid_x, y1, fill=fg_rendered, width=line_thickness,
                                             dash=self._dash)
                    self._canvas.create_line(mid_x, y2, mid_x, current_h, fill=fg_rendered, width=line_thickness,
                                             dash=self._dash)
        else:
            if self._dash:
                if self._orientation == "horizontal":
                    self._canvas.create_line(0, current_h / 2, current_w, current_h / 2, fill=fg_rendered,
                                             width=line_thickness, dash=self._dash)
                else:
                    self._canvas.create_line(current_w / 2, 0, current_w / 2, current_h, fill=fg_rendered,
                                             width=line_thickness, dash=self._dash)
            else:
                self._draw_engine.draw_rounded_rect_with_border(current_w, current_h,
                                                                self._apply_widget_scaling(self._corner_radius), 0)
                self._canvas.itemconfig("inner_parts", outline=fg_rendered, fill=fg_rendered)

    def configure(self, require_redraw=False, **kwargs):
        if "height" in kwargs: raise ValueError("Modify length/width arguments instead of height.")
        if "text" in kwargs: self._text, require_redraw = kwargs.pop("text"), True
        if "dash" in kwargs:
            v = kwargs.pop("dash")
            self._dash = tuple(
                int(x.strip()) for x in v.replace("(", "").replace(")", "").split(",") if x.strip()) if isinstance(v,
                                                                                                                   str) else v
            require_redraw = True

        t_orient = kwargs.pop("orientation", self._orientation)
        l_val = kwargs.pop("length", self._desired_height if self._orientation == "vertical" else self._desired_width)
        w_val = kwargs.pop("width", self._desired_width if self._orientation == "vertical" else self._desired_height)

        if t_orient != self._orientation:
            self._orientation = t_orient
            kwargs["width"], kwargs["height"] = (w_val, l_val) if self._orientation == "vertical" else (l_val, w_val)
            require_redraw = True
        else:
            kwargs["width"], kwargs["height"] = (w_val, l_val) if self._orientation == "vertical" else (l_val, w_val)
            if kwargs["width"] != self._desired_width or kwargs["height"] != self._desired_height: require_redraw = True

        if "corner_radius" in kwargs: self._corner_radius, require_redraw = kwargs.pop("corner_radius") or 1000, True
        if "fg_color" in kwargs: self._fg_color, require_redraw = self._check_color_type(
            kwargs.pop("fg_color") or THEME_DEFAULTS.get("sCTkSeparator", {}).get("fg_color")), True

        super().configure(require_redraw=require_redraw, **kwargs)

    def cget(self, attribute_name: str):
        if attribute_name == "height": raise ValueError("Use length and width arguments instead.")
        mapping = {"length": self._desired_height if self._orientation == "vertical" else self._desired_width,
                   "width": self._desired_width if self._orientation == "vertical" else self._desired_height,
                   "corner_radius": self._corner_radius, "fg_color": self._fg_color, "orientation": self._orientation,
                   "text": self._text, "dash": self._dash}
        return mapping.get(attribute_name, super().cget(attribute_name))

    # =========================================================================
    #   FIX: BIND & UNBIND ROUTING FOR PYGUBU PREVIEW SELECTION SAFETY
    # =========================================================================
    def bind(self, sequence=None, command=None, add=True):
        """ Redirects event hooks safely to the canvas to satisfy Pygubu click selections. """
        if not (add == "+" or add is True):
            raise ValueError("'add' argument can only be '+' or True to preserve internal callbacks")
        self._canvas.bind(sequence, command, add=True)

    def unbind(self, sequence=None, funcid=None):
        """ Redirects unbind hooks safely down to the inner canvas instance. """
        if funcid is not None:
            raise ValueError("'funcid' argument can only be None")
        self._canvas.unbind(sequence, None)


# ==========================================
#   MAIN TESTING RUNNER CODE BLOCK
# ==========================================
if __name__ == "__main__":
    if "sCTkSeparator" not in THEME_DEFAULTS:
        THEME_DEFAULTS["sCTkSeparator"] = {
            "fg_color": ("#BABABA", "#565B5E"),
            "bg_color": "transparent",
            "corner_radius": 6
        }

    root = ctk.CTk()
    root.title("sCTkSeparator Feature Test Environment")
    root.geometry("600x450")

    grid_Frame = ctk.CTkFrame(root)
    grid_Frame.pack(side="top", fill="both", expand=True, padx=20, pady=15)

    grid_Frame.grid_columnconfigure(0, weight=1)
    grid_Frame.grid_columnconfigure(1, weight=0)
    grid_Frame.grid_columnconfigure(2, weight=1)
    grid_Frame.grid_rowconfigure(0, weight=1)

    lbl_left = ctk.CTkLabel(grid_Frame, text="Left Sub-Panel Group Data")
    lbl_left.grid(row=0, column=0, sticky="nswe")

    sep_vertical_text = sCTkSeparator(grid_Frame, orientation="vertical", text="CORE API", width=4)
    sep_vertical_text.grid(row=0, column=1, sticky="ns", padx=10, pady=10)

    lbl_right = ctk.CTkLabel(grid_Frame, text="Right Sub-Panel Group Data")
    lbl_right.grid(row=0, column=2, sticky="nswe")

    sep_horizontal_text = sCTkSeparator(root, orientation="horizontal", text="SYSTEM DASH SEPARATOR SECTION", width=4)
    sep_horizontal_text.pack(side="top", fill="x", padx=20, pady=10)

    pack_frame = ctk.CTkFrame(root)
    pack_frame.pack(side="bottom", fill="both", expand=True, padx=20, pady=(5, 20))

    panel_a = ctk.CTkLabel(pack_frame, text="System Input Options")
    panel_a.pack(side="left", fill="both", expand=True)

    sep_dashed = sCTkSeparator(pack_frame, orientation="vertical", width=4, dash=(4, 4))
    sep_dashed.pack(side="left", fill="y", padx=10, pady=15)

    panel_b = ctk.CTkLabel(pack_frame, text="System Output Channels")
    panel_b.pack(side="right", fill="both", expand=True)

    root.mainloop()

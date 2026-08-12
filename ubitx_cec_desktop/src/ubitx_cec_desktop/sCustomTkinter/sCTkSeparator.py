import customtkinter as ctk
from typing import Literal, Union, Tuple, Optional
from sCTkButtonPrimary import sCTkButtonPrimary
from sCTkFrame import sCTkFrame


class sCTkSeparator(ctk.CTkBaseClass):
    """
    Separator widget to mark a separation between 2 other widgets.
    Using Separator.pack(expand=True, fill="both") or Separator.grid(sticky="nswe") doesn't work for now: you have to enter the size of the separator manually.
    """

    def __init__(self,
                 master: any,
                 length: int = 100,
                 width: float = 4,
                 corner_radius: Optional[int] = None,
                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 orientation: Literal["vertical", "horizontal"] = "vertical"
                 ):

        if orientation == "vertical":
            height = length
        elif orientation == "horizontal":
            height = width
            width = length
        else:
            raise ValueError(f"The value for orientation is incorrect: \"{orientation}\". Should be \"vertical\" or \"horizontal\"")

        super().__init__(master=master, width=width, height=height, bg_color=bg_color)

        self._corner_radius = 6 if corner_radius is None else corner_radius
        self._fg_color = ctk.ThemeManager.theme["CTkFrame"]["border_color"] if fg_color is None else self._check_color_type(fg_color)
        self._orientation = orientation

        self._canvas = ctk.CTkCanvas(self, highlightthickness=0)
        self._canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self._canvas.configure(bg=self._apply_appearance_mode(self._detect_color_of_master()), width=self._apply_widget_scaling(width), height=self._apply_widget_scaling(height))
        self._draw_engine = ctk.DrawEngine(self._canvas)

        self._draw(no_color_updates=True)

    def _set_scaling(self, *args, **kwargs):
        super()._set_scaling(*args, **kwargs)

        self._canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                               height=self._apply_widget_scaling(self._desired_height))
        self._draw()

    def _set_dimensions(self, width=None, height=None):
        super()._set_dimensions(width, height)

        self._canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                               height=self._apply_widget_scaling(self._desired_height))
        self._draw()

    def _draw(self, no_color_updates=False):
        super()._draw(no_color_updates)

        requires_recoloring = self._draw_engine.draw_rounded_rect_with_border(self._apply_widget_scaling(self._current_width),
                                                                              self._apply_widget_scaling(self._current_height),
                                                                              self._apply_widget_scaling(self._corner_radius),
                                                                              0,
                                                                              )

        if no_color_updates is False or requires_recoloring:
            self._canvas.itemconfig("inner_parts",
                                    outline=self._apply_appearance_mode(self._fg_color),
                                    fill=self._apply_appearance_mode(self._fg_color))

    def configure(self, require_redraw=False, **kwargs):
        """ Reconfigures the given arguments (length, width, corner_radius, bg_color, fg_color) """
        if "height" in kwargs:
            raise ValueError("Cannot modify directly the height of the widget. Use the length and width arguments instead.")

        if "length" in kwargs or "width" in kwargs:
            width, height = None, None

            if "length" in kwargs:
                if self._orientation == "vertical":
                    height = kwargs.pop("length")
                else:  # horizontal
                    width = kwargs.pop("length")
            if "width" in kwargs:
                if self._orientation == "vertical":
                    width = kwargs.pop("width")
                else:  # horizontal
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
                self._fg_color = ctk.ThemeManager.theme["CTkFrame"]["border_color"]
                require_redraw = True
            else:
                raise ValueError(f"fg_color should be str, Tuple[str, str] or NoneType, not {type(fg_color)}")

        super().configure(require_redraw=require_redraw, **kwargs)

    def cget(self, attribute_name: str):
        """ Returns the value of the given argument (length, width, corner_radius, fg_color, orientation, bg_color) """
        if attribute_name == "height":
            raise ValueError("Cannot directly get height of the widget. Use the length and width arguments instead.")

        elif attribute_name == "length":
            if self._orientation == "vertical":
                return self._desired_height
            else:
                return self._desired_width

        elif attribute_name == "width":
            if self._orientation == "vertical":
                return self._desired_width
            else:
                return self._desired_height

        elif attribute_name == "corner_radius":
            return self._corner_radius

        elif attribute_name == "fg_color":
            return self._fg_color

        elif attribute_name == "orientation":
            return self._orientation

        else:
            return super().cget(attribute_name)

    def bind(self, sequence=None, command=None, add=True):
        """ called on the tkinter.Canvas """
        if not (add == "+" or add is True):
            raise ValueError("'add' argument can only be '+' or True to preserve internal callbacks")
        self._canvas.bind(sequence, command, add=True)

    def unbind(self, sequence=None, funcid=None):
        """ called on the tkinter.Canvas """
        if funcid is not None:
            raise ValueError("'funcid' argument can only be None, because there is a bug in" +
                             " tkinter and its not clear whether the internal callbacks will be unbinded or not")
        self._canvas.unbind(sequence, None)

if __name__ == "__main__":


    root = ctk.CTk()
    root.title("sCTkSeperator examples")
    
    #
    #   Grid
    #

    grid_Frame = sCTkFrame(root)
    grid_Frame.pack(side="top", fill="both", expand=True, padx=25, pady=(15,0))


    b1 = sCTkButtonPrimary(grid_Frame, text="First Grid button", width=200)
    b1.grid(row=0, column=0, padx=5, pady=5)

    b3 = sCTkButtonPrimary(grid_Frame, text="Third Grid button", width=200)
    b3.grid(row=1, column=0, padx=5, pady=5)

    sep = sCTkSeparator(grid_Frame, orientation="vertical")
    sep.grid(row=0, column=1, padx=8, rowspan=2,sticky="ns", pady=25)

    b2 = sCTkButtonPrimary(grid_Frame, text="Second Grid Button", width=200)
    b2.grid(row=0, column=2, padx=5, pady=5)

    b4 = sCTkButtonPrimary(grid_Frame, text="Fourth Grid Button", width=200)
    b4.grid(row=1, column=2, padx=5, pady=5)
    #
    #   Horizontal spacer
    #

    sepHorizontal = sCTkSeparator(root, orientation="horizontal")
    sepHorizontal.pack(side="top", fill="both", expand=True, pady=(10,0), padx=5)

    #
    #   Pack
    #

    pack_frame = ctk.CTkFrame(root)
    pack_frame.pack(side="bottom", fill="both", expand=True, pady=25, padx=25)

    left_column= ctk.CTkFrame(pack_frame)
    left_column.pack(side="left", fill="both", expand="True")

    sep = sCTkSeparator(pack_frame, orientation="vertical")
    sep.pack(side="left", fill="y", padx=5, pady=5)

    right_column = ctk.CTkFrame(pack_frame)
    right_column.pack(side="right", fill="both", expand=True)

    b1 = sCTkButtonPrimary(left_column, text="First Pack Button", width=200)
    b1.pack(side="top", anchor="nw", padx=5, pady=5)

    b3 = sCTkButtonPrimary(right_column, text="Third Pack Button", width=200)
    b3.pack(side="top", anchor="ne", padx=5, pady=5)



    b2 = sCTkButtonPrimary(left_column, text="Second Pack Button", width=200)
    b2.pack(side="bottom", anchor="sw", padx=5, pady=5)

    b4 = sCTkButtonPrimary(right_column, text="Fourth Pack Button", width=200)
    b4.pack(side="bottom", anchor="se", padx=5, pady=5)
    
    

    root.mainloop()
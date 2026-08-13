import customtkinter as ctk
import os
import textwrap
from PIL import Image
from typing import Literal, Union, Tuple, Optional

# Import your system's shared configuration architecture and components
from sCTkThemes import THEME_DEFAULTS
from ThemeableWidget import ThemeableWidget

# Assuming your primary components reside within your sCustomTkinter package structure
from sCTkButtonPrimary import sCTkButtonPrimary
from sCTkButtonSecondary import sCTkButtonSecondary
from sCTkLabelPrimary import sCTkLabelPrimary


class sCTkMessage(ctk.CTkToplevel, ThemeableWidget):
    """
    Advanced themeable message dialog window.
    Supports customizable single prompt text or dual choice prompts returning boolean states.
    """

    def __init__(self,
                 title: str,
                 message: str,
                 typ: Literal["info", "warning", "error"],
                 master: any = None,
                 buttons: Literal["ok", "yes_no"] = "ok",
                 ok_text: str = "Ok",  # NEW: Allows custom text for the single button view
                 yes_text: str = "Yes",
                 no_text: str = "No",
                 width: int = 400,
                 *args, **kwargs):
        """TopLevel widget already configured for displaying messages"""

        # 1. Capture initialization parameters into a localized dictionary for processing
        local_kwargs = {}

        # 2. Invoke the ThemeableWidget engine to scrub parameters and construct self.final_kw
        ThemeableWidget.__init__(
            self,
            theme_defaults=THEME_DEFAULTS.get("sCTkMessage", {}),
            kwargs=local_kwargs
        )

        # 3. Extract base initialization top-level configurations
        super().__init__(master=master, *args, **kwargs)

        # Internal result storage container initialized to None
        self._result: Optional[bool] = None

        self.lift()  # Lift window on top
        self.attributes("-topmost", True)  # Stay on top
        self.resizable(False, False)
        self.grab_set()  # Make other windows not clickable
        self.title(title)

        # 4. Pull typography configs out of your localized ThemeableWidget stylesheet layers
        font_config = self.final_kw.get("font", ("Arial", 14))
        text_color_config = self.final_kw.get("text_color", ("#1A1A1A", "#E5E5E5"))

        # 5. Custom Local Icon Asset Extraction
        images_dir = os.path.join(os.path.dirname(__file__), "images")
        light_icon_path = os.path.join(images_dir, f"{typ}.png")
        dark_icon_path = os.path.join(images_dir, f"{typ}_dark.png")

        if not os.path.exists(dark_icon_path):
            dark_icon_path = light_icon_path

        if os.path.exists(light_icon_path):
            pil_light = Image.open(light_icon_path)
            pil_dark = Image.open(dark_icon_path)

            ctk_image = ctk.CTkImage(light_image=pil_light, dark_image=pil_dark, size=(85, 85))
            self.image_label = sCTkLabelPrimary(self, text="", image=ctk_image, width=85, height=85)
            self.image_label.grid(row=0, column=0, padx=(15, 5), pady=20, sticky="n")
        else:
            self.image_label = sCTkLabelPrimary(self, text=f"[{typ.upper()}]", font=("Arial", 12, "bold"))
            self.image_label.grid(row=0, column=0, padx=(15, 5), pady=20, sticky="n")

        # 6. Calculate text width line character boundaries dynamically
        char_width_estimate = 11.5
        max_text_width_pixels = width - 180
        char_limit_per_line = max(20, int(max_text_width_pixels / char_width_estimate))

        # Split paragraph on strict word boundaries inserting real '\n' newline feeds
        wrapped_message = "\n".join(textwrap.wrap(message, width=char_limit_per_line))

        self.label = sCTkLabelPrimary(
            self,
            text=wrapped_message,
            font=font_config,
            text_color=text_color_config,
            justify="left",
            anchor="w",
            wraplength=max_text_width_pixels
        )
        self.label.grid(row=0, column=1, padx=(10, 35), pady=20, sticky="w")

        # 7. Action Button Panel Layout Mapping
        if buttons == "yes_no":
            self.yes_button = sCTkButtonPrimary(self, text=yes_text, command=self.on_yes)
            self.yes_button.grid(row=1, column=0, padx=(15, 5), pady=15, sticky="ew")

            self.no_button = sCTkButtonSecondary(self, text=no_text, command=self.on_no)
            self.no_button.grid(row=1, column=1, padx=(5, 15), pady=15, sticky="ew")

            self.bind("<Return>", self.on_yes)

            self.grid_columnconfigure(0, weight=1, uniform="dialog_buttons")
            self.grid_columnconfigure(1, weight=1, uniform="dialog_buttons")
        else:
            # FIX: Dynamically wire the ok_text property configuration into the constructor
            self.ok_button = sCTkButtonPrimary(self, text=ok_text, command=self.on_ok)
            self.ok_button.grid(row=1, column=0, columnspan=2, padx=15, pady=15)
            self.bind("<Return>", self.on_ok)

            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=1)

        # 8. Automated screen centering calculation pass
        self._center_window(target_width=width)

    def _center_window(self, target_width: int):
        """Calculates geometry parameters to position the popup exactly centered using target metrics."""
        self.update_idletasks()
        width = target_width
        height = self.winfo_reqheight()

        if self.master and hasattr(self.master, "winfo_x"):
            x = self.master.winfo_x() + (self.master.winfo_width() // 2) - (width // 2)
            y = self.master.winfo_y() + (self.master.winfo_height() // 2) - (height // 2)
        else:
            x = (self.winfo_screenwidth() // 2) - (width // 2)
            y = (self.winfo_screenheight() // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{max(0, x)}+{max(0, y)}")

    def _close_dialog(self):
        """Internal cleanup sequence."""
        self.grab_release()
        self.destroy()

    def on_ok(self, event=None):
        self._result = True
        self._close_dialog()

    def on_yes(self, event=None):
        self._result = True
        self._close_dialog()

    def on_no(self, event=None):
        self._result = False
        self._close_dialog()

    def wait_end(self) -> Optional[bool]:
        """ When called, waits until the message is closed and returns the choice boolean result """
        if self.master:
            self.master.wait_window(self)
        else:
            self.wait_window(self)
        return self._result


# ==========================================
#   Global Functional Helper Interfaces
# ==========================================

# Functional shortcut extensions updated to safely support custom ok_text strings

def showinfo(title: str, message: str, ok_text: str = "Ok", width: int = 400, master: any = None) -> Optional[bool]:
    m = sCTkMessage(title, message, "info", master=master, buttons="ok", ok_text=ok_text, width=width)
    return m.wait_end()


def showwarning(title: str, message: str, ok_text: str = "Ok", width: int = 400, master: any = None) -> Optional[bool]:
    m = sCTkMessage(title, message, "warning", master=master, buttons="ok", ok_text=ok_text, width=width)
    return m.wait_end()


def showerror(title: str, message: str, ok_text: str = "Ok", width: int = 400, master: any = None) -> Optional[bool]:
    m = sCTkMessage(title, message, "error", master=master, buttons="ok", ok_text=ok_text, width=width)
    return m.wait_end()


def askyesno(title: str, message: str, yes_text: str = "Yes", no_text: str = "No", width: int = 400,
             master: any = None) -> bool:
    m = sCTkMessage(title, message, "info", master=master, buttons="yes_no", yes_text=yes_text, no_text=no_text,
                    width=width)
    val = m.wait_end()
    return True if val is True else False


def askwarningyesno(title: str, message: str, yes_text: str = "Yes", no_text: str = "No", width: int = 400,
                    master: any = None) -> bool:
    m = sCTkMessage(title, message, "warning", master=master, buttons="yes_no", yes_text=yes_text, no_text=no_text,
                    width=width)
    val = m.wait_end()
    return True if val is True else False


def askerroryesno(title: str, message: str, yes_text: str = "Yes", no_text: str = "No", width: int = 400,
                  master: any = None) -> bool:
    m = sCTkMessage(title, message, "error", master=master, buttons="yes_no", yes_text=yes_text, no_text=no_text,
                    width=width)
    val = m.wait_end()
    return True if val is True else False
# ==========================================
#   MAIN RUNNER TESTING ENVIRONMENT
# ==========================================
if __name__ == "__main__":
    import customtkinter as ctk

    root = ctk.CTk()
    root.geometry("300x520")
    root.title("Message Example")

    long_msg = "Warning: The VFO phase lock loop has lost lock synchronization with the master synthesizer. Continuous operation may contaminate adjacent radio channels. Do you wish to override?"

    def trigger_info_ask():
        ans = askyesno("Info Query", "Do you wish to log parameter data strings?", yes_text="Log Data", no_text="Skip", master=root)
        print(f"Info Yes/No Feedback evaluated to: {ans}")

    def trigger_warning_ask():
        ans = askwarningyesno("Band Switch Warning", long_msg, yes_text="Override", no_text="Disconnect", width=450, master=root)
        print(f"Warning Yes/No Feedback evaluated to: {ans}")

    def trigger_error_ask():
        ans = askerroryesno("Fatal Overload Error", "VFO buffer cascade encountered. Attempt cold reset?", yes_text="Reset Buffer", no_text="Terminate", master=root)
        print(f"Error Yes/No Feedback evaluated to: {ans}")

    # ----------------------------------------------------
    #   1. INFO ALERT SECTION (Testing custom ok_text text!)
    # ----------------------------------------------------
    sCTkButtonPrimary(root, text="Test Info (OK)", width=200,
                      command=lambda: showinfo("Message Example", "Short statement info alert box.", ok_text="Acknowledge", master=root)).pack(pady=8)
    sCTkButtonPrimary(root, text="Test Info (Yes/No)", width=200,
                      command=trigger_info_ask).pack(pady=(8, 25))

    # ----------------------------------------------------
    #   2. WARNING ALERT SECTION
    # ----------------------------------------------------
    sCTkButtonPrimary(root, text="Test Warning (OK)", width=200,
                      command=lambda: showwarning("Warning", "Listen carefully", ok_text="Proceed", master=root)).pack(pady=8)
    sCTkButtonPrimary(root, text="Test Warning (Yes/No)", width=200,
                      command=trigger_warning_ask).pack(pady=(8, 25))

    # ----------------------------------------------------
    #   3. ERROR ALERT SECTION
    # ----------------------------------------------------
    sCTkButtonPrimary(root, text="Test Error (OK)", width=200,
                      command=lambda: showerror("Error", "Dead meat", ok_text="Close", master=root)).pack(pady=8)
    sCTkButtonPrimary(root, text="Test Error (Yes/No)", width=200,
                      command=trigger_error_ask).pack(pady=8)

    root.mainloop()

#!/usr/bin/python3
"""
sCTkFileExplorer - Part 1 of 4

A fully stylized, theme-compliant CustomTkinter file system navigation panel.
Unselectable files/folders are dynamically dimmed and unclickable.
Handles standalone panel embed loops with single and double click callbacks.
"""
import os
import sys
import platform
import time
import ast
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from typing import Literal, Optional, Union, Tuple

from sCTkThemes import THEME_DEFAULTS
from ThemeableWidget import ThemeableWidget


class sCTkFileExplorer(ctk.CTkFrame, ThemeableWidget):
    _MANAGED_PROPERTIES = frozenset({"initialdir", "initialfile", "type", "title", "filetypes", "defaultextension"})

    def __init__(self,
                 master: any,
                 type: Literal["file", "directory"] = "directory",
                 filetypes: list[str] = None,
                 initialdir: str = None,
                 initialfile: str = None,
                 command: Optional[callable] = None,
                 double_click_command: Optional[callable] = None,
                 width: int = 400,
                 height: int = 300,
                 corner_radius: Optional[Union[int, str]] = None,
                 border_width: Optional[Union[int, str]] = None,
                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 border_color: Optional[Union[str, Tuple[str, str]]] = None,
                 background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,
                 overwrite_preferred_drawing_method: Union[str, None] = None,
                 **kwargs):

        # Cleanse incoming custom dictionary parameters to protect framework from core argument leaks
        kwargs.pop("initialdir", None)
        kwargs.pop("initialfile", None)
        kwargs.pop("type", None)
        kwargs.pop("filetypes", None)
        kwargs.pop("defaultextension", None)
        kwargs.pop("title", None)

        # Capture and pop the visual interaction state attribute if passed directly from Pygubu xml files
        self._initial_state_seed = str(kwargs.pop("state", "normal")).lower()

        theme_defaults = THEME_DEFAULTS.get("sCTkFileExplorer", {})
        ThemeableWidget.__init__(self, theme_defaults, kwargs)

        # Initialize base frame container safely with a perfectly sanitized kwargs package pass
        super().__init__(master, width=width, height=height, corner_radius=corner_radius,
                         border_width=border_width, bg_color=bg_color, fg_color=fg_color,
                         border_color=border_color, background_corner_colors=background_corner_colors,
                         overwrite_preferred_drawing_method=overwrite_preferred_drawing_method, **kwargs)

        self.response_type = type.lower()
        self.change_path = True
        self.item_labels = {}
        self.command = command
        self.double_click_command = double_click_command
        self._last_double_click_time = 0.0

        self._desired_width = width
        self._desired_height = height

        self.filetypes = []
        if filetypes:
            if self.response_type != "file":
                raise ValueError(
                    "Cannot provide 'filetypes' constraint array filter maps when widget mode is 'directory'.")

            if isinstance(filetypes, str):
                cleaned_str = filetypes.strip()
                if not (cleaned_str.startswith("[") and cleaned_str.endswith("]")):
                    raise ValueError(
                        f"Malformed filetypes string sequence parsed: '{filetypes}'. Must follow exact list structure syntax.")
                try:
                    processed_types = ast.literal_eval(cleaned_str)
                except Exception as err:
                    raise ValueError(
                        f"Malformed syntax encountered evaluating filetypes filter list configuration: {err}")
            else:
                processed_types = filetypes

            if not isinstance(processed_types, list):
                raise ValueError(
                    f"Invalid filetypes configuration format context: {type(processed_types)}. Target must evaluate to a list structure.")

            for f in processed_types:
                clean_f = str(f).lower().replace("*", "").strip()
                if clean_f:
                    if not clean_f.startswith("."):
                        clean_f = "." + clean_f
                    self.filetypes.append(clean_f)
        else:
            self.filetypes = None
        # Resolve starting coordinates, correcting for tilde variables upfront
        raw_file = os.path.expanduser(str(initialfile)) if initialfile else None
        raw_dir = os.path.expanduser(str(initialdir)) if initialdir else None

        if self.response_type == "directory" and raw_file:
            raw_dir = os.path.dirname(raw_file)
            raw_file = None

        if raw_dir is not None:
            init_p = raw_dir
        elif raw_file is not None:
            init_p = os.path.dirname(raw_file)
        else:
            init_p = os.getcwd()

        self.path_to_show = ctk.StringVar(self, value=os.path.normpath(os.path.abspath(init_p)))
        self.selected_path = ctk.StringVar(self, value=os.path.normpath(os.path.abspath(raw_file if raw_file else init_p)))

        self.folder_icon = "📁 "
        self.file_icon = "📄 "

        # Enforce exact dimension configurations to prevent layout canvas clipping failures
        self.top_frame = ctk.CTkFrame(self, width=self._desired_width, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.top_frame.columnconfigure(1, weight=1)

        self.back_button = ctk.CTkButton(
            self.top_frame,
            text="▲ Up",
            width=45,
            font=self.final_kw.get("btn_font"),
            fg_color=self.final_kw.get("btn_fg"),
            hover_color=self.final_kw.get("btn_hover"),
            text_color=self.final_kw.get("btn_text_color"),
            border_color=self.final_kw.get("btn_border_color")
        )
        self.back_button.grid(row=0, column=0, padx=(0, 5), sticky="nw")

        self.path_entry = ctk.CTkEntry(
            self.top_frame,
            textvariable=self.selected_path,
            font=self.final_kw.get("entry_font"),
            fg_color=self.final_kw.get("entry_fg"),
            border_color=self.final_kw.get("entry_border_color"),
            text_color=self.final_kw.get("entry_text_color")
        )
        self.path_entry.grid(row=0, column=1, sticky="ew")

        # Stretch the main container explicitly using layout grid weights to occupy available panel coordinates
        self.main_container = ctk.CTkFrame(self, width=self._desired_width, height=self._desired_height - 60)
        self.main_container.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.main_container.columnconfigure(0, weight=1)
        self.main_container.rowconfigure(0, weight=1)

        # Force structural width parameters down into canvas geometry definitions
        self.canvas = ctk.CTkCanvas(
            self.main_container,
            highlightthickness=0,
            bg=self._apply_appearance_mode(self.cget("fg_color")),
            width=self._desired_width - 30,
            height=self._desired_height - 70
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.explorer_frame = ctk.CTkFrame(self.canvas, fg_color="transparent")
        self.explorer_frame.columnconfigure(0, weight=1)

        self.y_scrollbar = ctk.CTkScrollbar(self.main_container, command=self.canvas.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.y_scrollbar.set)

        self.canvas.create_window((0, 0), window=self.explorer_frame, anchor="nw", tags="inner_window")

        self.after(10, self._finalize_split_bindings)

    # =========================================================================
    # sCTkFileExplorer - Part 3 of 4: Configuration API & State Managers
    # =========================================================================
    def _configure_frame(self, event=None):
        self.after(10, lambda: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def _user_path_changed(self, *args):
        if not self.change_path:
            return
        target = self.selected_path.get()
        if os.path.isdir(target):
            self.path_to_show.set(target)
            self._fill_explorer()

    def _on_entry_return(self):
        target = self.path_entry.get().strip()
        if os.path.exists(target):
            if os.path.isdir(target):
                self.path_to_show.set(target)
                self._fill_explorer()

    def _empty_explorer(self):
        for widget in self.explorer_frame.winfo_children():
            widget.destroy()
        self.item_labels.clear()

    def _mousewheel(self, event):
        if platform.system() == "Darwin":
            self.canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _move_back(self):
        parent = os.path.dirname(self.path_to_show.get())
        if parent != self.path_to_show.get():
            self.path_to_show.set(parent)
            self.change_path = False
            self.selected_path.set(parent)
            self.change_path = True
            self._fill_explorer()

    def _finalize_split_bindings(self):
        if hasattr(self, "back_button"):
            self.back_button.configure(command=self._move_back)
        if hasattr(self, "path_entry"):
            self.path_entry.bind("<Return>", lambda e: self._on_entry_return())
        if hasattr(self, "selected_path"):
            self.selected_path.trace_add("write", self._user_path_changed)
        if hasattr(self, "explorer_frame"):
            self.explorer_frame.bind("<Configure>", self._configure_frame)
        if hasattr(self, "canvas"):
            self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig("inner_window", width=e.width))
            self.canvas.bind_all("<MouseWheel>", self._mousewheel)

        self._fill_explorer()
        # Cleaned out initial state seed check block since state tracking is handled at the chooser level

    def configure(self, cnf=None, **kw):
        """Extended configure to handle dynamic updates and apply geometry/theme parameters."""
        if cnf is not None:
            kw = cnf | kw

        if "filetypes" in kw:
            ft_val = kw.pop("filetypes")
            if ft_val:
                if self.response_type != "file":
                    raise ValueError(
                        "Cannot provide 'filetypes' configuration filter when layout mode context is 'directory'.")
                if isinstance(ft_val, str):
                    cleaned_ft = ft_val.strip()
                    if not (cleaned_ft.startswith("[") and cleaned_ft.endswith("]")):
                        raise ValueError(f"Malformed filetypes string array configuration via configure: '{ft_val}'.")
                    try:
                        raw_types = ast.literal_eval(cleaned_ft)
                    except Exception as err:
                        raise ValueError(f"Malformed syntax encountered processing filetypes validation strings: {err}")
                else:
                    raw_types = ft_val

                if not isinstance(raw_types, list):
                    raise ValueError("Invalid filetypes format context. Must evaluate to a list layout structure.")

                self.filetypes = []
                for f in raw_types:
                    clean_f = str(f).lower().replace("*", "").strip()
                    if clean_f:
                        if not clean_f.startswith("."):
                            clean_f = "." + clean_f
                        self.filetypes.append(clean_f)
            else:
                self.filetypes = None

        if "width" in kw:
            self._desired_width = int(kw.pop("width"))
            super().configure(width=self._desired_width)
            if hasattr(self, "top_frame"): self.top_frame.configure(width=self._desired_width)
            if hasattr(self, "main_container"): self.main_container.configure(width=self._desired_width)
            if hasattr(self, "canvas"): self.canvas.configure(width=self._desired_width - 30)

        if "height" in kw:
            self._desired_height = int(kw.pop("height"))
            super().configure(height=self._desired_height)
            if hasattr(self, "main_container"): self.main_container.configure(height=self._desired_height - 60)
            if hasattr(self, "canvas"): self.canvas.configure(height=self._desired_height - 70)

        # Removed the block tracking kw.pop("state") to let the container rely cleanly on chooser-level freeze loops

        if "command" in kw: self.command = kw.pop("command")
        if "double_click_command" in kw: self.double_click_command = kw.pop("double_click_command")

        return super().configure(**kw)

    config = configure

    # =========================================================================
    # sCTkFileExplorer - Part 4 of 4: Rendering Engine & Callbacks
    # =========================================================================
    def _fill_explorer(self):
        self._empty_explorer()
        current_dir = self.path_to_show.get()
        current_selected = os.path.normpath(os.path.abspath(self.selected_path.get()))

        try:
            items = sorted(os.listdir(current_dir))
        except Exception:
            error_lbl = ctk.CTkLabel(self.explorer_frame, text="⚠️ Directory unreadable or permission denied",
                                     text_color="red")
            error_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="w")
            return

        row_idx = 0
        for item in items:
            if item.startswith('.'):
                continue
            full_path = os.path.normpath(os.path.join(current_dir, item))
            is_dir = os.path.isdir(full_path)

            is_valid_row = True
            if self.response_type == "directory" and not is_dir:
                is_valid_row = False
            elif self.response_type == "file" and not is_dir and self.filetypes:
                _, ext = os.path.splitext(item.lower())
                if ext not in self.filetypes:
                    is_valid_row = False

            icon = self.folder_icon if is_dir else self.file_icon
            is_currently_highlighted = (full_path == current_selected)

            if is_valid_row:
                txt_color = self.final_kw.get("row_active_text", self._apply_appearance_mode(
                    ctk.ThemeManager.theme["CTkLabel"]["text_color"]))
                widget_state = "normal"
                btn_bg = self.final_kw.get("btn_fg", ctk.ThemeManager.theme["CTkButton"][
                    "fg_color"]) if is_currently_highlighted else "transparent"
            else:
                txt_color = self.final_kw.get("row_dimmed_text", "gray50")
                widget_state = "disabled"
                btn_bg = "transparent"

            item_btn = ctk.CTkButton(
                self.explorer_frame,
                text=f"{icon}{item}",
                anchor="w",
                fg_color=btn_bg,
                text_color=txt_color,
                state=widget_state,
                hover_color=self.final_kw.get("btn_hover", self._apply_appearance_mode(
                    ctk.ThemeManager.theme["CTkButton"]["hover_color"])),
                command=lambda p=full_path: self._on_item_clicked(p)
            )
            item_btn.grid(row=row_idx, column=0, sticky="ew", padx=2, pady=1)

            if is_valid_row:
                item_btn.bind("<Double-Button-1>", lambda e, p=full_path: self._on_item_double_clicked(p))
                self.item_labels[full_path] = item_btn

            row_idx += 1

        self.canvas.yview_moveto(0)

    def _on_item_clicked(self, target_path):
        import time
        now = time.time()
        if (now - self._last_double_click_time) < 0.3:
            return

        target_path = os.path.normpath(target_path)
        if self.response_type == "directory" and os.path.isfile(target_path):
            target_path = os.path.dirname(target_path)

        self.change_path = False
        self.selected_path.set(target_path)
        self.change_path = True

        for path, btn in self.item_labels.items():
            if path == target_path:
                btn.configure(fg_color=self.final_kw.get("btn_fg", ctk.ThemeManager.theme["CTkButton"]["fg_color"]))
            else:
                btn.configure(fg_color="transparent")

        if self.command and callable(self.command):
            self.command(target_path)

    def _on_item_double_clicked(self, target_path):
        target_path = os.path.normpath(target_path)
        if os.path.isdir(target_path):
            self.path_to_show.set(target_path)
            self.change_path = False
            self.selected_path.set(target_path)
            self.change_path = True
            self._fill_explorer()
        else:
            if self.response_type == "directory":
                target_path = os.path.dirname(target_path)

            import time
            now = time.time()
            if (now - self._last_double_click_time) < 0.3:
                return

            self._last_double_click_time = now

            if self.double_click_command and callable(self.double_click_command):
                self.double_click_command(target_path)


if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Standalone Embedded sCTkFileExplorer Panel View")
    app.geometry("500x500")


    def track_selection(path):
        print(f"SINGLE-CLICK HIGHLIGHT: {path}")


    def execute_file(path):
        print(f"DOUBLE-CLICK CONFIRMED! Launching: {path}")


    explorer = sCTkFileExplorer(
        app,
        type="file",
        filetypes=[".py"],
        command=track_selection,
        state="disabled",
        double_click_command=execute_file
    )
    explorer.pack(fill="both", expand=True, padx=15, pady=15)
    app.mainloop()

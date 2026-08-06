#!/usr/bin/python3
"""
sCTkPathChooser

Based on Pygubu Widgets, Stylized to fit into other sCustomTkinter widget set.

UI source file: sCTkPathChooserButton.ui
"""
import os
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from sCTkThemes import THEME_DEFAULTS
from sCTkEntryPrimary import sCTkEntryPrimary
from sCTkButtonSecondary import sCTkButtonSecondary
import sCTkPathChooserui as baseui
from ThemeableWidget import ThemeableWidget


class sCTkPathChooser(baseui.sCTkPathChooserUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        # 1. Parse incoming Pygubu initialization properties safely
        self._type = str(kw.get("type", "directory") or "directory").lower()
        self._title = kw.get("title", "Select System Path Location Target")
        self._initialdir = kw.get("initialdir", os.getcwd())
        self._filetypes = kw.get("filetypes", [("All Files", "*.*")])
        self._defaultextension = kw.get("defaultextension", "")
        self._state_callback = kw.get("command", None)

        theme_defaults = THEME_DEFAULTS.get("sCTkPathChooser", {})
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize base framework safely
        super().__init__(master)

        # Snatch the initial string data layer right before clearing Pygubu's layouts
        init_path = ""
        if hasattr(super(), "get"):
            try:
                init_path = super().get()
            except Exception:
                pass
        if not init_path and self._initialdir:
            init_path = os.getcwd() if self._initialdir == "os.getcwd()" else self._initialdir

        btn_txt = self._button.cget("text") if hasattr(self, "_button") and self._button else "Browse..."
        if hasattr(self, "_button") and self._button:
            self._button.destroy()

        # Camouflage underlying Ttk Frame backing layers perfectly
        try:
            m_idx = 1 if ctk.get_appearance_mode().lower() == "dark" else 0
            target_hex = THEME_DEFAULTS.get("sCTkEntryPrimary", {}).get("fg_color", ("#FFFFFF", "#111827"))[m_idx]
            self.style = ttk.Style()
            s_name = f"sCTkPath_{id(self)}.TFrame"
            self.style.configure(s_name, background=target_hex, borderwidth=0, relief="flat")
            self.configure(style=s_name)
        except Exception:
            pass

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        # 📥 2. RE-INJECT CUSTOM CTK WIDGETS
        self.s_entry = sCTkEntryPrimary(self, font=self.final_kw.get("entry_font"),
                                        fg_color=self.final_kw.get("entry_fg"),
                                        border_color=self.final_kw.get("entry_border_color"),
                                        text_color=self.final_kw.get("entry_text_color"))
        self.s_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self.s_btn = sCTkButtonSecondary(self, text=btn_txt, font=self.final_kw.get("btn_font"),
                                         fg_color=self.final_kw.get("btn_fg"),
                                         hover_color=self.final_kw.get("btn_hover"),
                                         text_color=self.final_kw.get("btn_text_color"),
                                         border_color=self.final_kw.get("btn_border_color"), border_width=2,
                                         command=self._on_browse_clicked)
        self.s_btn.grid(row=0, column=1, sticky="ns")

        if init_path:
            self.set(os.path.expanduser(init_path))

    # =========================================================================
    # 🔄 MASTER INTERCEPT CONFIGURE ROUTER FOR PYGUBU PIPELINE
    # =========================================================================
    def configure(self, cnf=None, **kw):
        """
        Catches Pygubu's dictionary property updates at runtime
        and routes them directly into your custom sCTk components.
        """
        if cnf is not None:
            kw = cnf | kw

        # Process and route core path-chooser configurations immediately
        if "initialdir" in kw:
            val = kw.pop("initialdir")
            if val:
                self._initialdir = os.path.expanduser(str(val))
                self.set(self._initialdir)

        if "type" in kw:
            self._type = str(kw.pop("type")).lower()

        if "title" in kw:
            self._title = str(kw.pop("title"))

        if "filetypes" in kw:
            self._filetypes = kw.pop("filetypes")

        if "defaultextension" in kw:
            self._defaultextension = str(kw.pop("defaultextension"))

        if "command" in kw:
            self._state_callback = kw.pop("command")

        # 🔄 FIX: Capture button text properties and dynamically apply it to your custom s_btn layout face!
        if "text" in kw:
            btn_label_txt = kw.pop("text")
            if hasattr(self, "s_btn"):
                try:
                    self.s_btn.configure(text=btn_label_txt)
                except Exception:
                    pass

        # Pass any leftover standard framework keyword attributes safely up to the base class
        if kw:
            try:
                super().configure(**kw)
            except Exception:
                pass

    config = configure

    # =========================================================================

    @property
    def initialdir(self) -> str:
        return self._initialdir

    @initialdir.setter
    def initialdir(self, v: str):
        self.configure(initialdir=v)

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, v: str):
        self.configure(type=v)

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, v: str):
        self.configure(title=v)

    @property
    def filetypes(self):
        return self._filetypes

    @filetypes.setter
    def filetypes(self, v):
        self.configure(filetypes=v)

    @property
    def defaultextension(self) -> str:
        return self._defaultextension

    @defaultextension.setter
    def defaultextension(self, v: str):
        self.configure(defaultextension=v)

    # =========================================================================

    def _on_browse_clicked(self):
        if getattr(self, "_custom_current_state", "normal") == "disabled": return

        # 🔄 FIX: Securely pass the updated local title, initialdir, and default extension variables into the dialog loop
        if self._type == "directory":
            chosen = ctk.filedialog.askdirectory(
                title=self._title,
                initialdir=self._initialdir
            )
        else:
            chosen = ctk.filedialog.askopenfilename(
                title=self._title,
                initialdir=self._initialdir,
                filetypes=self._filetypes,
                defaultextension=self._defaultextension
            )

        if chosen:
            self.set(chosen)
            try:
                if hasattr(super(), "set"): super().set(chosen)
            except Exception:
                pass
            if self._state_callback and callable(self._state_callback):
                try:
                    self._state_callback(chosen)
                except Exception:
                    pass

    def set(self, path_string: str):
        if not hasattr(self, "s_entry"): return
        cur = self.s_entry.cget("state")
        self.s_entry.configure(state="normal")
        self.s_entry.delete(0, tk.END)
        self.s_entry.insert(0, path_string)
        self.s_entry.configure(state=cur)

    def get(self) -> str:
        if not hasattr(self, "s_entry"): return self._initialdir
        return self.s_entry.get()


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("500x200")
    from sCTkFrame import sCTkFrame

    base_layer = sCTkFrame(root)
    base_layer.pack(expand=True, fill="both", padx=20, pady=20)
    widget = sCTkPathChooser(base_layer, type="file", title="Select Config Log Target", text="Select File...")
    widget.pack(expand=True, fill="x", padx=20, pady=10)
    root.mainloop()


# sCustomTkinter Technical Components Reference - Part 1

This document contains the complete developer reference documentation for the specialized sCTk CustomTkinter layout toolkit. 

All modules are built natively using CustomTkinter vector elements, ensuring clean scaling across high-DPI panels, full dual-profile theme compliance (Light/Dark mode), and complete freedom from standard Tcl/Tk focus bugs on macOS. Unselectable file parameters are dynamically dimmed, disabled, and locked from mouse clicks in real time.

---

## Centralized Theme & Integrity Guard Lockout

All custom layout components inherit properties and configuration data from ThemeableWidget and pull values out of the shared style sheet registry THEME_DEFAULTS inside sCTkThemes.py.

### Core Safety Exception Interceptors
To protect your production scripts from CustomTkinter's strict initialization checks (such as dropping a ValueError: color is None or throwing a TypeError for unexpected dictionary arguments), the suite implements two severe global validation traps straight inside ThemeableWidget.py:
1. Critical File Guard: If sCTkThemes.py is entirely missing or cannot be imported at boot, the application halts immediately and outputs a detailed FileNotFoundError on the terminal.
2. Null-Traffic Interceptor: If a component section exists inside sCTkThemes.py but has empty placeholder properties (None), the application stops compiling and raises a clear ValueError specifying exactly which widget and key path is broken.
3. Contamination Filter: The mixin isolates the disabled_map tracking sub-dictionary into a private class property (self._widget_disabled_map), stripping it completely from self.final_kw. This guarantees that forwarding **self.final_kw straight into native CustomTkinter base class constructors never leaks tracking keys or crashes your screens.

---

## 1. sCTkPathChooser (Compound Input Row)

The sCTkPathChooser is an advanced entry-based path selection row designed for settings forms and configuration columns. It pairs a fluid layout text entry field with a square or wide descriptive browse button.

The text entry field acts like an accordion: it is assigned an initial layout width of 0 inside a column weighted to 1, meaning it automatically stretches or contracts to fill 100% of whatever horizontal space remains after the browse button claims its fixed btn_width. By using a single vector character character token (such as "▶" or ">") combined with a narrow btn_width=36, you maximize the screen real estate for nested file strings.

### Constructor Signature
```python
sCTkPathChooser(master=None, width=350, height=32, type="directory", justify="left", title="Select Path", initialdir=None, initialfile=None, filetypes=None, btn_width=110, btn_height=32, btn_text=None, entry_height=32, browser_width=500, browser_height=450, state="normal", command=None, **kwargs)
```

### Available Properties & Arguments

| Argument | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| **width** | int | 350 | Total horizontal width in pixels of file entry and button combined. File path width = total width - button width. |
| **height** | int | 32 | Total vertical space allocated to the frame container block envelope. Children padding loops center them inside this space. |
| **type** | str | "directory" | Determines file picking or directory selection ("file" or "directory"). (Case-insensitive) |
| **justify** | str | "left" | Aligns path text orientation ("left", "right", "center"). Set to "right" to anchor long strings on the trailing directory folder names. |
| **btn_text** | str | None | Custom character text string mapped directly to the button face (e.g. "▶"). If left as None, it falls back to wide descriptive phrases like "Browse Folders...". |
| **entry_height** | int | 32 | Explicit thickness height in pixels assigned directly to the text entry field sub-widget. |
| **btn_width** | int | 110 | Explicit width in pixels assigned directly to the browse button element. |
| **btn_height** | int | 32 | Explicit thickness height in pixels assigned directly to the browse button element. |
| **browser_width** | int | 500 | Width of the pop-up modal file browser window in pixels. |
| **browser_height** | int | 450 | Height of the pop-up modal file browser window in pixels. |
| **state** | str | "normal" | Set whether row is interactive ("normal" or "disabled"). Toggling to disabled locks fields and dims colors using disabled_map. |

### Public API Methods
*   **set(path_string: str) -> None** – Rewrites the input box location string, executing system normalization rules automatically. Triggers your command callback.
*   **get() -> str** – Extracts the absolute normalized path string currently written inside the input field.
# sCustomTkinter Technical Components Reference - Part 2

---

## 2. Structural Passive Containers (sCTkFrame variants)

To follow native Tkinter conventions and avoid fragile timer overrides or initialization race conditions, all structural container classes behave as **passive geometry layout groups**. They do not actively monitor, police, or block incoming children on arrival. 

Toggling states on an entry group is handled cleanly at the application controller level using runtime children iterations (winfo_children()).

### sCTkFrame / sCTkFrameOutlined / sCTkScrollableFrame
Standard direct subclasses of native CustomTkinter frame elements wrapped in ThemeableWidget parameters. They pass arguments up to their parent layers cleanly.
```python
# Pure initialization layout pass
my_group = sCTkFrameOutlined(parent_window, border_width=2)
my_group.pack(fill="both", expand=True)
```

### sCTkFrameLabeledPrimary / sCTkFrameLabeledSecondary
Custom scrollable viewport containers that natively hide their vertical scrollbar paths by retrieving their active frame fg_color and painting the inner self._scrollbar parameters to match invisibly while setting track width to 0. 

They preserve complete compatibility with Pygubu Designer because they inherit directly from ctk.CTkScrollableFrame—allowing you to drag, drop, and pack elements inside them with native properties (label_text and label_anchor) working perfectly out of the box.
```python
# Native configurations compile fluidly inside Pygubu Designer trees
labeled_scroll_pane = sCTkFrameLabeledPrimary(
    master=app,
    label_text="System Network Configurations",
    label_anchor="w"
)
```

---

## 3. Visual Static Labels (sCTkLabel variants)

Because standard CustomTkinter CTkLabel components do not feature a native state property, running a generic form-disabling loop over a container normally leaves label descriptions fully bright, breaking your UI aesthetic.

The **sCTkLabelPrimary**, **sCTkLabelSecondary**, and **sCTkLabelTertiary** components natively intercept the .configure(state="...") property key. When set to "disabled", they gracefully intercept the command, bypass standard Tkinter attribute rejections, and look up the exact dimming colors assigned to the "text_color" row inside your style sheets to match your frozen fields.

### Global Controller Disabling Pattern
To cleanly freeze a passive container frame group and all of its interior fields and custom labels at runtime, apply this standard loop pattern inside your controller file:

```python
def set_form_group_state(container_widget, target_state: str):
    """Recursively walks down the layout group to toggle states on all input controls and labels."""
    for child in container_widget.winfo_children():
        if hasattr(child, "configure"):
            try:
                child.configure(state=target_state)
            except Exception:
                pass
```

---

## 4. Creating Standardized Dialogs With sCTkDialogCore

The creation of an advanced user dialogue panel is a structured, multi-step process in the sCustomTkinter system. This flow decouples structural layouts from operational code.

### Step-by-Step Implementation Workflow

#### Step 1: Initialization inside Pygubu-Designer
1. Open Pygubu-Designer and create a new clean project space (e.g., settingMachine).
2. Add a standard **CTkToplevel** widget into your visual workspace canvas.
3. Open the **Settings** panel, select the **Compound Subclass** choice option, and fill out your specific values for both the object name and your desired file package destination folder. 
4. *Note:* Leave the **Styles** option entirely blank. If custom components are missing from your layout pane options, register them via the **Custom Widget** setup tab first.
5. **Important:** Now, delete the placeholder CTkToplevel element you just generated from the design tree hierarchy.
6. Add the **sCTkDialogCore** custom component widget straight into your design workspace canvas (rename the instance label identifier token if desired).
7. Return to the visual **Settings** pane and assign your main layout widget reference target to lock onto the **sCTkDialogCore** element you just added.
8. Save your visual designer tree.

#### Step 2: Adding Content to the Dialog
1. With your active Pygubu-Designer project open, drag and direct additional custom sCTk input widgets directly onto the dialog canvas shell.
2. All inputs will align and organize themselves natively within the designated **Content Area**.
3. Customize your layout properties freely, setting row grid parameters, cell constraints, or pixel padding metrics (padx / pady).
4. Operational buttons, titles, and confirmation click handlers can be configured or swapped later via built-in convenience methods.
5. Save your work and select **Generate Code**.

#### Step 3: Customizing Generated Class Code
1. Open your top-level operational class file in your script editor space. Focus on **classname.py** (do NOT modify the structural baseline file classnameui.py).
2. Inject the following import declaration line at the absolute top of the module file structure:
   ```python
   from sCTkDialogMixin import sCTkDialogMixin
   ```
3. Inject the dialog mixin token straight into your class definition inheritance chain. Your original generated definition line will look like this:
   ```python
   class classname(baseui.classnameUI):
   ```
   Modify it to include the helper mixin parameter like this:
   ```python
   class classname(sCTkDialogMixin, baseui.classnameUI):
   ```

---

### Built-in Convenience Functions Reference

#### Dialogue & Window Management

*   **self.onDeleteWindow()**  
    Trigger hook bound to handle standard system Window Manager intercept close requests (e.g. clicking the top title bar "X" close circle).
*   **self.dialogClose()**  
    Call programmatically anywhere inside your controller script functions to instantly dismiss, unbind, and destroy the open dialog modal screen.
*   **self.runAndWait()**  
    Locks focus onto the window and forces the dialog into a strict **Modal (Blocking)** interaction state. The script will halt execution on that thread until the window closes. If this method is not explicitly called, the dialog window remains **Non-Modal (Fluid)**.
*   **self.setTitle(title: str)**  
    Dynamically rewrites the text string displayed at the top left of the native operating system window header shell wrapper.

#### Viewport & Button Content Management

*   **self.setHeading(heading=None, anchor=None)**  
    Modifies the core header label text printed above the content grid. The anchor string input accepts standard parameters: "w", "e", or "center". All alternative anchor inputs are ignored. Passing None to either argument results in no modification to that specific layout parameter.
*   **self.setTwoButton()**  
    Configures the window button row to display exactly two functional controls: an **Apply** action button and a **Cancel** shortcut button.
*   **self.setApplyButton(buttonName=None, ButtonCommand=None)**  
    Configures the label text string and click callback function pointer for the primary validation button. Passing None preserves current settings. Returns True.
*   **self.setCancelButton(buttonName=None, ButtonCommand=None)**  
    Configures the label text string and click callback function pointer for the exit shortcut button. Passing None preserves current settings. Returns True.
*   **self.setResetButton(buttonName=None, ButtonCommand=None)**  
    Configures the label text string and click callback function pointer for the secondary option button. Passing None preserves current settings. If the internal reset button component has been previously destroyed or unmapped, no updates occur and it returns False. Otherwise, parameters align and it returns True.

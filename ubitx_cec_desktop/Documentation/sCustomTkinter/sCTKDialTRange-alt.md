

### sCTkDialRange

Designed for continuous absolute attenuations like Volume, Mic Gain, or RF Attenuation. It enforces hard structural end-stops (blocks wrap-around) and decouples physical graduation markings from internal tracking values.

#### Constructor
```python
sCTkDialRange(master=None, from_=0, to=100, arc_angle=270, command=None, diameter=120, width=120, height=120, divisions=5, **kw)
```

#### Parameter Reference Matrix

| Parameter Name | Data Type | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Widget` | `None` | Reference pointer tracking the parent parent `sCTkFrame` or root context window layout layer. |
| `from_` | `int` | `0` | The lower absolute mathematical limit boundary offset initializing the rotation origin baseline. |
| `to` | `int` | `100` | The upper absolute mathematical limit boundary offset representing the maximum end-stop value. |
| `divisions` | `int` | `5` | The physical number of graduation calibration tick marks drawn uniformly around the dial perimeter. |
| `arc_angle` | `int / float` | `270` | Total active angular sweep area in degrees, automatically centered symmetrically at the top. |
| `command` | `callable` | `None` | **Primary Event Callback:** Fired instantly on rotation. Passes the current absolute position integer clamped between `from_` and `to`. |
| `left_click_callback` | `callable` | `None` | Custom macro callback triggered on canvas Left Mouse Button clicks (e.g., handles accelerated jumps like `-2`). |
| `right_click_callback` | `callable` | `None` | Custom macro callback triggered on canvas Right Mouse Button clicks (e.g., handles accelerated jumps like `+2`). |
| `diameter` | `int` | `120` | **Geometric Sizing Constraint:** If specified, forces a strict 1:1 square canvas container, overriding structural box parameters to guarantee a perfect circle. |
| `width` | `int` | `120` | The explicit fallback horizontal pixel boundary box width for the widget container frame. |
| `height` | `int` | `120` | The explicit fallback vertical pixel boundary box height for the widget container frame. |
| `state` | `str` | `"normal"` | Set to `"normal"` for interactive tuning or `"disabled"` to freeze inputs and gray-out graphics. |

#### Callback Signature & Usage
```python
# Emits absolute tracking value integers
def on_volume_pot_rotated(absolute_value: int):
    # Wheel impulses step by 5 units automatically to keep the potentiometer fast and snappy
    print(f"Transceiver Audio Gain updated to: {absolute_value}%")
```

#### Dynamic Property Modifiers Live
```python
# Re-calibrate a volume pot into a coarse squelch attenuator with 2 ticks
dial_range.configure(from_=0, to=10, divisions=2)

# Manually force the potentiometer value to absolute index 50
dial_range.set(50)
```


[Return to Table of Contents](#contents)




### sCTkDialContinuous

Designed exclusively for Variable Frequency Oscillators and rapid continuous menu rolling. It spins infinitely in 360-degree vectors, ignoring absolute limit boundaries completely.

### Constructor
```python
sCTkDialContinuous(master=None, divisions=24, command=None, left_click_callback=None, right_click_callback=None, diameter=120, width=120, height=120, **kw)
```

#### Parameter Reference Matrix

| Parameter Name | Data Type | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Widget` | `None` | Reference pointer tracking the parent parent `sCTkFrame` or root context window layout layer. |
| `divisions` | `int` | `24` | Number of detented layout index points tracked inside a single 360° visual turn of the dimple indicator. |
| `command` | `callable` | `None` | **Primary Event Callback:** Fired instantly on rotation. Passes a signed step velocity delta integer (`+1` for CW, `-1` for CCW). |
| `left_click_callback` | `callable` | `None` | Custom macro callback triggered on canvas Left Mouse Button clicks (e.g., handles accelerated jumps like `-2`). |
| `right_click_callback` | `callable` | `None` | Custom macro callback triggered on canvas Right Mouse Button clicks (e.g., handles accelerated jumps like `+2`). |
| `diameter` | `int` | `120` | **Geometric Sizing Constraint:** If specified, forces a strict 1:1 square canvas container, overriding structural box parameters to guarantee a perfect circle. |
| `width` | `int` | `120` | The explicit fallback horizontal pixel boundary box width for the widget container frame. |
| `height` | `int` | `120` | The explicit fallback vertical pixel boundary box height for the widget container frame. |
| `state` | `str` | `"normal"` | Set to `"normal"` for interactive tuning or `"disabled"` to freeze inputs and gray-out graphics. |

#### Callback Signature & Usage
```python
# Emits signed directional step velocity deltas (+1, -1, +2, -2)
def on_vfo_wheel_rotated(signed_step_delta: int):
    global current_frequency_hz
    # Multiply raw step increments by a simulated 100 Hz tuning channel step
    current_frequency_hz += signed_step_delta * 100
    refresh_frequency_display()
```

#### Dynamic Property Modifiers Live
```python
# Dynamically re-scale the heavy VFO flywheel container box size instantly at runtime
tuning_dial.configure(diameter=140)

# Manually advance the 3D visual dimple layout coordinates by an integer tracking step delta
tuning_dial.set_position_index(1)
```

---

### 🎨 Centralized Stylesheet Integration (`sCTkThemes.py`)

The suite fully complies with standard design systems and loads its parameters dynamically from your central dictionary theme registry based on active child class names. Make sure your shared configuration entries contain these exact tokens to maintain layout unity:

```python
THEME_DEFAULTS = {
    "sCTkDial": {
        "fg_color": ("#F1F5F9", "#0A0A0A"),       
        "text_color": ("#1A4375", "#FF9100"),     
        "dial_color": ("#9E9E9E", "#2A2F3D"),     
        "shadow_color": ("#CBD5E1", "#02040A"),
        "disabled_text_color": ("#94A3B8", "#4B5563"),
        "disabled_dial_color": ("#E2E8F0", "#1A1D24"),
        "disabled_dimple_glow": ("#CBD5E1", "#334155")
    },
    "sCTkDialSelector": {
        "fg_color": ("#F1F5F9", "#0A0A0A"),       
        "text_color": ("#1A4375", "#FF9100"),     
        "dial_color": ("#9E9E9E", "#2A2F3D"),     
        "shadow_color": ("#CBD5E1", "#02040A"),
        "pointer_color": ("#1A4375", "#FF9100"),   
        "disabled_text_color": ("#94A3B8", "#4B5563"),
        "disabled_dial_color": ("#E2E8F0", "#1A1D24")
    },
    "sCTkDialRange": {
        "fg_color": ("#F1F5F9", "#0A0A0A"),       
        "text_color": ("#1A4375", "#64748B"),     
        "dial_color": ("#9E9E9E", "#2A2F3D"),     
        "shadow_color": ("#CBD5E1", "#02040A"),
        "pointer_color": ("#1A4375", "#FF9100"),   
        "disabled_text_color": ("#94A3B8", "#4B5563"),
        "disabled_dial_color": ("#E2E8F0", "#1A1D24")
    },
    "sCTkDialContinuous": {
        "fg_color": ("#F1F5F9", "#0A0A0A"),       
        "text_color": ("#1A4375", "#FF9100"),     
        "dial_color": ("#1E293B", "#181E2B"),     
        "shadow_color": ("#CBD5E1", "#02040A"),
        "pointer_glow_color": ("#CBD5E1", "#3A455C"), 
        "disabled_text_color": ("#94A3B8", "#4B5563"),
        "disabled_dial_color": ("#E2E8F0", "#1A1D24"),
        "disabled_dimple_glow": ("#CBD5E1", "#334155")
    }
}
```


[Return to Table of Contents](#contents)



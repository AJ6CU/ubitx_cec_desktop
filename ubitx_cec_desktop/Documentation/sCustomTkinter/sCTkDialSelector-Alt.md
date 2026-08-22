



## sCTkDialSelector

Designed to mimic a physical multi-position rotary band or mode selection switch. It restricts pointer operations to fixed angular arcs, strips out all distracting intermediate tick subdivisions, and loops infinitely past boundary edges.

### Constructor
```python
sCTkDialSelector(master=None, labels=None, arc_angle=270, command=None, diameter=120, width=120, height=120, **kw)
```

### ### API Property Reference

| Property Name          | Data Type | Default Value | Description |
|:-----------------------| :--- | :--- | :--- |
| `master`               | `Widget` | `None` | Reference pointer tracking the parent parent `sCTkFrame` or root context window layout layer. |
| `labels`               | `List[str / int]` | `["POS 1", "POS 2", "POS 3"]` | Explicit array of text choice options to map uniformly around the configured arc sweep. |
| `arc_angle`            | `int / float` | `270` | Total active angular sweep area in degrees, automatically centered symmetrically at the top. |
| `command`              | `callable` | `None` | **Primary Event Callback:** Fired instantly on rotation. Passes a strict, positive 0-based index integer matching the position in your labels list array. |
| `left_click_callback`  | `callable` | `None` | Custom macro callback triggered on canvas Left Mouse Button clicks (e.g., handles accelerated jumps like `-2`). |
| `right_click_callback` | `callable` | `None` | Custom macro callback triggered on canvas Right Mouse Button clicks (e.g., handles accelerated jumps like `+2`). |
| `diameter`             | `int` | `120` | **Geometric Sizing Constraint:** If specified, forces a strict 1:1 square canvas container, overriding structural box parameters to guarantee a perfect circle. |
| `width`                | `int` | `120` | The explicit fallback horizontal pixel boundary box width for the widget container frame. |
| `height`               | `int` | `120` | The explicit fallback vertical pixel boundary box height for the widget container frame. |
| `state`                | `str` | `"normal"` | Set to `"normal"` for interactive tuning or `"disabled"` to freeze inputs and gray-out graphics. |

### Callback Signature & Usage


Returns a zero based positive or negative integer. Counterclockwise is negative, clockwise is positive.


#### Command 

```python
# Fires on dial rotation via mousewheel rotation (Command)
def dial_rotated(active_index: int):
```

#### left_click_callback 
```python
# Fires on left mouse button click
def dial_left_click(active_index: int):
```
#### right_click_callback 
```python
# Fires on right mouse button click
def dial_right_click(active_index: int):
```

### Dynamic Property Modifiers Live
```python
# Change the list options and arc sweep on the fly
dial_selector.configure(labels=["160M", "80M", "40M", "20M", "10M"], arc_angle=240)

# Manually snap the switch pointer directly to index notch 2
dial_selector.set(2)
```


[Return to Table of Contents](#contents)



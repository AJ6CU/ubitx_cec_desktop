import customtkinter as ctk
THEME_DEFAULTS = {
    "sCTkButtonPrimary": {
            # Physical Geometry (Passed to lock layout boundaries natively)
            "width": 140,  # Standard compact horizontal width profile
            "height": 34,  # FIX: Natively sets a clean, balanced button height

            "font": ("Arial", 15, "normal"),
            "fg_color": ("#1A4375", "#2471A3"),
            "hover_color": ("#112A4B", "#1F618D"),
            "text_color": ("#FFFFFF", "#FFFFFF"),
            "corner_radius": 6,

            "disabled_map": {
                "fg_color": ("#E5E7EB", "#374151"),
                "hover_color": ("#E5E7EB", "#374151"),
                "text_color": ("#94A3B8", "#64748B")
            },

            #  Higher-contrast Blue-Slate pressed state for maximum background separation
            "pressed_map": {
                # Light Mode: Balanced deep slate blue (#3B5984) - clean contrast against white background
                # Dark Mode: Lighter Cobalt-Slate blue (#2E4A75) - pops sharply forward from #111827 background
                "fg_color": ("#3B5984", "#2E4A75"),
                "hover_color": ("#3B5984", "#2E4A75"),

                # High-contrast font pairing to keep text perfectly legible
                "text_color": ("#FFFFFF", "#FFFFFF")
            },

            "alarm_map": {
                "fg_color": ("#990000", "#E74C3C"),
                "hover_color": ("#990000", "#E74C3C"),
                "text_color": ("#FFFFFF", "#FFFFFF")
            }
    },


    "sCTkButtonSecondary": {
            "font": ("Arial", 15, "normal"),
            "fg_color": ("#E5E7EB", "#374151"),
            "hover_color": ("#D1D5DB", "#4B5563"),
            "text_color": ("#1F2937", "#F9FAFB"),
            "border_width": 2,  # Ensure border renders
            "border_color": ("#9CA3AF", "#4B5563"),  # Add distinct border colors
            "corner_radius": 6,

            "disabled_map": {
                "fg_color": ("#F3F4F6", "#1F2937"),
                "hover_color": ("#F3F4F6", "#1F2937"),  # FIX: Absorbs hover glow
                "border_color": ("#E5E7EB", "#374151"),
                "text_color": ("#94A3B8", "#64748B")
            },

            # Custom Secondary Pressed Mapping Configuration
            "pressed_map": {
                "fg_color": ("#CBD5E1", "#1F2937"),  # Significantly darkens layout frame layer
                "hover_color": ("#CBD5E1", "#1F2937"),
                "border_color": ("#475569", "#94A3B8"),  # Sharpens edge lines for compressed feedback
                "text_color": ("#0F172A", "#FFFFFF")
            }
    },


    "sCTkButtonTertiary": {
            "font": ("Arial", 15, "normal"),
            "fg_color": "transparent",
            "text_color": ctk.ThemeManager.theme["CTkButton"]["fg_color"],
            "corner_radius": 6,

            # Darkened for Light Mode, brightened for Dark Mode to ensure high-contrast boundaries!
            "border_width": 1.25,
            "border_color": ("#64748B", "#94A3B8"),  # Light Mode: Solid Slate Gray | Dark Mode: Bright Light Slate
            "hover_color": ("#E2E8F0", "#1E293B"),  # Synchronized hover panel tints

            "disabled_map": {
                "border_color": ("#E5E7EB", "#374151"),
                "text_color": ("#94A3B8", "#64748B")
            },

            # Tactile Pressed Mapping (Matches your signature cobalt desaturated blue palette)
            "pressed_map": {
                "fg_color": ("#E2E8F0", "#1E293B"),
                "border_color": ("#112A4B", "#1F618D"),
                "text_color": ("#112A4B", "#1F618D")
            }
    },

    "sCTkCheckBox": {
            "font": ("Arial", 15, "normal"),
            "border_width": 3,

            # Active Palette (Primary Brand Blue Accents)
            "border_color": ("#64748B", "#94A3B8"),  # High-visibility structural rims
            "fg_color": ("#1A4375", "#2471A3"),      # Inner fill color when checked
            "hover_color": ("#112A4B", "#1F618D"),   # Smooth feedback glow on cursor over
            "text_color": ("#1F2937", "#D1D5DB"),    # Darkened Light Mode text for sharp visibility

            # Muted Disabled Overlay
            "disabled_map": {
                "text_color": ("#94A3B8", "#64748B"),    # Fades label text out of active focus
                "fg_color": ("#E5E7EB", "#374151"),      # Dulls the core inner box fill
                "border_color": ("#CBD5E1", "#475569")   # Softens the outer ring track line
            }
    },

    "sCTkComboBox": {
            "font": ("Arial", 15, "normal"),
            "dropdown_font": ("Arial", 15, "normal"),
            "border_width": 1.5,

            # Active Palette (Primary Brand Blue and High-Contrast Grays)
            "border_color": ("#1A4375", "#64748B"),  # Brand blue line / slate dark line
            "fg_color": ("#FFFFFF", "#111827"),       # Text entry field background layer
            "text_color": ("#1F2937", "#FFFFFF"),      # Input text characters
            "button_color": ("#2471A3", "#64748B"),    # The arrow clickable dropdown button box
            "button_hover_color": ("#112A4B", "#1F618D"),  # Arrow box cursor feedback highlight

            # Floating Popup Dropdown Selection Card List View Menu Styling
            "dropdown_fg_color": ("#FFFFFF", "#1F2937"),
            "dropdown_text_color": ("#1F2937", "#F9FAFB"),
            "dropdown_hover_color": ("#E5E7EB", "#374151"),

            # Muted Disabled Overlay
            "disabled_map": {
                "fg_color": ("#F3F4F6", "#1F2937"),      # Shades input container slightly
                "border_color": ("#E5E7EB", "#374151"),  # Softens bounding lines profile
                "text_color": ("#94A3B8", "#64748B"),    # Fades input text out of focus
                "button_color": ("#94A3B8", "#4B5563")   # Dulls arrow dropdown box container
            }
    },

    "sCTkEntryPrimary": {
            "font": ("Arial", 15, "normal"),
            "border_width": 1.5,

            # Active Look (Brand Blue Outline Rim / High Contrast Entry Layer)
            "border_color": ("#1A4375", "#64748B"),  # Brand blue / slate dark outline ring
            "fg_color": ("#FFFFFF", "#111827"),       # Clean entry input channel background canvas
            "text_color": ("#1F2937", "#F9FAFB"),     # High contrast text typography
            "corner_radius": 6,

            # Muted Disabled Overlay
            "disabled_map": {
                "fg_color": ("#F3F4F6", "#1F2937"),      # Drops frame luminosity track down 1 step
                "border_color": ("#CBD5E1", "#475569"),  # Softens bounding outer container grid lines
                "text_color": ("#94A3B8", "#64748B")     # Fades typed alphanumeric strings
            }
    },

    "sCTkEntrySecondary": {
            "font": ("Arial", 13, "normal"),  # Scaled down context fields
            "border_width": 1,  # Thinner layout border tracking

            # Active Look (Neutral borders / Shaded recessed entry track layer)
            "border_color": ("#9CA3AF", "#4B5563"),  # Neutral border frame profile
            "fg_color": ("#F3F4F6", "#1F2937"),      # Recessed background entry layer
            "text_color": ("#4B5563", "#D1D5DB"),     # Softer primary gray typography
            "corner_radius": 6,

            # Muted Disabled Overlay
            "disabled_map": {
                "fg_color": ("#F3F4F6", "#0B0F19"),      # Further drops frame luminosity values
                "border_color": ("#CBD5E1", "#374151"),  # Finalized soft silver trace for Light Mode!
                "text_color": ("#94A3B8", "#64748B")     # Standardizes locking typography behavior
            }
    },

    "sCTkFrame": {
            "border_width": 0,
            "corner_radius": 0,

            # Valid color tuple satisfies type validation checks safely
            "border_color": ("gray", "gray"),

            # Fully allows transparent fills to let background containers bleed through cleanly!
            "fg_color": "transparent"
    },

    "sCTkFrameLabeledPrimary": {
            "border_width": 2,
            # Crisp heavy branding accents matching your primary buttons palette
            "border_color": ("#1A4375", "#2471A3"),
            "fg_color": ("#FFFFFF", "#111827"),  # Solid interior card canvas panels
            "corner_radius": 8,

            # Custom sub-label parameters
            "label_font": ("Arial", 15, "bold"),
            "label_text_color": ("#111827", "#F9FAFB"),

            # Muted Disabled Overlay for the container border/text
            "disabled_map": {
                "border_color": ("#CBD5E1", "#374151"),
                "label_text_color": ("#94A3B8", "#64748B")
            }
    },

    "sCTkFrameLabeledSecondary": {
            # Secondary visual metrics footprint
            "border_width": 1,  # Thinner trace line profile tracking
            "border_color": ("#64748B", "#94A3B8"),  # Soft, clean slate outer rings
            "fg_color": ("#F3F4F6", "#111827"),  # Ambient recessed helper panel backdrops
            "corner_radius": 6,

            # Secondary hierarchy text configuration profile
            "label_font": ("Arial", 12, "normal"),
            "label_text_color": ("#4B5563", "#D1D5DB"),  # Muted body gray typography layout

            # Muted Disabled Overlay for the container border/text
            "disabled_map": {
                "border_color": ("#CBD5E1", "#374151"),
                "label_text_color": ("#94A3B8", "#64748B")
            }
    },

    "sCTkFrameOutlined": {
            "border_width": 1.5,
            # Light Mode: Crisp Slate Gray | Dark Mode: High-contrast Light Slate Gray
            "border_color": ("#64748B", "#94A3B8"),
            "corner_radius": 8,  # Smooth rounded container edges

            # Base Canvas Surface Layers (Crisp solid container cards)
            "fg_color": ("#FFFFFF", "#111827"),

            # Muted Disabled Overlay for the container border
            "disabled_map": {
                "border_color": ("#CBD5E1", "#374151")  # Soft silver trace light / Charcoal dark
            }
    },

    "sCTkLabelPrimary": {
            # Bolds and scales up to 18px to stand out cleanly above form fields as a header title
            "font": ("Arial", 18, "bold"),
            "fg_color": "transparent",
            "text_color": ("#111827", "#F9FAFB"),  # Uses your maximum high-contrast text metrics

            "disabled_map": {
                "text_color": ("#94A3B8", "#64748B")  # Soft slate tone across both modes uniformly
            }
    },

    "sCTkLabelSecondary": {
        # Standard body size 15 to match checkbox and option menu labels on a uniform baseline
        "font": ("Arial", 15, "normal"),
        "fg_color": "transparent",
        "text_color": ("#374151", "#D1D5DB"),

        # FIXED: Remove the top-level 'disabled_text_color' string parameter completely.
        # Place it strictly within the isolated 'disabled_map' layout dictionary object track instead!
        "disabled_map": {
            "text_color": ("#94A3B8", "#64748B")  # Your theme engine extracts this automatically
        }
    },


    "sCTkLabelTertiary": {
            # Scaled down to size 13 to serve as secondary context, captions, or helper hint messages
            "font": ("Arial", 13, "normal"),
            "fg_color": "transparent",
            "text_color": ("#4B5563", "#9CA3AF"),  # Slightly softer text colors so it is less loud on layout

            "disabled_map": {
                "text_color": ("#94A3B8", "#64748B")  # Standardizes locking behavior across text weights
            }
    },

    "sCTkOptionMenuPrimary": {
            "font": ("Arial", 15, "normal"),
            "dropdown_font": ("Arial", 15, "normal"),

            # Active Palette (Primary Brand Blue Accents & High-Contrast Layout Panels)
            "fg_color": ("#1A4375", "#2471A3"),  # Deep brand blue click-bar container
            "button_color": ("#112A4B", "#1F618D"),  # Right-aligned disclosure arrow block
            "button_hover_color": ("#0D1F38", "#1A5276"),  # Feedback highlight on arrow hover
            "text_color": ("#FFFFFF", "#FFFFFF"),  # Main selected item text
            "corner_radius": 6,

            # Floating Popup Menu Card Customization (Explicit solid tuples satisfy engine checks)
            "dropdown_fg_color": ("#FFFFFF", "#1F2937"),
            "dropdown_text_color": ("#1F2937", "#F9FAFB"),
            "dropdown_hover_color": ("#E5E7EB", "#374151"),

            # Muted Disabled Overlay
            "disabled_map": {
                "fg_color": ("#CBD5E1", "#374151"),  # Clean silver trace for Light Mode | Charcoal for Dark Mode
                "button_color": ("#CBD5E1", "#374151"),  # Matches track to form a single locked block
                "text_color": ("#94A3B8", "#64748B")  # Soft, high-contrast muted typography
            }
        },

    "sCTkOptionMenuSecondary": {
            # Bounding geometry parameters
            "border_width": 1.25,
            "corner_radius": 6,

            # Border contrast rims (Slate ring / Light slate gray)
            "border_color": ("#64748B", "#94A3B8"),

            # Widget container backgrounds (Soft light tint / Ultra-deep anthracite-black #0B0F19)
            "fg_color": ("#F3F4F6", "#0B0F19"),

            # Font metrics
            "font": ("Arial", 13, "normal"),
            "dropdown_font": ("Arial", 13, "normal"),

            # Aligned high-contrast typography
            "text_color": ("#1F2937", "#F9FAFB"),
            "button_hover_color": ("#94A3B8", "#374151"),

            # Dropdown options panels
            "dropdown_fg_color": ("#FFFFFF", "#1F2937"),
            "dropdown_text_color": ("#1F2937", "#F9FAFB"),
            "dropdown_hover_color": ("#E5E7EB", "#374151"),

            # Muted Disabled Overlay
            "disabled_map": {
                "text_color": ("#94A3B8", "#64748B"),
                "border_color": ("#CBD5E1", "#374151"),
                "fg_color": ("#E5E7EB", "#0B0F19")
            }
    },

    "sCTkProgressBar": {
            # Physical Geometry (Passed via **kwargs)
            "width": 200,  # Standard horizontal track length
            "height": 6,  # FIX: Natively sets a sleek, ultra-thin 6px track height

            # Color Map
            # Matches your slider's high-contrast unselected gray tones
            "fg_color": ("#E5E7EB", "#4B5563"),

            # Matches your primary OptionMenu/ComboBox brand blue
            "progress_color": ("#1A4375", "#2471A3"),

            # Smooth continuous edge styling
            "corner_radius": 100,  # Fully rounds off the left and right ends of the track

            # Muted Disabled Overlay
            "disabled_map": {
                "fg_color": ("#CBD5E1", "#374151"),  # Dulls unselected track backing
                "progress_color": ("#94A3B8", "#4B5563")  # Mutes current metric level bar contrast
            }
    },

    "sCTkRadioButton": {
            "font": ("Arial", 15, "normal"),

            # Text matching your standard labels and checkboxes
            "text_color": ("#374151", "#D1D5DB"),

            # Thicker unchecked rings give hover highlights an excellent surface area to pop!
            "border_width_unchecked": 4,
            "border_width_checked": 6,
            "border_color": ("#64748B", "#94A3B8"),

            # Active selection dot (matches OptionMenu/ComboBox base blue)
            "fg_color": ("#1A4375", "#2471A3"),

            # High-contrast navy/blue tones for tracking cursor movements
            "hover_color": ("#112A4B", "#1F618D"),

            # Muted Soft-Contrast Disabled Overlay
            "disabled_map": {
                "text_color": ("#94A3B8", "#64748B"),
                "fg_color": ("#CBD5E1", "#374151"),  # Inner dot drops to a soft silver in light mode
                "border_color": ("#CBD5E1", "#475569")  # Outer circle matches the soft silver trace look
            }
    },


    "sCTkScrollableFrame": {
            # Outer Container Framework
            "border_width": 1.5,
            "border_color": ("#64748B", "#94A3B8"),
            "corner_radius": 8,

            # Base Canvas Surface Layers
            "fg_color": ("#FFFFFF", "#111827"),
            "label_fg_color": "transparent",

            # 🎨 FIX: Sync the track channel background directly to your core surface tuple
            # This completely matches your row colors, removing the wide gray background stripe!
            "scrollbar_fg_color": ("#FFFFFF", "#111827"),

            # Internal Scrollbar Track Synchronization
            "scrollbar_button_color": ("#64748B", "#4B5563"),
            "scrollbar_button_hover_color": ("#1A4375", "#2471A3"),

            # Muted Disabled Overlay
            "disabled_map": {
                "border_color": ("#CBD5E1", "#374151"),
                "scrollbar_button_color": ("#CBD5E1", "#1F2937")
            }
        },


    "sCTkScrollbar": {
            "corner_radius": 4,
            "fg_color": "transparent",
            "button_color": ("#64748B", "#4B5563"),
            "button_hover_color": ("#1A4375", "#2471A3"),

            # Muted Disabled Overlay
            "disabled_map": {
                "button_color": ("#E5E7EB", "#1F2937")
            }
    },


    "sCTkSegmentedButton": {
            # Typography matching your core form controls
            "font": ("Arial", 15, "normal"),

            # Base Track Background (Pure neutral medium gray / dark container)
            "fg_color": ("#9E9E9E", "#111827"),

            # Active selected text remains crisp white over the brand blue
            "text_color": ("#FFFFFF", "#FFFFFF"),

            # Selected / Active Segment (Your primary OptionMenu/ComboBox brand navy blues)
            "selected_color": ("#1A4375", "#2471A3"),
            "selected_hover_color": ("#112A4B", "#1F618D"),

            # The perfect mid-dark neutral gray tone
            "unselected_color": ("#9E9E9E", "#1F2937"),
            "unselected_hover_color": ("#7D7D7D", "#374151"),  # Smoothly deepens on hover

            # Muted Disabled Overlay
            "disabled_map": {
                # FIX: Lightened the track background BEHIND the buttons completely to match your frame panels!
                "fg_color": ("#FFFFFF", "#111827"),

                # The individual button segments preserve their crisp, solid inactive looks
                "selected_color": ("#64748B", "#4B5563"),
                "unselected_color": ("#64748B", "#4B5563"),

                # Hover states completely lock to the background color to mask cursor movements
                "selected_hover_color": ("#64748B", "#4B5563"),
                "unselected_hover_color": ("#64748B", "#4B5563"),

                # Text turns into a light silver font in light mode, and a soft gray font in dark mode
                "text_color": ("#CBD5E1", "#94A3B8")
            }

    },


    "sCTkSlider": {
            # Physical Geometry (Passed via **kwargs)
            "width": 200,
            "height": 24,
            "button_length": 12,
            "border_width": 9,

            # Color Map
            # FIX: Changed Dark Mode track color from #1F2937 to #4B5563 for sharp visibility
            "fg_color": ("#E5E7EB", "#4B5563"),

            "progress_color": ("#1A4375", "#2471A3"),
            "button_color": ("#2471A3", "#2471A3"),
            "button_hover_color": ("#112A4B", "#1F618D"),

            # Muted Disabled Overlay
            "disabled_map": {
                # FIX: Added fg_color and unified to use your soft silver trace / charcoal dark gray palette maps!
                "fg_color": ("#CBD5E1", "#374151"),
                "progress_color": ("#CBD5E1", "#4B5563"),
                "button_color": ("#94A3B8", "#4B5563")
            }
    },


    "sCTkSwitch": {
            "font": ("Arial", 15, "normal"),

            # Physical Geometry (Thin Pill Silhouette Alignment Metrics)
            "width": 60,
            "height": 24,
            "switch_width": 42,
            "switch_height": 14,
            "corner_radius": 100,

            # Color Map (OFF / Resting State)
            # FIX: Darkened the Light Mode track line to #94A3B8 so it pops cleanly against white cards!
            "fg_color": ("#94A3B8", "#4B5563"),
            "text_color": ("#374151", "#D1D5DB"),

            # Active Palette (ON / Checked State)
            "progress_color": ("#1A4375", "#2471A3"),
            "button_color": ("#2471A3", "#2471A3"),
            "button_hover_color": ("#112A4B", "#1F618D"),

            # Muted Soft-Contrast Disabled Overlay
            "disabled_map": {
                "text_color": ("#94A3B8", "#64748B"),
                "fg_color": ("#CBD5E1", "#374151"),
                "progress_color": ("#CBD5E1", "#4B5563"),
                "button_color": ("#475569", "#94A3B8")
            }
    },


    "sCTkTabview": {
            # Global tab navigation font settings
            "font": ("Arial", 15, "normal"),

            # Active Palette (Page Canvas & Outer Background Surface Layers)
            # Light Mode: Pure white for card contrast
            # Dark Mode: Charcoal Slate 900 matching your core container frames
            "fg_color": ("#FFFFFF", "#111827"),
            "text_color": ("#FFFFFF", "#FFFFFF"),

            # Active Navigation Row Palette (Inner Segmented Button Customization)
            "segmented_button_fg_color": ("#9E9E9E", "#111827"),
            "segmented_button_selected_color": ("#1A4375", "#2471A3"),
            "segmented_button_selected_hover_color": ("#112A4B", "#1F618D"),
            "segmented_button_unselected_color": ("#9E9E9E", "#1F2937"),
            "segmented_button_unselected_hover_color": ("#7D7D7D", "#374151"),

            # Muted Disabled Overlay (Locks page clicks and flattens nav row)
            "disabled_map": {
                # FIX: Lightened the track background BEHIND the tab buttons completely to #FFFFFF for light mode!
                "segmented_button_fg_color": ("#FFFFFF", "#111827"),
                "segmented_button_selected_color": ("#CBD5E1", "#374151"),
                "segmented_button_unselected_color": ("#CBD5E1", "#374151"),
                "text_color": ("#94A3B8", "#64748B")
            }
    },

    "sCTkTextboxPrimary": {
            # Physical Sizing & Typography
            "font": ("Arial", 13, "normal"),
            "border_width": 1,
            "corner_radius": 6,

            # Canvas Base Layers (Sage/Charcoal Palette Profile)
            "border_color": ("#b5beb6", "#3d5242"),
            "fg_color": ("#cbcfcb", "#1a1a1a"),
            "text_color": ("#1c1d1c", "#e3ece4"),

            # Internal Native Scrollbar Map
            "scrollbar_button_color": ("#64748B", "#4B5563"),
            "scrollbar_button_hover_color": ("#1A4375", "#2471A3"),

            # Muted Disabled Overlay
            "disabled_map": {
                "fg_color": ("#E5E7EB", "#111827"),  # Lock container canvas back completely
                "border_color": ("#CBD5E1", "#1F2937"),
                "text_color": ("#94A3B8", "#64748B"),
                "scrollbar_button_color": ("#E5E7EB", "#1F2937"),  # Mutes the inner handle tracking rails
                "scrollbar_button_hover_color": ("#E5E7EB", "#1F2937")
            }
    },

    "sCTkTextboxSecondary": {
            # Compact size 12 font for minor logs or multi-column data views
            "font": ("Arial", 12, "normal"),
            "border_width": 0,
            "corner_radius": 0,

            # Canvas Base Layers (Flat Card Mirroring Colors)
            "fg_color": ("#FFFFFF", "#111827"),
            "text_color": ("#1F2937", "#F9FAFB"),

            # Internal Native Scrollbar Map
            "scrollbar_button_color": ("#64748B", "#4B5563"),
            "scrollbar_button_hover_color": ("#1A4375", "#2471A3"),

            # Muted Disabled Overlay
            "disabled_map": {
                "fg_color": ("#E5E7EB", "#111827"),  # Lock container canvas back completely
                "text_color": ("#94A3B8", "#64748B"),
                "scrollbar_button_color": ("#E5E7EB", "#1F2937"),  # Mutes the inner handle tracking rails
                "scrollbar_button_hover_color": ("#E5E7EB", "#1F2937")
            }
    },

    "sCTkPathChooser": {
        "entry_font": ("Arial", 13),
        "entry_fg": ("#F9F9FA", "#343638"),
        "entry_border_color": ("#979DA2", "#565B5E"),
        "entry_text_color": ("#000000", "#FFFFFF"),
        "btn_font": ("Arial", 13, "bold"),
        "btn_fg": ("#3B8ED0", "#1F6AA5"),
        "btn_hover": ("#2C74B3", "#144E75"),
        "btn_text_color": ("#DCE4EE", "#F9F9FA"),
        "btn_border_color": ("#3B8ED0", "#1F6AA5"),
        "disabled_map": {
            "entry_fg": ("#EAEAEA", "#2B2B2C"),
            "entry_border_color": ("#D3D3D3", "#3A3A3C"),
            "entry_text_color": ("#A0A0A0", "#7C7C7C"),
            "btn_fg": ("#D3D3D3", "#2D2F31"),
            "btn_border_color": ("#D3D3D3", "#2D2F31"),
            "btn_text_color": ("#A0A0A0", "#5A5C5E")
        }
    },
    "sCTkFileExplorer": {
        "entry_font": ("Arial", 12),
        "entry_fg": ("#F9F9FA", "#343638"),
        "entry_border_color": ("#979DA2", "#565B5E"),
        "entry_text_color": ("#000000", "#FFFFFF"),
        "btn_font": ("Arial", 12),
        "btn_fg": ("#3B8ED0", "#1F6AA5"),
        "btn_hover": ("#2C74B3", "#144E75"),
        "btn_text_color": ("#DCE4EE", "#F9F9FA"),
        "btn_border_color": ("#3B8ED0", "#1F6AA5"),
        "row_active_text": ("#1F6AA5", "#3B8ED0"),
        "row_dimmed_text": ("#A0A0A0", "#606060"),
    },

    "sCTkSelector": {
        "fg_color": "transparent",
        "corner_radius": 6,

        # 1. Provide an explicit map tracking structure for the disabled state
        "disabled_map": {
            "text_color": ("#808080", "#666666"),  # Light/Dark mode gray hex tokens
            "fg_color": "transparent"
        },

        # # 2. Add empty structural placeholders to satisfy the unresolved NULL interceptor guard
        # "pressed_map": {
        #     "state_placeholder": "none"
        # },
        # "alarm_map": {
        #     "state_placeholder": "none"
        # }
    },

    "sCTkSeparator": {
        # Format: (Light Mode Hex, Dark Mode Hex)
        # Softer mid-tones changed to robust crisp outlines for sharp visual separation
        "fg_color": ("#808080", "#8A9296"),
        "bg_color": "transparent",
        "corner_radius": 6,
        "font": ("Arial", 11, "bold"),
        "text_color": ("#1A1A1A", "#FFFFFF")  # Crisp high-contrast header text labels
    },

    "sCTkMessage": {
            # Centralized typography management
            "font": ("Arial", 14),
            # Stark charcoal for bright mode / Crisp off-white for slate dark mode
            "text_color": ("#1A1A1A", "#E5E5E5")
    },
    "sCTkTreeview": {
        "bg_color": "transparent",

        # Heading bar style profiles
        "header_bg_color": ("#E2E8F0", "#1E293B"),
        "header_text_color": ("#0F172A", "#F8FAFC"),
        "header_font": ("Arial", 11, "bold"),

        # 🎨 OPTIMIZED ROW STRIPING THEME PARAMETERS
        # Light mode alternates white/light-blue. Dark mode alternates deep obsidian/slate.
        "row_bg_color": ("#FFFFFF", "#111827"),     # Main background [3]
        "row_alt_bg_color": ("#F1F5F9", "#1E293B"), # Alternating background stripe [3]

        "text_color": ("#1E293B", "#F1F5F9"),
        "font": ("Arial", 11),

        # Selected high-contrast indicator tracks
        "selected_bg_color": ("#3B82F6", "#2563EB"),
        "selected_text_color": ("#FFFFFF", "#FFFFFF")
    },

    "sCTkTableview": {
        # Header Styling Container Mappings (Light Mode, Dark Mode)
        "header_bg_color": ("#E2E8F0", "#0F172A"),       # Slate-200 / Slate-900
        "header_text_color": ("#0F172A", "#F8FAFC"),     # Deep Charcoal / Snow White
        "header_font": ("Arial", 14, "bold"),

        # 🦓 Strengthened High-Contrast Zebra Striping Color Profiles
        # Enhanced Light Mode Alternate Row to an explicit, high-contrast Steel Blue Tint (#D1DCEE)
        # so it remains punchy and highly visible across all ambient cockpit display conditions!
        "cell_bg_color": ("#FFFFFF", "#111827"),         # Row A: Pure White / Deep Charcoal-950
        "cell_alt_bg_color": ("#D1DCEE", "#222C3A"),     # Row B: Punchy Steel Blue / Aligned Deep Slate Blue

        # Typography & Data Matrix Font Mapping
        "cell_text_color": ("#1E293B", "#E2E8F0"),       # Charcoal Gray / Off-White
        "cell_font": ("Arial", 13, "normal"),

        # Structural Framework Separators
        "grid_line_color": ("#CBD5E1", "#334155")        # Light Border Slate / Dark Border Slate
    },

    "sCTkSMeter": {
        "fg_color": ("#F4F7FA", "#0A0A0A"),       # Off-White Base / True Cockpit Black
        "text_color": ("#1A4375", "#FF9100"),     # High-Visibility Brand Blue / Glowing Neon Amber
        "alarm_color": ("#990000", "#FF2200"),    # Sharp Crimson Red / Blazing Mechanical Warning Red
        "needle_color": ("#112A4B", "#FF9100")    # Deep Navy Pointer / Glowing Orange Pointer
    },

    "sCTkBarSMeter": {
        # Light Mode: Clean White Face | Dark Mode: Deep Cockpit Black
        "fg_color": ("#FFFFFF", "#0A0A0A"),

        # Scale Labels & Ticks
        "text_color": ("#1A4375", "#FF9100"),  # Deep Navy Steel / Glowing Neon Amber

        # High-attenuation / High SWR Warning LED zones
        "alarm_color": ("#DC2626", "#FF2200"),  # Solid Crimson / Intense Redline Warning

        # Active illuminated LED blocks below thresholds
        "led_on_color": ("#2471A3", "#FF9100"),  # Active Brand Blue / Glowing Segment Orange

        # Unlit background block tracks visible behind active segments
        "led_off_color": ("#E2E8F0", "#1A1D20")  # Softer Gray / Muted Recessed Charcoal Slots
    },
    "sCTkDial": {
        # Light Mode Frame Base Panel | Dark Mode Cockpit Obsidian Base Panel
        "fg_color": ("#F1F5F9", "#0A0A0A"),

        # Perimeter calibration ticks: Brand Navy Blue (Light) / Neon Orange-Amber (Dark)
        "text_color": ("#1A4375", "#FF9100"),

        # Main Knob Cap Body Face: Harmonized Segmented Button Gray (Light) / Heavy Gunmetal Graphite (Dark)
        "dial_color": ("#9E9E9E", "#2A2F3D"),

        # Light Mode soft shadow bleed wash | Dark Mode absolute deep matte void background
        "shadow_color": ("#CBD5E1", "#02040A"),

        # Centralized multi-state disabled parameters (Completely removed from class code)
        "disabled_text_color": ("#94A3B8", "#4B5563"),  # Muted inactive tick marks
        "disabled_dial_color": ("#E2E8F0", "#1A1D24"),  # Faded matte knob cap face plate
        "disabled_dimple_glow": ("#CBD5E1", "#334155")  # Softened finger pocket reflection ring
    },
    "sCTkSpinbox": {
        # Sourced precisely from your sCTkEntryPrimary specifications!
        "font": ("Arial", 15, "normal"),
        "border_width": 1.5,
        "border_color": ("#1A4375", "#64748B"),
        "entry_color": ("#FFFFFF", "#111827"),
        "text_color": ("#1F2937", "#F9FAFB"),
        "corner_radius": 6,

        # FIXED: Deeply dampened contrast tokens to blend smoothly into the canvas backgrounds
        # Light Mode: Soft silver gray that steps down dramatically from the #1F2937 active text font
        # Dark Mode: Faded slate charcoal that sits just a tiny fraction above the pitch-black entry core
        "placeholder_text_color": ("#B1BBC6", "#2E3748"),

        # Standard vertical stacked micro-arrow styling tracks
        "button_color": ("#9E9E9E", "#2A2F3D"),
        "button_hover_color": ("#7D7D7D", "#374151"),

        # Direct cascading mapping for the locked disabled state machine
        "disabled_entry_color": ("#F3F4F6", "#1F2937"),
        "disabled_border_color": ("#CBD5E1", "#475569"),
        "disabled_text_color": ("#94A3B8", "#64748B"),
        "disabled_button_color": ("#CBD5E1", "#334155")
    },
    # ... your other widget entries
}


# 🔒 CENTRALIZED MODULE ENFORCEMENT GUARD
# Enforce absolute structural integrity validations instantly on module compilation
mandatory_keys = {"sCTkPathChooser", "sCTkFileExplorer"}
current_keys = set(THEME_DEFAULTS.keys())

missing_keys = mandatory_keys - current_keys
if missing_keys:
    raise KeyError(
        f"CRITICAL LAYOUT STATE EXCEPTION: The sCTkThemes configuration profile registry map "
        f"is severely corrupted. Missing mandatory custom widget dictionary structures: {list(missing_keys)}. "
        f"Please verify your package assets deployment loops immediately."
    )
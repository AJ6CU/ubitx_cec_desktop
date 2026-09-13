#!/usr/bin/python3
"""
uBITX CEC Desktop -- proposed interface, as a working mockup.

Nothing here talks to a radio. Every value is simulated so the LAYOUT and the
INTERACTIONS can be judged: what is where, what happens when you click it, how
it behaves when the state changes.

WHAT IT DEMONSTRATES

  * Two VFO panels of equal weight, the transmitting one tinted and marked.
    Nothing moves or changes size when split, RIT or transmit turn on or off.

  * Digit-select tuning. Click any digit in a frequency and the dial steps by
    that digit's value -- selecting a digit IS selecting the step, so there is
    no separate step control to keep in sync.

  * One meter split in two: signal under the receiving frequency, power and
    SWR under the transmitting one. Neither half is ever dead.

  * Controls that do not exist yet shown DISABLED rather than absent, so the
    layout does not shift when a backend gains the capability.

  * A wide, short window, sized to sit above SDR++ on a laptop.

RUN IT

    python3 ubitx_mockup.py

Then: click frequency digits, turn the dials, toggle Split and RIT, press
Transmit to watch the meters swap roles, and move between the tabs.
"""
import json
import os
import random
import tkinter as tk

import customtkinter as ctk

from scustomtkinter import (
    sCTk, sCTkFrame, sCTkNotebook,
    sCTkLabelPrimary, sCTkLabelSecondary, sCTkLabelTertiary,
    sCTkButtonPrimary, sCTkButtonSecondary, sCTkButtonTertiary,
    sCTkSMeterBar, sCTkDialContinuous, sCTkSpinbox,
    sCTkSegmentedButton, sCTkSwitch, sCTkComboBox, sCTkEntryPrimary,
    sCTkCheckBox,
)

# ---------------------------------------------------------------------------
# Simulated radio
# ---------------------------------------------------------------------------
BANDS = [
    ("160 m", 1_840_000), ("80 m", 3_573_000), ("40 m", 7_074_000),
    ("30 m", 10_136_000), ("20 m", 14_074_000), ("17 m", 18_100_000),
    ("15 m", 21_074_000), ("12 m", 24_915_000), ("10 m", 28_074_000),
]
MODES = ["LSB", "USB", "CWL", "CWU"]
CW_TONE_HZ = 500

# The widest useful filter for each mode, and what reset returns to.
#
# Kept per mode because they are not comparable: 2600 Hz is normal for voice
# and useless for CW, where it lets in everything either side of the signal
# you are working. Both are settable under Setup.
FILTER_DEFAULTS = {"LSB": 2600, "USB": 2600, "CWL": 500, "CWU": 500}

# Sizing. The frequency is the thing you read, so it takes what the window
# can spare; the dials are what you reach for, so they follow.
#
# The panel's height comes from whichever is taller -- the readout stack or
# the dial canvas -- so pushing one much past the other only adds empty
# space. They are kept roughly in step for that reason.
FREQ_FONT_SIZE = 56
KNOB_DIAMETER = 118

# Latching is NOT used on these dials.
#
# It exists so an accidental scroll cannot move a frequency, which is a real
# hazard -- but the protection each dial needs here is simpler and can be
# stated outright:
#
#   RX  is always live, because it is the control you are using, unless Lock
#       is on, which freezes everything.
#   TX  is live only in split. Out of split the two frequencies are the same
#       one, so a second tunable dial would be a way to move the RX frequency
#       while looking at the wrong panel.
#
# A disabled dial says that better than an armed one: it is visibly inert,
# and there is nothing to remember about how to wake it.
LATCHING_DIALS = False

# Where the window position is remembered.
#
# The panel is meant to sit against SDR++, and getting the two lined up is
# fiddly enough that nobody wants to do it twice. Reading SDR++'s own window
# geometry would be the obvious alternative, but Tk cannot see another
# application's windows -- and the answer would be stale the moment either
# one moved.
GEOMETRY_FILE = os.path.expanduser("~/.ubitx_mockup_geometry.json")


class RadioState:
    """Everything the interface displays. Stands in for the rig and the SDR."""

    def __init__(self):
        self.vfo_a = 14_029_400
        self.vfo_b = 14_024_500
        self.active = "a"          # which VFO the dial turns
        self.mode = "USB"
        self.band_index = 4
        self.split = False
        self.rit = False
        self.rit_offset = 0
        self.locked = False
        self.muted = False
        self.transmitting = False
        self.tx_inhibit = False
        self.filter_hz = FILTER_DEFAULTS["USB"]
        self.s_value = 4.0
        self.pwr = 0.0
        self.swr = 1.0

    @property
    def tx_vfo(self):
        """Which VFO transmits. B in split, otherwise the active one."""
        return "b" if self.split else self.active

    @property
    def rx_vfo(self):
        """Which VFO receives. The active one unless split moved TX to B."""
        return self.active if self.split else self.active

    def role_frequency(self, role):
        """The frequency for a ROLE rather than a VFO -- see VFOPanel."""
        which = self.tx_vfo if role == "tx" else self.rx_vfo
        base = self.frequency(which)
        if role == "rx" and self.rit:
            return base + self.rit_offset
        return base

    def role_vfo(self, role):
        return self.tx_vfo if role == "tx" else self.rx_vfo

    def set_role_frequency(self, role, value):
        which = self.tx_vfo if role == "tx" else self.rx_vfo
        if role == "rx" and self.rit:
            # Tuning the RX side while RIT is on moves the OFFSET, not the
            # VFO. That is what RIT is: a temporary nudge you can undo.
            self.rit_offset = max(-9999, min(9999,
                                             int(value) - self.frequency(which)))
            return
        self.set_frequency(which, value)

    def frequency(self, which):
        return self.vfo_a if which == "a" else self.vfo_b

    def set_frequency(self, which, value):
        value = max(100_000, min(30_000_000, int(value)))
        if which == "a":
            self.vfo_a = value
        else:
            self.vfo_b = value


# ---------------------------------------------------------------------------
# A frequency readout whose digits can be clicked
# ---------------------------------------------------------------------------
class FrequencyDisplay(sCTkFrame):
    """
    A frequency in the form 14.029.400, with every digit individually
    clickable.

    Clicking a digit selects it, and the selection IS the tuning step -- the
    hundreds digit means 100 Hz per dial click. That replaces a separate step
    control, and a step control that can disagree with the digit being tuned.
    """

    def __init__(self, master, on_digit=None, font_size=FREQ_FONT_SIZE, **kw):
        super().__init__(master, fg_color="transparent", border_width=0, **kw)
        self._on_digit = on_digit
        self._font = ("Arial", font_size)
        self._dim = ("Arial", font_size)
        self._digits = []          # label widgets, most significant first
        self._selected = 3         # index into the 8 digits; 1 kHz to start
        self._enabled = True
        # The rig tunes in whole 10 Hz steps, so the units digit can never be
        # the thing you are moving. It is shown, because the frequency has
        # eight digits, but it is not selectable.
        self._min_index = 6
        self._build()

    def _build(self):
        """Eight digit labels and two separators, packed left to right."""
        position = 0
        for group, trailing_dot in ((2, True), (3, True), (3, False)):
            for _ in range(group):
                lbl = sCTkLabelPrimary(self, text="0", font=self._font,
                                       fg_color="transparent")
                lbl.pack(side="left")
                # Each label carries its own index, so the handler knows which
                # digit was hit without searching the list.
                if position <= self._min_index:
                    lbl.bind("<Button-1>",
                             lambda e, i=position: self._select(i))
                self._digits.append(lbl)
                position += 1
            if trailing_dot:
                sCTkLabelTertiary(self, text=".", font=self._font,
                                  fg_color="transparent").pack(side="left")

    def set_enabled(self, value):
        """Greys the digits when the panel is not tunable."""
        self._enabled = bool(value)
        self._paint_selection()

    def _select(self, index):
        if index > self._min_index or not self._enabled:
            return
        self._selected = index
        self._paint_selection()
        if callable(self._on_digit):
            self._on_digit(self.step_hz())

    def step_hz(self):
        """The value of the selected digit, in Hz."""
        return 10 ** (7 - self._selected)

    def set_frequency(self, hz):
        text = f"{int(hz):08d}"[-8:]
        for lbl, ch in zip(self._digits, text):
            lbl.configure(text=ch)
        self._paint_selection()

    def _paint_selection(self):
        for i, lbl in enumerate(self._digits):
            if not self._enabled:
                lbl.configure(fg_color="transparent",
                              text_color=("#94A3B8", "#64748B"))
                continue
            lbl.configure(text_color=("#111827", "#F9FAFB"))
            if i == self._selected:
                lbl.configure(fg_color=("#1A4375", "#2471A3"),
                              text_color=("#FFFFFF", "#FFFFFF"))
            else:
                lbl.configure(fg_color="transparent")


# ---------------------------------------------------------------------------
# One VFO panel: label, frequency, annotation, dial
# ---------------------------------------------------------------------------
class RolePanel(sCTkFrame):
    """
    A frequency readout for a ROLE -- receive or transmit -- not for a VFO.

    RECEIVE IS ALWAYS ON THE LEFT. Making the panels stand for roles rather
    than for VFO A and VFO B means nothing swaps sides when split turns on:
    the number you are listening to stays where your eye already is, and only
    the VFO label under it changes. Panels that trade places on a state change
    are exactly what makes a display hard to read quickly.

    Which VFO currently fills each role is shown in the header, because it
    still matters -- but it is a label, not a layout.
    """

    def __init__(self, master, role, app, **kw):
        super().__init__(master, border_width=1, corner_radius=6, **kw)
        self._role = role
        self._app = app
        # Remembered so state() is called only when it CHANGES.
        #
        # sCTkDial.state() repaints, and update_view() runs on every refresh
        # -- so setting it unconditionally meant turning the dial triggered a
        # refresh, which restated the dial, which repainted it, which the
        # scroll handler saw as more work. It presented as the dial locking
        # up under the wheel.
        self._dial_state = None

        header = sCTkFrame(self, fg_color="transparent", border_width=0)
        header.pack(fill="x", padx=8, pady=(5, 0))

        self.role_label = sCTkLabelSecondary(
            header, text=role, font=("Arial", 12, "bold"))
        self.role_label.pack(side="left")

        self.vfo_label = sCTkLabelTertiary(header, text="vfo a",
                                           font=("Arial", 11))
        self.vfo_label.pack(side="left", padx=(8, 0))

        if role == "tx":
            # A transmit indicator, not a control. It belongs on the TX
            # frequency because that is the thing it is telling you about:
            # this number is going out right now.
            self.led = sCTkLabelPrimary(header, text=" ON AIR ",
                                        font=("Arial", 11, "bold"),
                                        corner_radius=4)
            self.led.pack(side="right")
        else:
            # VFO B sits with the receive panel because that is what it is:
            # the frequency you would be listening to if you swapped. In
            # split it is the transmit frequency and appears on the right
            # instead, so this hides.
            # sCTkLabelSecondary, not Tertiary: this is a frequency you read,
            # not a caption explaining one. Tertiary is for the annotations
            # under the readouts -- the step size, the CW tone -- which you
            # check occasionally. VFO B you want legible at a glance.
            self.standby = sCTkLabelSecondary(header, text="",
                                              font=("Arial", 14))
            self.standby.pack(side="right")

        body = sCTkFrame(self, fg_color="transparent", border_width=0)
        body.pack(fill="x", padx=8, pady=(0, 5))

        left = sCTkFrame(body, fg_color="transparent", border_width=0)
        left.pack(side="left", fill="x", expand=True)

        self.display = FrequencyDisplay(left, on_digit=self._on_digit)
        self.display.pack(anchor="w")

        self.note = sCTkLabelTertiary(left, text="", font=("Arial", 10))
        self.note.pack(anchor="w")

        # fg_color transparent so the knob sits on the panel's own colour.
        # The dial's theme block carries its own background, which reads as a
        # darker rectangle behind the knob when it differs from the frame.
        # width and height are the CANVAS; knob_diameter is the knob drawn on
        # it. Left at their defaults the canvas is 120x120 whatever the knob
        # does, so a bigger knob just fills more of the same box -- and a
        # smaller one leaves a wide margin. Both are set together, with just
        # enough margin for the tick marks the dial draws outside the knob.
        self.dial = sCTkDialContinuous(
            body, divisions=24, knob_diameter=KNOB_DIAMETER,
            width=KNOB_DIAMETER + 10, height=KNOB_DIAMETER + 10,
            fg_color="transparent",
            command=self._on_turn,
            left_click_callback=lambda: self._click_step(-1),
            right_click_callback=lambda: self._click_step(+1),
            double_click_command=lambda d: d.set_pressed(True),
            shift_double_click_command=lambda d: d.set_pressed(False))
        self.dial.pack(side="right", padx=(4, 0), pady=0)

    def _on_digit(self, step_hz):
        self._app.refresh()

    def _click_step(self, direction):
        self._on_turn(direction)

    def _on_turn(self, clicks):
        radio = self._app.radio
        if radio.locked:
            return
        step = self.display.step_hz()
        radio.set_role_frequency(
            self._role, radio.role_frequency(self._role) + clicks * step)
        self._app.refresh()

    def update_view(self, radio):
        is_tx = self._role == "tx"

        if is_tx:
            on_air = radio.transmitting
            self.led.configure(
                text=" ON AIR " if on_air else "  off air  ",
                fg_color=("#C0392B", "#C0392B") if on_air else "transparent",
                text_color=("#FFFFFF", "#FFFFFF") if on_air
                else ("#94A3B8", "#64748B"))
        else:
            other = "b" if radio.rx_vfo == "a" else "a"
            if radio.split:
                self.standby.configure(text="")
            else:
                hz = radio.frequency(other)
                self.standby.configure(
                    text=f"vfo {other}   {hz // 1_000_000}."
                         f"{(hz // 1000) % 1000:03d}.{hz % 1000:03d}")

        # Lock freezes both. Otherwise TX is tunable only in split -- out of
        # split it is showing the same frequency as RX, and moving it here
        # would be moving that.
        live = (not radio.locked) and (radio.split if is_tx else True)
        wanted = "normal" if live else "disabled"
        if wanted != self._dial_state:
            self._dial_state = wanted
            self.dial.state(wanted)
        self.display.set_enabled(live)
        self.display.set_frequency(radio.role_frequency(self._role))
        self.vfo_label.configure(text=f"vfo {radio.role_vfo(self._role)}")

        self.configure(border_color=("#993C1D", "#993C1D") if is_tx
                       else ("#CBD5E1", "#374151"))

        if is_tx and not radio.split:
            self.note.configure(text="follows rx — turn Split on to set it")
        elif radio.locked:
            self.note.configure(text="locked")
        elif is_tx and radio.mode.startswith("CW"):
            self.note.configure(text=f"−{CW_TONE_HZ} Hz cw tone")
        elif not is_tx and radio.rit:
            # The base is what you return to when RIT goes off, so it has to
            # be visible while RIT is on -- otherwise the only frequency on
            # screen is one you cannot get back to except by zeroing.
            base = radio.frequency(radio.rx_vfo)
            self.note.configure(
                text=f"rit {radio.rit_offset:+d} Hz   ·   base "
                     f"{base // 1_000_000}.{(base // 1000) % 1000:03d}."
                     f"{base % 1000:03d}")
        else:
            self.note.configure(text=f"step {self._readable_step()}")

    def _readable_step(self):
        hz = self.display.step_hz()
        return f"{hz // 1000} kHz" if hz >= 1000 else f"{hz} Hz"


# ---------------------------------------------------------------------------
# The application
# ---------------------------------------------------------------------------
class UbitxMockup(sCTk):

    def __init__(self):
        super().__init__()
        self.title("uBITX CEC Desktop — proposed layout")
        self.geometry(self._remembered_geometry())
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self.radio = RadioState()
        self._toggles = {}

        # refresh() touches widgets from every tab, and sCTkSpinbox.set()
        # invokes its command -- so setting an initial value while building
        # calls back into a interface that does not exist yet. The flag keeps
        # that harmless rather than relying on construction order.
        self._ready = False

        self.notebook = sCTkNotebook(self, side="left", tab_width=30,
                                     tab_style="rounded",
                                     text_orientation="auto",
                                     show_page_border=True)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self._build_operate(self.notebook.add("Operate"))
        self._build_rx(self.notebook.add("RX"))
        self._build_channels(self.notebook.add("Channels"))
        self._build_cw(self.notebook.add("CW"))
        self._build_setup(self.notebook.add("Setup"))

        # Initial values go in AFTER every tab exists, for the reason above.
        self._ready = True
        self.band_picker.set(BANDS[self.radio.band_index][0])
        self.mode_picker.set(self.radio.mode)

        self.refresh()
        self._tick()

    # -- window position ---------------------------------------------------
    def _remembered_geometry(self):
        """Where it was last time, or a sensible default."""
        try:
            with open(GEOMETRY_FILE) as handle:
                return json.load(handle)["geometry"]
        except Exception:
            return "1140x500"

    def _on_close(self):
        try:
            with open(GEOMETRY_FILE, "w") as handle:
                json.dump({"geometry": self.winfo_geometry()}, handle)
        except Exception:
            # Losing the position is a small cost; refusing to close is not.
            pass
        self.destroy()

    def _toggle_on_top(self):
        """
        Keeps the panel above SDR++.

        A short window sitting over a large one disappears behind it the
        moment you click the waterfall -- which is most of what you do. On
        top is almost certainly what you want here, but it is a preference
        rather than a given, so it is a switch.
        """
        wanted = not bool(self.attributes("-topmost"))
        self.attributes("-topmost", wanted)
        self.on_top_button.configure(
            text="on top" if wanted else "not on top",
            fg_color=("#1A4375", "#2471A3") if wanted else "transparent")

    # -- convenience ------------------------------------------------------
    # NAMED radio, NOT state.
    #
    # sCTk is a Tk window, and Misc.state() is Tk's own window-state method --
    # CustomTkinter's DPI tracker calls it on every open window:
    #
    #     TypeError: 'RadioState' object is not callable
    #
    # Anything subclassing a Tk widget inherits a large namespace; state,
    # place, lower and _draw are all already taken.

    def set_active(self, which):
        self.radio.active = which

    # -- Operate ----------------------------------------------------------
    def _build_operate(self, page):
        page.grid_columnconfigure(0, weight=1)
        # Row 5 is empty and takes every spare pixel, which holds the real
        # content at the TOP. Without it the rows share the extra height and
        # the whole panel drifts to the middle as the window grows.
        page.grid_rowconfigure(4, weight=1)

        # The two VFOs -----------------------------------------------------
        vfos = sCTkFrame(page, fg_color="transparent", border_width=0)
        vfos.grid(row=0, column=0, sticky="ew", padx=6, pady=(6, 2))
        vfos.grid_columnconfigure((0, 1), weight=1, uniform="vfo")

        self.panel_rx = RolePanel(vfos, "rx", self)
        self.panel_rx.grid(row=0, column=0, sticky="ew", padx=(0, 4))

        self.panel_tx = RolePanel(vfos, "tx", self)
        self.panel_tx.grid(row=0, column=1, sticky="ew", padx=(4, 0))

        # The split meter --------------------------------------------------
        meters = sCTkFrame(page, fg_color="transparent", border_width=0)
        meters.grid(row=1, column=0, sticky="ew", padx=6, pady=2)
        meters.grid_columnconfigure((0, 1), weight=1, uniform="meter")

        # One instrument in two halves: signal under the receiving frequency,
        # power under the transmitting one. Neither half is ever dead.
        self.s_meter = sCTkSMeterBar(meters, hide_lower_row=True,
                                     width=460, height=46)
        self.s_meter.grid(row=0, column=0, sticky="ew", padx=(0, 4))

        self.p_meter = sCTkSMeterBar(meters, hide_sig_row=True,
                                     width=460, height=46)
        self.p_meter.grid(row=0, column=1, sticky="ew", padx=(4, 0))

        # Actions ----------------------------------------------------------
        actions = sCTkFrame(page, fg_color="transparent", border_width=0)
        actions.grid(row=2, column=0, sticky="ew", padx=6, pady=2)

        sCTkButtonPrimary(actions, text="Log QSO", width=96,
                          command=self._log_qso).pack(side="left", padx=(0, 4))

        for key, label in (("split", "Split"), ("rit", "RIT")):
            btn = sCTkButtonSecondary(actions, text=label, width=64,
                                      command=lambda k=key: self._toggle(k))
            btn.pack(side="left", padx=2)
            self._toggles[key] = btn

        sCTkButtonSecondary(actions, text="A ⇄ B", width=64,
                            command=self._swap).pack(side="left", padx=2)

        for key, label in (("locked", "Lock"), ("muted", "Mute")):
            btn = sCTkButtonSecondary(actions, text=label, width=64,
                                      command=lambda k=key: self._toggle(k))
            btn.pack(side="left", padx=2)
            self._toggles[key] = btn

        # Transmit inhibit lives on Operate, not behind a tab. It is the
        # control you want when something is wrong -- a bad SWR, the wrong
        # antenna, a neighbour on frequency -- and hunting for it is exactly
        # what you cannot afford then.
        self._toggles["tx_inhibit"] = sCTkButtonSecondary(
            actions, text="TX off", width=68,
            command=lambda: self._toggle("tx_inhibit"))
        self._toggles["tx_inhibit"].pack(side="left", padx=2)

        # Mode is DIRECT selection, not a rotary: you jump between modes
        # rather than sweeping through them.
        self.mode_picker = sCTkSegmentedButton(
            actions, values=MODES, command=self._on_mode)
        self.mode_picker.pack(side="right")

        # Band is a short ordered list you step through, which is what a
        # spinbox is. It also shows where you are without being read.
        self.band_picker = sCTkSpinbox(
            actions, values=[b[0] for b in BANDS], wrap=False, width=110,
            command=self._on_band)
        self.band_picker.pack(side="right", padx=8)

        # Receive controls -------------------------------------------------
        rx_row = sCTkFrame(page, fg_color="transparent", border_width=0)
        rx_row.grid(row=3, column=0, sticky="ew", padx=6, pady=(6, 4))

        sCTkLabelTertiary(rx_row, text="filter",
                          font=("Arial", 11)).pack(side="left", padx=(0, 6))
        sCTkButtonSecondary(rx_row, text="wide", width=60,
                            command=lambda: self._filter(+300)).pack(side="left", padx=2)
        sCTkButtonSecondary(rx_row, text="narrow", width=60,
                            command=lambda: self._filter(-300)).pack(side="left", padx=2)
        # Reset matters as much as the two beside it: widening and narrowing
        # without a way back means every adjustment drifts further from
        # something usable, and the way back is mode-dependent.
        sCTkButtonSecondary(rx_row, text="reset", width=56,
                            command=self._filter_reset).pack(side="left", padx=2)
        self.filter_label = sCTkLabelPrimary(rx_row, text="2400 Hz",
                                             font=("Arial", 11))
        self.filter_label.pack(side="left", padx=8)

        # Disabled rather than absent: the layout will not shift when a
        # backend gains these, and the control says it exists.
        for label in ("AGC", "NR", "Notch"):
            btn = sCTkButtonSecondary(rx_row, text=label, width=60)
            btn.pack(side="left", padx=2)
            btn.state("disabled")
        sCTkLabelTertiary(rx_row, text="awaiting backend",
                          font=("Arial", 10)).pack(side="left", padx=6)

        self._build_status_strip(page)

    def _build_status_strip(self, page):
        """
        The bottom line: what the radio is doing, and whether it is reachable.

        Moved here from the top because none of it is something you act on
        mid-QSO -- it is state you glance at. The frequencies deserve the
        position your eye lands on first.

        The callsign and firmware version are gone entirely: they never
        change, so they belong in About rather than occupying the same line
        as live state.
        """
        strip = sCTkFrame(page, fg_color="transparent", border_width=0)
        strip.grid(row=5, column=0, sticky="ew", padx=6, pady=(0, 6))

        self.tx_chip = sCTkLabelPrimary(strip, text=" RX ", font=("Arial", 11),
                                        fg_color=("#0F6E56", "#0F6E56"),
                                        corner_radius=4)
        self.tx_chip.pack(side="left")

        self.mode_label = sCTkLabelTertiary(strip, text="USB",
                                            font=("Arial", 11))
        self.mode_label.pack(side="left", padx=8)

        self.sdr_status = sCTkButtonTertiary(
            strip, text="sdr — reconnect", width=130, height=22,
            command=lambda: self.sdr_status.configure(text="sdr ok"))
        self.sdr_status.pack(side="right")

        # NOT part of the design. The real radio transmits from the key or the
        # PTT, so there is no transmit button to place -- this is here only so
        # the mockup can show what the panel looks like on air, and it sits
        # apart from the controls that are real.
        sCTkButtonTertiary(strip, text="simulate transmit", width=130,
                           height=22, command=self._toggle_tx
                           ).pack(side="right", padx=8)
        sCTkLabelTertiary(strip, text="rig ok",
                          font=("Arial", 11)).pack(side="right", padx=8)

        self.on_top_button = sCTkButtonTertiary(
            strip, text="not on top", width=96, height=22,
            command=self._toggle_on_top)
        self.on_top_button.pack(side="right", padx=8)

    # -- the other tabs, sketched -----------------------------------------
    def _build_rx(self, page):
        wrap = sCTkFrame(page, fg_color="transparent", border_width=0)
        wrap.pack(fill="both", expand=True, padx=14, pady=12)

        sCTkLabelPrimary(wrap, text="Receive",
                         font=("Arial", 15, "bold")).pack(anchor="w")
        sCTkLabelTertiary(
            wrap,
            text="Everything about how you are listening. The choice below "
                 "decides where the audio and the signal reading come from, "
                 "and which of the controls under it can do anything: ATT and "
                 "IFS belong to the rig's own front end, so they are inert "
                 "while you are listening through the SDR.",
            font=("Arial", 11), wraplength=640, justify="left").pack(anchor="w", pady=(2, 12))

        row = sCTkFrame(wrap, fg_color="transparent", border_width=0)
        row.pack(anchor="w", pady=4)
        sCTkLabelSecondary(row, text="receiver",
                           font=("Arial", 12, "bold")).pack(side="left", padx=(0, 10))
        sCTkSegmentedButton(row, values=["SDR", "Rig"]).pack(side="left")
        sCTkLabelTertiary(
            row,
            text="which receiver the audio and the signal meter come from",
            font=("Arial", 10)).pack(side="left", padx=12)

        for label, note in (("ATT", "rig front end only"),
                            ("IFS", "rig front end only"),
                            ("Squelch", "awaiting backend"),
                            ("AGC", "awaiting backend")):
            line = sCTkFrame(wrap, fg_color="transparent", border_width=0)
            line.pack(anchor="w", pady=3)
            sw = sCTkSwitch(line, text=label)
            sw.pack(side="left")
            sCTkLabelTertiary(line, text=note,
                              font=("Arial", 10)).pack(side="left", padx=10)

    def _build_channels(self, page):
        """
        One list, one bank selector, and every action working on what is in
        front of you.

        The two channel systems -- the rig's twenty EEPROM slots and the
        unlimited file banks -- are shown as banks of one kind. That removes
        the separate copy-from-the-radio function: moving a channel from the
        radio to a file is a copy like any other.

        EVERYTHING ACTS ON THE BANK YOU ARE LOOKING AT. New goes here, delete
        removes from here, scan scans here. No target selector to keep in your
        head, and Copy is the only action needing a destination -- which it
        asks for when you press it.
        """
        page.grid_columnconfigure(0, weight=1)
        page.grid_rowconfigure(1, weight=1)

        head = sCTkFrame(page, fg_color="transparent", border_width=0)
        head.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 4))

        sCTkLabelTertiary(head, text="bank",
                          font=("Arial", 11)).pack(side="left", padx=(0, 6))

        # "New bank…" as the last entry is how one gets created: the place you
        # go to choose a bank is the place you would look to add one, and it
        # keeps bank management off the page entirely.
        self.bank_picker = sCTkComboBox(
            head, width=200, command=self._on_bank,
            values=["Radio (20 slots)", "Default set", "Contest", "Nets",
                    "New bank…"])
        self.bank_picker.pack(side="left")

        sCTkButtonSecondary(head, text="⋯", width=34).pack(side="left", padx=4)

        self.bank_note = sCTkLabelTertiary(head, text="", font=("Arial", 10))
        self.bank_note.pack(side="left", padx=10)

        self.bank_dirty = sCTkButtonPrimary(head, text="Write to radio",
                                            width=120)
        self.bank_dirty.pack(side="right")

        # What the radio is on RIGHT NOW, read-only.
        #
        # Clicking down a list or watching a scan, the question is always
        # "where am I actually listening?" -- and the answer was on another
        # tab. Repeating it here is duplication, but the alternative is
        # switching tabs to find out what the tab you left just did.
        self.channel_now = sCTkLabelSecondary(head, text="",
                                              font=("Arial", 13))
        self.channel_now.pack(side="right", padx=14)
        sCTkLabelTertiary(head, text="now",
                          font=("Arial", 10)).pack(side="right")

        # The table -------------------------------------------------------
        table = sCTkFrame(page, border_width=1, corner_radius=6)
        table.grid(row=1, column=0, sticky="nsew", padx=10, pady=2)

        header = sCTkFrame(table, fg_color="transparent", border_width=0)
        header.pack(fill="x", padx=8, pady=(6, 2))
        for text, width in (("#", 34), ("label", 120), ("frequency", 130),
                            ("mode", 70), ("station", 240), ("group", 90)):
            sCTkLabelTertiary(header, text=text, width=width,
                              font=("Arial", 11, "bold"),
                              anchor="w").pack(side="left")

        channels = (
            ("1", "20M-FT8", "14.074.000", "USB", "20m FT8 digital", "Digital"),
            ("2", "40M-LSB", "7.200.000", "LSB", "40m voice calling", "Voice"),
            ("3", "WX1", "14.032.000", "CW", "NOAA weather 1", "Utility"),
            ("4", "HAM2", "3.532.000", "CW", "2m hailing", "Nets"),
            ("5", "", "", "", "", ""),
        )
        for number, label, freq, mode, station, group in channels:
            self._channel_row(table, number, label, freq, mode, station, group)

        # Actions ---------------------------------------------------------
        actions = sCTkFrame(page, fg_color="transparent", border_width=0)
        actions.grid(row=2, column=0, sticky="ew", padx=10, pady=(6, 10))

        sCTkButtonPrimary(actions, text="Tune to", width=84).pack(side="left", padx=(0, 4))
        for label, width in (("Store VFO here", 120), ("Copy to…", 86),
                             ("Clear", 70)):
            sCTkButtonSecondary(actions, text=label,
                                width=width).pack(side="left", padx=2)

        sCTkLabelTertiary(actions, text="scan",
                          font=("Arial", 11)).pack(side="left", padx=(20, 4))
        sCTkButtonSecondary(actions, text="▶ start", width=76).pack(side="left", padx=2)
        dwell = sCTkEntryPrimary(actions, width=48)
        dwell.pack(side="left", padx=2)
        dwell.insert(0, "5")
        sCTkLabelTertiary(actions, text="seconds on each",
                          font=("Arial", 10)).pack(side="left", padx=4)

        self._on_bank("Radio (20 slots)")

    def _channel_row(self, parent, number, label, freq, mode, station, group):
        """
        One channel, editable in place.

        Editing in the table rather than in a form below it: the value you
        want to change is the one you are looking at, and a form means
        selecting a row, moving your eye, editing, and confirming that the
        right row was selected. Double-click anywhere on the row to tune to
        it.
        """
        row = sCTkFrame(parent, fg_color="transparent", border_width=0)
        row.pack(fill="x", padx=8, pady=1)

        empty = not label
        sCTkLabelTertiary(row, text=number, width=34,
                          font=("Arial", 11), anchor="w").pack(side="left")

        if empty:
            sCTkLabelTertiary(row, text="— empty —", width=560,
                              font=("Arial", 11), anchor="w").pack(side="left")
            return

        for value, width in ((label, 120), (freq, 130), (mode, 70),
                             (station, 240)):
            field = sCTkEntryPrimary(row, width=width - 6)
            field.pack(side="left", padx=(0, 6))
            field.insert(0, value)
            field.bind("<Double-Button-1>", lambda e: self._tune_to_channel())

        sCTkComboBox(row, values=["Voice", "Digital", "Nets", "Utility"],
                     width=84).pack(side="left")

    def _tune_to_channel(self):
        """Double-clicking a row puts it on the active VFO."""
        self.notebook.set("Operate")

    def _on_bank(self, choice):
        """
        Reacts to the bank changing, including the request to make a new one.
        """
        if choice == "New bank…":
            self._new_bank()
            return

        is_radio = choice.startswith("Radio")
        # The radio's memories are edited in place and written DELIBERATELY.
        # EEPROM has a finite number of writes and the value lives in the
        # hardware, so a keystroke should not reach it. File banks have
        # neither constraint and save as you type.
        self.bank_note.configure(
            text="the rig's own memories — edits are written when you say so"
            if is_radio else "a file bank — edits save as you make them")
        self.bank_dirty.state("normal" if is_radio else "disabled")

    def _new_bank(self):
        """Asks for a name, then leaves you in the new bank."""
        win = ctk.CTkToplevel(self)
        win.title("New bank")
        win.geometry("320x150")
        win.transient(self)

        body = sCTkFrame(win, fg_color="transparent", border_width=0)
        body.pack(fill="both", expand=True, padx=16, pady=14)
        sCTkLabelSecondary(body, text="Name", font=("Arial", 11)).pack(anchor="w")
        field = sCTkEntryPrimary(body, width=220)
        field.pack(anchor="w", pady=(2, 12))
        field.focus_set()

        row = sCTkFrame(body, fg_color="transparent", border_width=0)
        row.pack(anchor="w")
        sCTkButtonPrimary(row, text="Create", width=80,
                          command=win.destroy).pack(side="left", padx=(0, 6))
        sCTkButtonSecondary(row, text="Cancel", width=80,
                            command=win.destroy).pack(side="left")

        # The picker fell to the new entry when it was chosen; put it back so
        # cancelling does not leave "New bank…" showing as the current bank.
        win.protocol("WM_DELETE_WINDOW",
                     lambda: (self.bank_picker.set("Radio (20 slots)"),
                              win.destroy()))

    def _build_cw(self, page):
        wrap = sCTkFrame(page, fg_color="transparent", border_width=0)
        wrap.pack(fill="both", expand=True, padx=14, pady=12)
        sCTkLabelPrimary(wrap, text="CW",
                         font=("Arial", 15, "bold")).pack(anchor="w")
        sCTkLabelTertiary(
            wrap,
            text="Keyer settings live here rather than in a dialog: you adjust "
                 "speed and tone while operating, sometimes mid-QSO.",
            font=("Arial", 11), wraplength=640, justify="left").pack(anchor="w", pady=(2, 12))

        for label, value in (("Tone (Hz)", "500"), ("Speed (wpm)", "10"),
                             ("Delay to TX (ms)", "250"),
                             ("Delay to RX (ms)", "1000")):
            line = sCTkFrame(wrap, fg_color="transparent", border_width=0)
            line.pack(anchor="w", pady=3)
            sCTkLabelSecondary(line, text=label, width=130,
                               font=("Arial", 11)).pack(side="left")
            entry = sCTkEntryPrimary(line, width=80)
            entry.pack(side="left")
            entry.insert(0, value)

        line = sCTkFrame(wrap, fg_color="transparent", border_width=0)
        line.pack(anchor="w", pady=3)
        sCTkLabelSecondary(line, text="Keyer", width=130,
                           font=("Arial", 11)).pack(side="left")
        sCTkSegmentedButton(line, values=["Straight", "Iambic A",
                                          "Iambic B"]).pack(side="left")

        practice = sCTkFrame(wrap, fg_color="transparent", border_width=0)
        practice.pack(anchor="w", pady=(14, 0))
        sCTkSwitch(practice, text="Practice mode").pack(side="left")
        sCTkLabelTertiary(
            practice,
            text="keyer and sidetone work, nothing reaches the antenna",
            font=("Arial", 10)).pack(side="left", padx=10)

        decoder = sCTkButtonSecondary(wrap, text="Decoder", width=110)
        decoder.pack(anchor="w", pady=(14, 0))
        decoder.state("disabled")
        sCTkLabelTertiary(wrap, text="awaiting a backend that decodes",
                          font=("Arial", 10)).pack(anchor="w")

    def _build_setup(self, page):
        """
        Everything set once, gathered into groups on one page.

        The dialogs this replaces were one window each -- logbook, SDR,
        machine, connection -- which meant hunting through a menu to find
        which one held a given setting. Grouped here they are all visible at
        once, and the relationships are obvious: the SDR address sits beside
        the SDR software that uses it.

        Two keep their own windows: EEPROM and machine settings both write
        values that can stop the radio working, and both deserve a deliberate
        act rather than a field on a page you are scrolling past.
        """
        wrap = sCTkFrame(page, fg_color="transparent", border_width=0)
        wrap.pack(fill="both", expand=True, padx=14, pady=10)

        groups = (
            ("Station", (
                ("Callsign", "entry", "AJ6CU"),
                ("Appearance", "choice", ["Dark", "Light", "Follow system"]),
            )),
            ("Radio", (
                ("Connection", "button", "Serial or network…"),
                ("Tuning presets", "choice", ["10 Hz", "50 Hz", "100 Hz",
                                              "500 Hz", "1 kHz"]),
            )),
            ("SDR", (
                ("Software", "choice", ["SDR++", "SDRangel", "Gqrx", "None"]),
                ("Address", "entry", "127.0.0.1:4532"),
                ("Autostart", "switch", True),
                ("Default bandwidth CW", "entry", "500"),
                ("Default bandwidth SSB", "entry", "2600"),
            )),
            ("Logbook", (
                ("Enabled", "switch", True),
                ("Format", "choice", ["ADIF", "CSV"]),
                ("File", "button", "~/Downloads/ubitx_Logbook.adi"),
                ("Backup every (minutes)", "entry", "30"),
            )),
        )

        columns = sCTkFrame(wrap, fg_color="transparent", border_width=0)
        columns.pack(fill="both", expand=True)
        columns.grid_columnconfigure((0, 1), weight=1, uniform="setup")

        for index, (title, rows) in enumerate(groups):
            box = sCTkFrame(columns, border_width=1, corner_radius=6)
            box.grid(row=index // 2, column=index % 2, sticky="nsew",
                     padx=4, pady=4)

            sCTkLabelSecondary(box, text=title, font=("Arial", 12, "bold")
                               ).pack(anchor="w", padx=10, pady=(8, 4))

            for label, kind, value in rows:
                line = sCTkFrame(box, fg_color="transparent", border_width=0)
                line.pack(fill="x", padx=10, pady=2)
                sCTkLabelTertiary(line, text=label, width=150,
                                  font=("Arial", 11), anchor="w").pack(side="left")

                if kind == "entry":
                    field = sCTkEntryPrimary(line, width=150)
                    field.pack(side="left")
                    field.insert(0, value)
                elif kind == "choice":
                    sCTkComboBox(line, values=value, width=150).pack(side="left")
                elif kind == "switch":
                    sCTkSwitch(line, text="").pack(side="left")
                else:
                    sCTkButtonSecondary(line, text=value, width=200,
                                        anchor="w").pack(side="left")

            sCTkFrame(box, fg_color="transparent", border_width=0,
                      height=6).pack()

        danger = sCTkFrame(wrap, fg_color="transparent", border_width=0)
        danger.pack(anchor="w", pady=(10, 0))
        sCTkButtonSecondary(danger, text="EEPROM settings…",
                            width=150).pack(side="left", padx=(0, 6))
        sCTkButtonSecondary(danger, text="Machine settings…",
                            width=150).pack(side="left", padx=(0, 10))
        sCTkButtonSecondary(danger, text="Backup and restore…", width=170,
                            command=self._eeprom_backup).pack(side="left", padx=(0, 6))
        sCTkButtonSecondary(danger, text="About…", width=90,
                            command=self._about).pack(side="left", padx=(0, 10))
        sCTkLabelTertiary(
            danger,
            text="both write to the radio — their own windows, and a confirmation",
            font=("Arial", 10)).pack(side="left")

    # -- behaviour --------------------------------------------------------
    def _toggle(self, key):
        setattr(self.radio, key, not getattr(self.radio, key))
        if key == "rit" and self.radio.rit and self.radio.rit_offset == 0:
            self.radio.rit_offset = 700
        self.refresh()

    def _toggle_tx(self):
        if self.radio.tx_inhibit and not self.radio.transmitting:
            return
        self.radio.transmitting = not self.radio.transmitting
        self.refresh()

    def _swap(self):
        s = self.radio
        s.vfo_a, s.vfo_b = s.vfo_b, s.vfo_a
        self.refresh()

    def _on_mode(self, value):
        self.radio.mode = value
        # A 2600 Hz filter left over from voice is not a useful starting
        # point for CW, or the reverse. Changing mode resets it.
        self.radio.filter_hz = FILTER_DEFAULTS.get(value, self.radio.filter_hz)
        self.refresh()

    def _on_band(self, *_):
        label = self.band_picker.get()
        for i, (name, freq) in enumerate(BANDS):
            if name == label:
                self.radio.band_index = i
                self.radio.set_frequency(self.radio.active, freq)
                # Bands imply modes -- below 10 MHz is LSB by convention.
                self.radio.mode = "LSB" if freq < 10_000_000 else "USB"
                self.mode_picker.set(self.radio.mode)
                break
        self.refresh()

    def _filter_reset(self):
        """Back to the widest useful setting for the current mode."""
        self.radio.filter_hz = FILTER_DEFAULTS.get(self.radio.mode, 2600)
        self.refresh()

    def _filter(self, delta):
        self.radio.filter_hz = max(200, min(4000,
                                             self.radio.filter_hz + delta))
        self.refresh()

    def _about(self):
        """
        Where the callsign and firmware version went.

        They were on the main screen's top line, sharing space with live
        state -- but neither changes, so neither earns a place you look at
        while operating. The file paths belong here too: you need them when
        something has gone wrong, not while working a pileup.
        """
        win = ctk.CTkToplevel(self)
        win.title("About")
        win.geometry("520x300")
        win.transient(self)

        body = sCTkFrame(win, fg_color="transparent", border_width=0)
        body.pack(fill="both", expand=True, padx=18, pady=16)

        sCTkLabelPrimary(body, text="uBITX CEC Desktop",
                         font=("Arial", 16, "bold")).pack(anchor="w")
        sCTkLabelTertiary(body, text="a visual desktop for KD8CEC-powered uBITX radios",
                          font=("Arial", 11)).pack(anchor="w", pady=(0, 10))

        for label, value in (
            ("Version", "1.0  ·  June 2026"),
            ("Author", "Mark Hatch (AJ6CU)"),
            ("Email", "markjhatch@gmail.com"),
            ("Radio firmware", "KD8CEC v1.200"),
            ("Configuration", "~/.ubitx_cec_desktop.ini"),
            ("Logbook", "~/Downloads/ubitx_Logbook.adi"),
            ("Licence", "GPL v3"),
        ):
            line = sCTkFrame(body, fg_color="transparent", border_width=0)
            line.pack(anchor="w", pady=1)
            sCTkLabelTertiary(line, text=label, width=120,
                              font=("Arial", 11), anchor="w").pack(side="left")
            sCTkLabelSecondary(line, text=value,
                               font=("Arial", 11)).pack(side="left")

        sCTkButtonSecondary(body, text="Close", width=80,
                            command=win.destroy).pack(anchor="w", pady=(14, 0))

    def _eeprom_backup(self):
        """
        Compare and copy the radio's stored settings.

        Three places a value can live -- the factory default, what is in the
        radio now, and what is in the configuration file -- shown side by side
        so the differences are visible before anything is written.

        THE DIRECTION IS ABOVE THE COLUMNS, not below them in two dropdowns.
        Source and destination pickers under the table mean reading the
        values, then looking away to work out which way "Copy" goes. Putting
        the arrow in the header keeps it where the eye already is, and the
        two columns it names are the two being compared.
        """
        win = ctk.CTkToplevel(self)
        win.title("Radio settings — compare and copy")
        win.geometry("700x420")
        win.transient(self)

        body = sCTkFrame(win, fg_color="transparent", border_width=0)
        body.pack(fill="both", expand=True, padx=16, pady=14)

        direction = sCTkFrame(body, fg_color="transparent", border_width=0)
        direction.pack(anchor="w", pady=(0, 8))
        sCTkLabelTertiary(direction, text="copy",
                          font=("Arial", 11)).pack(side="left", padx=(0, 6))
        sCTkComboBox(direction, values=["Config file", "Factory", "Radio"],
                     width=130).pack(side="left")
        sCTkLabelPrimary(direction, text="  →  ",
                         font=("Arial", 14, "bold")).pack(side="left")
        sCTkComboBox(direction, values=["Radio", "Config file"],
                     width=130).pack(side="left")
        sCTkLabelTertiary(direction, text="   differences are marked",
                          font=("Arial", 10)).pack(side="left", padx=8)

        table = sCTkFrame(body, border_width=1, corner_radius=6)
        table.pack(fill="both", expand=True)

        head = sCTkFrame(table, fg_color="transparent", border_width=0)
        head.pack(fill="x", padx=8, pady=(6, 2))
        for text, width in (("", 30), ("Setting", 150), ("Factory", 120),
                            ("In the radio", 130), ("Config file", 130)):
            sCTkLabelTertiary(head, text=text, width=width,
                              font=("Arial", 11, "bold"),
                              anchor="w").pack(side="left")

        rows = (
            ("Master calibration", "85351", "148711", "—"),
            ("SSB BFO", "11056992", "11056342", "—"),
            ("CW BFO", "—", "11056042", "—"),
            ("Key type", "—", "Straight", "Straight"),
            ("CW speed (wpm)", "15", "5", "10"),
            ("Sidetone (Hz)", "600", "600", "600"),
            ("Delay to TX (ms)", "—", "0", "500"),
            ("Delay to RX (ms)", "—", "600", "5000"),
        )
        for name, factory, radio_value, config in rows:
            line = sCTkFrame(table, fg_color="transparent", border_width=0)
            line.pack(fill="x", padx=8, pady=1)
            # A CHECKBOX, not a switch. A switch says "this setting is on";
            # picking rows out of a table is selection, and a tick reads as
            # selected at a glance where a coloured track does not.
            sCTkCheckBox(line, text="", width=30).pack(side="left")
            sCTkLabelTertiary(line, text=name, width=150,
                              font=("Arial", 11), anchor="w").pack(side="left")
            sCTkLabelTertiary(line, text=factory, width=120,
                              font=("Arial", 11), anchor="w").pack(side="left")
            # A value that differs from the one beside it is the whole reason
            # for looking at this table, so it is the thing that stands out.
            differs = radio_value != config and "—" not in (radio_value, config)
            cell = sCTkLabelSecondary if differs else sCTkLabelTertiary
            cell(line, text=radio_value, width=130,
                 font=("Arial", 11, "bold") if differs else ("Arial", 11),
                 anchor="w").pack(side="left")
            cell(line, text=config, width=130,
                 font=("Arial", 11, "bold") if differs else ("Arial", 11),
                 anchor="w").pack(side="left")

        footer = sCTkFrame(body, fg_color="transparent", border_width=0)
        footer.pack(anchor="w", pady=(10, 0))
        sCTkCheckBox(footer, text="Select all").pack(side="left", padx=(0, 16))
        sCTkButtonPrimary(footer, text="Copy selected", width=120,
                          command=win.destroy).pack(side="left", padx=(0, 6))
        sCTkButtonSecondary(footer, text="Cancel", width=80,
                            command=win.destroy).pack(side="left")

    def _log_qso(self):
        """
        The log dialog: everything known is filled in, and the only field
        needing typing has the focus.
        """
        win = ctk.CTkToplevel(self)
        win.title("Log QSO")
        win.geometry("340x300")
        win.transient(self)

        body = sCTkFrame(win, fg_color="transparent", border_width=0)
        body.pack(fill="both", expand=True, padx=16, pady=14)

        sCTkLabelSecondary(body, text="Callsign",
                           font=("Arial", 11)).pack(anchor="w")
        call = sCTkEntryPrimary(body, width=200)
        call.pack(anchor="w", pady=(2, 10))
        call.focus_set()

        s = self.radio
        known = (
            ("Frequency", f"{s.frequency(s.tx_vfo) / 1_000_000:.6f} MHz"),
            ("Band", BANDS[s.band_index][0]),
            ("Mode", s.mode),
            ("RST sent", "599"),
            ("RST received", "599"),
        )
        for label, value in known:
            line = sCTkFrame(body, fg_color="transparent", border_width=0)
            line.pack(anchor="w", pady=1)
            sCTkLabelTertiary(line, text=label, width=110,
                              font=("Arial", 11)).pack(side="left")
            sCTkLabelSecondary(line, text=value,
                               font=("Arial", 11)).pack(side="left")

        row = sCTkFrame(body, fg_color="transparent", border_width=0)
        row.pack(anchor="w", pady=(14, 0))
        sCTkButtonPrimary(row, text="Log", width=80,
                          command=win.destroy).pack(side="left", padx=(0, 6))
        sCTkButtonSecondary(row, text="Cancel", width=80,
                            command=win.destroy).pack(side="left")

        win.bind("<Return>", lambda e: win.destroy())

    # -- redraw -----------------------------------------------------------
    def refresh(self):
        if not self._ready:
            return
        s = self.radio

        self.panel_rx.update_view(s)
        self.panel_tx.update_view(s)

        self.tx_chip.configure(
            text=" TX " if s.transmitting else " RX ",
            fg_color=("#993C1D", "#993C1D") if s.transmitting
            else ("#0F6E56", "#0F6E56"))

        for key, btn in self._toggles.items():
            on = getattr(s, key)
            # A latched control reads as lit or unlit, which is what
            # distinguishes it from a button that does something.
            btn.configure(fg_color=("#0F6E56", "#0F6E56") if on else
                          ("#E2E8F0", "#1F2937"))

        self.filter_label.configure(text=f"{s.filter_hz} Hz")
        self.mode_label.configure(text=s.mode)

        rx_hz = s.role_frequency("rx")
        self.channel_now.configure(
            text=f"{rx_hz // 1_000_000}.{(rx_hz // 1000) % 1000:03d}."
                 f"{rx_hz % 1000:03d}   {s.mode}")



        self.s_meter.set(s_value=0.0 if s.transmitting else s.s_value)
        self.p_meter.set(pwr_value=s.pwr, swr_value=s.swr)

    def _tick(self):
        """Wanders the simulated telemetry so the meters do something."""
        s = self.radio
        if s.transmitting:
            s.pwr = min(10.0, max(0.0, (s.pwr or 6.0) + random.uniform(-0.6, 0.6)))
            s.swr = min(3.0, max(1.0, (s.swr or 1.4) + random.uniform(-0.1, 0.1)))
        else:
            s.pwr, s.swr = 0.0, 1.0
            s.s_value = min(9.0, max(1.0, s.s_value + random.uniform(-0.8, 0.8)))
        self.refresh()
        self.after(400, self._tick)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    UbitxMockup().mainloop()

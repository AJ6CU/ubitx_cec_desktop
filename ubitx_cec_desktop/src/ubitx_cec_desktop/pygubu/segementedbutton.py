#!/usr/bin/python3
"""
segmented button test

a test

UI source file: segmentedbuttontest.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import segementedbuttonui as baseui


class segementedbutton(baseui.segementedbuttonUI):
    def __init__(self, master=None):
        super().__init__(master)


if __name__ == "__main__":
    app = segementedbutton()
    app.run()

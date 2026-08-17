#!/usr/bin/python3
"""
customCTK_WidgetTesterPart4

just tests each widget

UI source file: customCTK_WidgetTesterPart4.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customCTK_WidgetTesterPart4ui as baseui


class customCTK_WidgetTesterPart4(baseui.customCTK_WidgetTesterPart4UI):
    def __init__(self, master=None):
        super().__init__(master)


if __name__ == "__main__":
    app = customCTK_WidgetTesterPart4()
    app.run()

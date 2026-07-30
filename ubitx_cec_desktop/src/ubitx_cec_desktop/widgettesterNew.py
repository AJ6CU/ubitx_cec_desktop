#!/usr/bin/python3
"""
widgettesterNew

just tests eah widget

UI source file: widgettester.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import widgettesterNewui as baseui


class widgettesterNew(baseui.widgettesterNewUI):
    def __init__(self, master=None):
        super().__init__(master)

    def primary1_CB(self):
        pass

    def secondary2_CB(self):
        pass

    def ghost3_cb(self):
        pass

    def menuOption_CB(self):
        pass

    def callback(self, event=None):
        pass


if __name__ == "__main__":
    app = widgettesterNew()
    app.run()

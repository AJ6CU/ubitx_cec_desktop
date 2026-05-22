#!/usr/bin/python3
"""
bandGraph

reuseable band graph object

UI source file: bandGraph.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import bandGraphui as baseui


#
# Manual user code
#

class bandGraph(baseui.bandGraphUI):
    def __init__(self, master=None, bandScannerWindow=None,  **kw):
        super().__init__(master, **kw)
        self.bandScannerWindow = bandScannerWindow

    def attachScrollbar_CB (self, scrollbar_callback):
        self.scrollbar_CB = scrollbar_callback

    def bandStart_CB(self, scale_value):
        self.scrollbar_CB(scale_value )


if __name__ == "__main__":
    root = tk.Tk()
    widget = bandGraph(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()

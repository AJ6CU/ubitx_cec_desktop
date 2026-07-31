#!/usr/bin/python3
"""
progressBar

derived from progressBar

UI source file: progressBar.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import progressBarui as baseui


#
# Manual user code
#

class progressBar(baseui.progressBarUI):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = progressBar(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()

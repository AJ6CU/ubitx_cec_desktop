#!/usr/bin/python3
"""
Frequency Spectrum

Displays an area of the Frequency showing signal strength

UI source file: frequencySpectrum.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import frequencySpectrumui as baseui

import mystyles
import globalvars as gv


#
# Manual user code
#

class frequencySpectrum(baseui.frequencySpectrumUI):
    def __init__(self,  master=None, mainWindow=None, **kw):
        self.master = master
        self.mainWindow = mainWindow

        self.centerFrequency = 14150000
        self.currentFrequency = self.centerFrequency
        self.startFrequency = None
        self.stopFrequency = None
        self.bandwidth = None

        super().__init__(self.master, **kw)


        #
        #   Make sure that a close by the Window manager goes to the same close callback
        #
        self.protocol("WM_DELETE_WINDOW", self.cancel_CB)

        self.initUX()

    def initUX(self):
        # self.title("Frequency Spectrum")
        # self.geometry("800x550")
        self.wait_visibility()  # required on Linux
        self.grab_set()
        self.transient(self.master)

        gv.trimAndLocateWindow(self.master, 0, 0)

        gv.formatCombobox(self.repeat_Combobox, "Arial", "24", "bold")
        gv.formatCombobox(self.bandwidth_Combobox, "Arial", "24", "bold")

        self.repeat_VAR.set('10x')
        self.bandwidth_VAR.set('120,000Hz')

        self.bandwidth = 120000
        self.startFrequency = int(self.centerFrequency - self.bandwidth/2)
        self.startFrequency_VAR.set(str(self.startFrequency))

        self.stopFrequency = int(self.centerFrequency + self.bandwidth/2)
        self.stopFrequency_VAR.set(str(self.stopFrequency))

        self.frequencyTuning_VAR.set(250)
        self.currentFrequency_VAR.set(str(self.currentFrequency))

    def testValues(self):
        self.centerFrequency =14150000

    def frequencyTuning_CB(self, scale_value):
        print("frequencyTuning_CB, new value:", self.frequencyTuning_VAR.get())
        self.currentFrequency = int((self.bandwidth * (int(self.frequencyTuning_VAR.get())/500))+self.startFrequency)
        self.currentFrequency_VAR.set(str(self.currentFrequency))


    def repeatValueChanged_CB(self, event=None):
        print("repeatValueChanged_CB, new value:", self.repeat_VAR.get())

    def bandwidthValueChanged_CB(self, event=None):
        print("bandwidthValueChanged_CB, new value:", self.bandwidth_VAR.get())

    def recenter_CB(self):
        print("recenter_CB")

    def startStopSpectrum_CB(self):
        print("startStopSpectrum_CB")

    def applyClose_CB(self):
        print("applyClose_CB")
        self.destroy()


    def cancel_CB(self):
        print("cancel_CB")
        self.destroy()




myroot=None
mainWindow=None


def launch_widget():
    widget= frequencySpectrum(myroot,mainWindow)

if __name__ == "__main__":
    myroot = tk.Tk()
    mystyles.setup_ttk_styles(myroot)

    Launch_Button = ttk.Button(myroot, text="Launch")
    Launch_Button.configure(text='Launch')
    Launch_Button.configure(command=launch_widget)
    Launch_Button.pack(side="top")

    myroot.mainloop()


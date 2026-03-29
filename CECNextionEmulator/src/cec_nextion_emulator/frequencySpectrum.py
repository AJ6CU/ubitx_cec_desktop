#!/usr/bin/python3
"""
Frequency Spectrum

Displays an area of the Frequency showing signal strength

UI source file: frequencySpectrum.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import frequencySpectrumui as baseui
import random
import time

import mystyles
import globalvars as gv


#
# Manual user code
#

class frequencySpectrum(baseui.frequencySpectrumUI):
    def __init__(self,  master=None, mainWindow=None, centerFrequency=None, **kw):
        self.master = master
        self.mainWindow = mainWindow
        self.centerFrequency = centerFrequency

        self.startFrequency = None                      # starting frequency for scanning
        self.stopFrequency = None                       # stopping frequency for scanning
        self.bandwidth = None                           # the width of the band being scanned
        self.stepSize = None                            # size of steps (frequency samples)
        self.lastCenterFrequency = None                 # tracks the last center frequency in case it has been changed
                                                        # between scans
        self.MaxADCCount = None                         # Maximum number of times that the ADC can be read.
                                                        # Machine dependent. About
        self.spectrumScanning = None                    # If true, spectrum scanning is running
        self.frequencyLines = {}

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
        print("canvas size after init=", self.frequencyPlotCanvas.winfo_height(),
              self.frequencyPlotCanvas.winfo_width())

        gv.formatCombobox(self.repeat_Combobox, "Arial", "24", "bold")
        gv.formatCombobox(self.bandwidth_Combobox, "Arial", "24", "bold")


        # Update bandwidth to use selected delimiter

        if gv.NUMBER_DELIMITER != '':                   # temporary to handle standalone testing
            localizedBandwidth=[]
            for item in self.bandwidth_Combobox['values']:
                localizedBandwidth.append(item.replace(',', gv.NUMBER_DELIMITER))
            self.bandwidth_Combobox['values']=localizedBandwidth

        #
        #   DEFAULTS
        #

        self.lastCenterFrequency = self.centerFrequency     # save current frequency

        self.MaxADCCount = 120
        self.repeat_VAR.set('10x')
        self.bandwidthSelected_VAR.set('120,000Hz')

        self.spectrumScanning = False           # default to scanning off

        self.updateScanParameters(self.bandwidthSelected_VAR.get())     # Can now format Frequency graphs

        self.frequencyTuning_VAR.set(250)                               # Set scrollbar in middle
        self.currentFrequency_VAR.set(str(self.lastCenterFrequency))    # Set frequency
        print(self.frequencyPlotCanvas.winfo_height(), self.frequencyPlotCanvas.winfo_width())

    def updateScanParameters(self, newBandwidth):
        self.bandwidth = int(newBandwidth.replace(",","").replace(".","").replace("Hz",""))

        self.startFrequency=int(self.centerFrequency - self.bandwidth/2)
        self.startFrequency_VAR.set(str(self.startFrequency))

        self.stopFrequency = int(self.centerFrequency + self.bandwidth/2)
        self.stopFrequency_VAR.set(str(self.stopFrequency))

        self.calculatedSampleSize_VAR.set(int((self.bandwidth / self.MaxADCCount) * 2))

    def genPlotData(self, count):
        buffer = []

        for i in range(count):
            buffer.append(random.randint(0, 255))
        return bytearray(buffer).hex()

    def plot(self, buffer):
        print("plotting called")
        print("canvas size after init=", self.frequencyPlotCanvas.winfo_height(),
              self.frequencyPlotCanvas.winfo_width())
        canvasWidth = self.frequencyPlotCanvas.winfo_width()
        x_width = canvasWidth // 120                     #width of each bar
        print("x_width =", x_width)
        remainingWidth = canvasWidth - (x_width * 120) - 8
        print("remainingWidth =", remainingWidth)

        x_stretch = remainingWidth / 120




        # the variables below size the bar graph
        # experiment with them to fit your needs
        # highest y = max_data_value * y_stretch
        y_stretch = 2.1
        # gap between lower canvas edge and x axis
        y_gap = 0
        # stretch enough to get all data items in

        # x_width = 4
        # gap between left canvas edge and y axis
        x_gap = 4
        c_height = 160


        for x in range(120):
            ymag = int(buffer[x*2:x*2+2],16)%70

            # calculate reactangle coordinates (integers) for each bar
            x0 = x * x_stretch + x * x_width + x_gap
            y0 = c_height - (ymag * y_stretch + y_gap)
            x1 = x * x_stretch + x * x_width + x_width + x_gap
            y1 = c_height - y_gap
            # # draw the bar
            if x in self.frequencyLines:
                self.frequencyPlotCanvas.coords(self.frequencyLines[x], x0, y0, x1, y1)
            else:
                self.frequencyLines[x]=self.frequencyPlotCanvas.create_rectangle(x0, y0, x1, y1, fill="lightgray", outline="lightgray")

    def frequencyTuning_CB(self, scale_value):
        self.currentFrequency = int((self.bandwidth * (int(self.frequencyTuning_VAR.get())/500))+self.startFrequency)
        self.currentFrequency_VAR.set(str(self.currentFrequency))


    def repeatValueChanged_CB(self, event=None):
        print("repeatValueChanged_CB, new value:", self.repeat_VAR.get())
        self.remainingCount_VAR.set(self.repeat_VAR.get().replace("X",""))

    def bandwidthValueChanged_CB(self, event=None):
        print("bandwidthValueChanged_CB, new value:", self.bandwidthSelected_VAR.get())
        self.updateScanParameters(self.bandwidthSelected_VAR.get())

    def recenter_CB(self):
        print("recenter_CB")

    def startStopSpectrum_CB(self):
        if self.startStopSpectrum_VAR.get() == "Start":
            self.startStopSpectrum_VAR.set("Stop")
            self.spectrumScanning = False
        else:
            self.startStopSpectrum_VAR.set("Start")
            self.spectrumScanning = True
        print("startStopSpectrum_CB")

        print(self.frequencyPlotCanvas.winfo_height(), self.frequencyPlotCanvas.winfo_width())
        self.plotTestData()
        print(self.frequencyPlotCanvas.winfo_height(), self.frequencyPlotCanvas.winfo_width())

    def frequencyPlotCanvas_CB(self, event=None):
        print("frequencyPlotCanvas_CB, x=", event.x, ", y=", event.y)


    def plotTestData(self):
        buffer = self.genPlotData(120)
        self.plot(buffer)

    def applyClose_CB(self):
        print("applyClose_CB")
        self.destroy()


    def cancel_CB(self):
        print("cancel_CB")
        self.destroy()




myroot=None
mainWindow=None

def updatePlot(root, widget):
    widget.plotTestData()
    myroot.after(100, updatePlot,root, widget)

def launch_widget():
    global myroot
    widget= frequencySpectrum(myroot,mainWindow, 14150000)
    # myroot.after(50, updatePlot, myroot, widget)


if __name__ == "__main__":
    myroot = tk.Tk()
    mystyles.setup_ttk_styles(myroot)

    Launch_Button = ttk.Button(myroot, text="Launch")
    Launch_Button.configure(text='Launch')
    Launch_Button.configure(command=launch_widget)
    Launch_Button.pack(side="top")


    myroot.mainloop()


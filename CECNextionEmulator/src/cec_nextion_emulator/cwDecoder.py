#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import cwDecoderui as baseui
import globalvars as gv
from tkinter import messagebox


#
# Manual user code
#

class cwDecoder(baseui.cwDecoderUI):
    def __init__(self,  master=None, mainWindow=None, **kw):
        self.master = master
        self.mainWindow = mainWindow
        #
        #   Flags
        #

        #   This is a tristate flag that determines the state of the UX
        #   Can only do Frequency/Spectrum or CW decode (or nothing)
        self.spectrumMorseState = None  # None = not initialized,
                                        # "FreqScan" = Frequency/Spectrum Mode
                                        # "CWDecode" = CW Decode Mode


        super().__init__(self.master, **kw)
        #
        #   Make sure that a close by the Window manager goes to the same close callback
        #
        self.protocol("WM_DELETE_WINDOW", self.close_CB)

        self.windowResized = False      # these two variables are used to handle resizing of screen
        self.windowResizedObj = None    # while window is active. When the resized is detected,
                                        # the windowResized flag is set to true and a future
                                        # event is created to eventually update the window after 100ms
                                        # Each time the reseize event is called, the current future event
                                        # is deleted and a new one is scheduled. Only after 100 ms of no
                                        # new resize, is the scheduled event finally executed, the graph is
                                        # updated and the flag is set back to False.

        self.initUX()

    def initUX(self):
        self.title("CW Decode")
        self.geometry("600x430")
        self.wait_visibility()  # required on Linux
        self.grab_set()
        self.transient(self.master)

        gv.trimAndLocateWindow(self.master, 0, 0)


        #
        #   set defaults for scale
        #
        # self.frequencyPlotcwToneScale_VAR.set("10")
        # self.frequencyPlotcwToneValue_VAR.set("800")    # 10*50 + 300




        self.frequencyDecodeScale_VAR.set(self.mainWindow.frequencyDecodeScale)
        self.frequencySigValue_VAR.set(str(self.mainWindow.frequencyDecodeScale*10))            # 2*10

        self.frequencyPlotcwToneScale_VAR.set(self.mainWindow.frequencyPlotcwToneScale)
        self.frequencyPlotcwToneValue_VAR.set(str(self.mainWindow.frequencyPlotcwToneValue))

        if  self.mainWindow.frequencySpectrumMode == "FreqScan":
            self.enable_Frequency_Spectrum_CB()  # Start with the frequency scan
        else:
            self.enable_CW_Decode_CB()

        #
        #   Request existing saved data in EEPROM
        #
        # self.request_DSP_EEPROM_Data()

        self.frequencyHighValue_VAR.set('0')        # Reset min/max on entry
        self.frequencyLowValue_VAR.set(self.frequencySigValue_VAR.get())

        self.frequencyPlotCanvas_height = self.frequencyPlotCanvas.winfo_height()
        self.frequencyPlotCanvas_width = self.frequencyPlotCanvas.winfo_width()
        # print("self.frequencyPlotCanvas_width =", self.frequencyPlotCanvas.winfo_width(), "self.frequencyPlotCanvas_height =", self.frequencyPlotCanvas.winfo_height())

        self.FFTSIZE = 63   # Maximum number of times that the ADC can be read.
                            # Appears to be a bug in the DSP code. Suppose to be 64 elements (0-63) but only
                            # really sends 0-62
                                # Machine dependent. About

        self.FREQ_X_GAP = 4  # gap between left canvas edge and y axis
        self.FREQ_Y_GAP = 0  # gap between lower canvas edge and x axis
        self.FREQ_Y_MAX = 70  # maximum value of Y values

        self.frequencyLineObj = [None] * self.FFTSIZE * 1
        self.frequencyLineYmag = [None] * self.FFTSIZE * 1
        self.frequencyLineX0 = [None] * self.FFTSIZE * 1
        self.frequencyLineX1 = [None] * self.FFTSIZE * 1

        self.tuningLine1 = None  # used to save the tuning line object
        self.tuningLine2 = None  # used to save the tuning line object



    def enable_Frequency_Spectrum_CB(self, event=None):
        #
        #   Executed when Button-1 clicked on Frequency/Spectrum Frame (or children)
        #

        self.spectrumMorseState = "FreqScan"      # Set state flag Frequency/Spectrum mode

        self.setcwDecodeState("disabled")
        self.setFrequencySpectrumState("normal")
        self.mainWindow.theRadio.Set_Spectrum_Mode(95)  # Magic number indicating it is a spectrum scan
        self.frequencyHighValue_VAR.set('0')  # Reset min/max on entry
        self.frequencyLowValue_VAR.set(self.frequencySigValue_VAR.get())

    def enable_CW_Decode_CB(self, event=None):
        #
        #   Executed when Button-1 clicked on CW_Decode Frame (or children)
        #

        self.spectrumMorseState = "CWDecode"      # Set state flag to True = CW Decode Mode mode

        self.setcwDecodeState("normal")
        self.setFrequencySpectrumState("disabled")
        value = int(self.frequencyPlotcwToneValue_VAR.get()) - 300

        # following code is just to encode the tone setting and the fact that it is a CW
        value = value // 50

        value = value + 100     # this maps the final byte to between 100-129
                                # which means decode morse

        self.mainWindow.theRadio.Set_Spectrum_Mode(value)

    def setcwDecodeState(self, newState):
        if newState == "normal":
            self.cwDecodedText.configure(background="blue")
        else:
            self.cwDecodedText.configure(background="gray")



    def setFrequencySpectrumState(self, newState):
        if newState == "normal":
            self.frequencyPlotFrame.state(['!disabled'])
            self.frequencyPlotCanvas.configure(bg="blue")

        else:
            self.frequencyPlotFrame.state(['disabled'])
            self.frequencyPlotCanvas.configure(bg="gray")

    #
    #   EEPROM Variable load functions
    #
    def request_DSP_EEPROM_Data(self):
        #
        # Request DSP data stored in EEPROM
        self.mainWindow.theRadio.Req_DSP_EEPROM_Settings()


    def process_DSP_Data(self, buffer):
        byteList = int(buffer).to_bytes(4,'little')
        # print("process_DSP_Data", byteList)

        if int(buffer) < 0xffffff:          # only a 3 hex byte number

            print("eeprom values returned")
            print("decodescale*10=", byteList[0])
            print("useDSPFlag=", byteList[1])

            self.frequencyDecodeScale_VAR.set(byteList[0]/10)
            self.frequencySigValue_VAR.set(byteList[0])

            if byteList[1] == 1:
                self.mainWindow.UseDSP =  "True"
            else:
                self.mainWindow.UseDSP = "False"
            # case 95:    # This is the code for being in spectrum mode
            #     self.spectrumMorseState = "FreqScan"      # Set state flag Frequency/Spectrum mode
            #
            # #
            # #   in CWDecode mode, this byte is between 100 and < 146. The offset from 100
            # #   is the offset (*50 +300) within the SSB bandwidth. So the scan is limited to be
            # #   between 300(scale=0) and (50*45 + 300 = 2550)
            # #   So a very little room to scan the band, really just fine tuning within a frequency
            # #
            # case _:
        # commandType if (commandType >= 106):
        # elif ((byteList[2] >= 100) and (byteList[2] < 146)):
        #     self.spectrumMorseState = "CWDecode"
        #     self.frequencyPlotcwToneScale_VAR.set(str(byteList[2]-100))
        #     self.frequencyPlotcwToneValue_VAR.set(
        #         str((int(self.frequencyPlotcwToneScale_VAR.get())*50)+300))   # 10*50 + 300
        # else:
        else:
            pass
            # print("loopback DSP Data:", hex(int(buffer)))

    #
    #   Data processors
    #
    def process_Spectrum_Data(self, buffer):
        # print("buffer size=", len(buffer))
        currentMax = int(self.frequencyHighValue_VAR.get())
        currentMin = int(self.frequencyLowValue_VAR.get())

        x_width, x_stretch, y_stretch = gv.calculatePlotParameters(self.frequencyPlotCanvas_width, self.FFTSIZE,
                                                                   self.FREQ_X_GAP,
                                                                   self.frequencyPlotCanvas_height,
                                                                   self.FREQ_Y_MAX,
                                                                   self.FREQ_Y_GAP)

        byteBuffer = bytearray.fromhex(buffer)          #This gives us an array of hex bytes

        for x, y in enumerate(byteBuffer):

            ymag = y>>1
            if ymag < 0:
                ymag = 0
            else:
                if (ymag > self.FREQ_Y_MAX):
                    ymag = self.FREQ_Y_MAX

            if ymag < currentMin:
                currentMin = ymag
                self.frequencyLowValue_VAR.set(str(currentMin))
            elif ymag > currentMax:
                currentMax = ymag
                self.frequencyHighValue_VAR.set(str(currentMax))

            self.drawBars(x, ymag, x_width, x_stretch, y_stretch)

        self.updateTargetFreqBars()

    def drawBars(self,x,y, x_width, x_stretch, y_stretch):

        # calculate rectangle coordinates (integers) for each bar
        # x0 = x * x_stretch + x * x_width + x_gap
        # y0 = c_height - (ymag * y_stretch + y_gap)
        # x1 = x * x_stretch + x * x_width + x_width + x_gap
        # y1 = c_height - y_gap

        x0, y0, x1, y1 = gv.calculatePlotBar(self.frequencyPlotCanvas_height, x, y, x_width, x_stretch,
                                             self.FREQ_X_GAP, y_stretch, self.FREQ_Y_GAP)

        # draw the bar
        if self.frequencyLineObj[x] != None:  # if bar exists, then adjust coordinates for new values
            self.frequencyPlotCanvas.coords(self.frequencyLineObj[x], x0, y0, x1, y1)
        else:  # If this is the first time, then create the bar
            self.frequencyLineObj[x] = self.frequencyPlotCanvas.create_rectangle(x0, y0, x1, y1, fill="yellow",
                                                                                 outline="yellow")

        #
        #   Save y magnitude for resize event
        #   Save x0,x1 for beginning and end of every bar. This allows us to redraw the guide bars as the cw tuning bar is moved
        #
        self.frequencyLineYmag[x] = y
        self.frequencyLineX0[x] = x0
        self.frequencyLineX1[x] = x1

    def updateTargetFreqBars(self):
        #   get the length of the scale and add 1 ("fence post rule")
        scaleLength = int(self.frequencyPlotcwToneScale["to"] - self.frequencyPlotcwToneScale["from"]) + 1
        #
        #   this calculation maps the scale (0-45) until the FFT Size (0-63)
        #   this allows us to draw two vertical lines that help target the apparent CW signal in the range
        #
        barPos = round((int(self.frequencyPlotcwToneScale_VAR.get()) / scaleLength) * self.FFTSIZE)

        x0 = self.frequencyLineX0[barPos]
        x1 = self.frequencyLineX1[barPos]

        if self.tuningLine1 == None:
            self.tuningLine1 = self.frequencyPlotCanvas.create_line(x0,
                                                                    self.frequencyPlotCanvas_height,
                                                                    x0,
                                                                    0,
                                                                    fill="red", width=2)
            self.tuningLine2 = self.frequencyPlotCanvas.create_line(x1,
                                                                    self.frequencyPlotCanvas_height,
                                                                    x1,
                                                                    0,
                                                                    fill="red", width=2)
        else:

            self.frequencyPlotCanvas.coords(self.tuningLine1, x0, self.frequencyPlotCanvas_height, x0, 0)
            self.frequencyPlotCanvas.coords(self.tuningLine2, x1, self.frequencyPlotCanvas_height, x1, 0)

    def process_CWDecoded_Data(self, buffer):
        print("Processing CW Decoded in window", buffer)
        for char in buffer:
            self.logCW_Character(char)

    #
    #   Callbacks
    #

    def frequencyDecodeScale_CB(self, scale_value):
        print("scale_value:", scale_value, type(scale_value))
        self.frequencySigValue_VAR.set(str(int(scale_value)*10)) # 2*10
        self.mainWindow.theRadio.Set_Signal_Value(scale_value)

    def frequencyPlotcwToneScale_CB(self, scale_value):
        self.frequencyPlotcwToneValue_VAR.set(str(((int(scale_value)*50)+300)))
        self.updateTargetFreqBars()


    def close_CB(self):
        self.spectrumMorseState = None
        self.mainWindow.consumerDSPdata = self.mainWindow
        self.destroy()

    def logCW_Character (self,newchar):
        if len(self.cwDecodedText.get('1.0', 'end')) > 190:   # Not maximum, but close to it
            self.cwDecodedText.delete('1.0')
        self.cwDecodedText.insert('2.end',newchar)



        #
        #   resizeCanvas_CB and refreshCanvas work together to deal with any resizing of the canvas.
        #   When a resize is detected, resizeCanvas_CB is called and it schedules a future execution of
        #   refreshCanvas.  But resizing generates a lot of callbacks... So if the resize process is underway
        #   each new event cancels the prior "after refreshCanvas" and creates a new one 100ms in the future
        #   Eventually the events end, and the last refreshCanvas future event runs and replots the data
        #

    def resizeCanvas_CB(self, event=None):
        if self.windowResized:
            self.master.after_cancel(self.windowResizedObj)
        else:
            self.windowResized = True
        self.windowResizedObj = self.master.after(100, self.refreshCanvas)

    def refreshCanvas(self):

        #
        #   Update canvas size
        #
        self.frequencyPlotCanvas_height = self.frequencyPlotCanvas.winfo_height()
        self.frequencyPlotCanvas_width = self.frequencyPlotCanvas.winfo_width()

        if self.frequencyLineObj[0] == None:  # if nothing plotted, just return
            return

        x_width, x_stretch, y_stretch = gv.calculatePlotParameters(self.frequencyPlotCanvas_width, self.FFTSIZE,
                                                                   self.FREQ_X_GAP,
                                                                   self.frequencyPlotCanvas_height,
                                                                   self.FREQ_Y_MAX,
                                                                   self.FREQ_Y_GAP)

        for x in range(self.FFTSIZE):

            ymag = self.frequencyLineYmag[x]

            self.drawBars(x, ymag, x_width, x_stretch, y_stretch)

            self.updateTargetFreqBars()


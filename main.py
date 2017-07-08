from PyQt4 import QtGui, QtCore
import sys
import os
from os import path
from os.path import splitext

from Screens import checkscreen
from Screens import analysisscreen
from Screens import timescreen
from Screens import freqscreen
from Screens import powerscreen
from Screens import spectscreen
from Screens import waitscreen
from Screens import bandpassscreen

from Modules import SignalData
from Modules import checkmodules
from Modules import read_dat
from Modules import read_wav
from Modules import read_txt
from Modules import signal_plot
from Modules import signal_plot_freq
from Modules import signal_plot_power
from Modules import spectrogram
from Modules import bandpass


class ValidFreq(QtGui.QValidator):
    def __init__(self):
        QtGui.QValidator.__init__(self)

    def validate(self, formdata, pos):
        decimal = 0

        if(formdata == "."):
            return (QtGui.QValidator.Acceptable, formdata, pos)
        if(formdata != ""):
            try:
                freq = float(formdata)

                if("." in formdata):
                    decimal = len(formdata.split(".")[1])

                if(freq > 1000 or decimal > 4 or freq < 0):
                    return (QtGui.QValidator.Invalid, formdata, pos)
            except:
                return (QtGui.QValidator.Invalid, formdata, pos)

        return (QtGui.QValidator.Acceptable, formdata, pos)


class ControlScreen(QtGui.QMainWindow, analysisscreen.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()

        self.setupUi(self)

        self.SignalMeta = SignalData.Signal()
        self.addlogo()
        self.initializeAnalysiscreen()
        self.TimeLaunchButton.clicked.connect(self.launchtimedomain)
        self.FourierLaunchButton.clicked.connect(self.launchfourier)
        self.PowerLaunchButton.clicked.connect(self.launchpower)
        self.SpectrogramLaunchButton.clicked.connect(self.launchspect)
        self.BandpassLaunchButton.clicked.connect(self.launchfilter)

    def addlogo(self):
        image_directory = path.join(os.getcwd(), 'img')
        imagefile = path.join(image_directory, 'logo_small.png')
        pixmap = QtGui.QPixmap(imagefile)
        self.LogoDisplay.setPixmap(pixmap)

        image_directory = path.join(os.getcwd(), 'img')
        imagefile = path.join(image_directory, 'wrong_file.png')
        pixmap = QtGui.QPixmap(imagefile)
        self.FileLogoDisplay.setPixmap(pixmap)

    def launchfileselect(self):
        filename = QtGui.QFileDialog.getOpenFileName()
        _, file_extension = os.path.splitext(filename)
        if file_extension != ".wav" and file_extension != ".dat" and file_extension != ".txt":
            self.FileNameDisplay.clear()
            self.setVizualizationside(False)
            choice = QtGui.QMessageBox.warning(
                self, "Error", "Only .dat or .wav .txt file extension supported", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            if choice == QtGui.QMessageBox.Ok:
                pass
        else:
            self.FileNameDisplay.setText(filename)
            if file_extension == ".wav":
                image_directory = path.join(os.getcwd(), 'img')
                imagefile = path.join(image_directory, 'wav_file.png')
                pixmap = QtGui.QPixmap(imagefile)
                self.FileLogoDisplay.setPixmap(pixmap)
            elif file_extension == ".dat":
                image_directory = path.join(os.getcwd(), 'img')
                imagefile = path.join(image_directory, 'dat_file.png')
                pixmap = QtGui.QPixmap(imagefile)
                self.FileLogoDisplay.setPixmap(pixmap)
            else:
                image_directory = path.join(os.getcwd(), 'img')
                imagefile = path.join(image_directory, 'text_file.png')
                pixmap = QtGui.QPixmap(imagefile)
                self.FileLogoDisplay.setPixmap(pixmap)

    def checkvalue(self):
        message = "Ok"
        value = True
        Fsample = 0.0
        Fcentre = 0.0

        if(self.FileNameDisplay.text() == ""):
            message = "Please Select data file."
            value = False
        if(self.SampleFreqInput.text() != "" and value):
            Fsample = float(self.SampleFreqInput.text())
            if(Fsample == 0):
                message = "Sampling Frequency cannot be zero"
                value = False
        if(self.SampleFreqInput.text() == ""and value):
            message = "Please enter Sampling Frequency"
            value = False
        if(self.CentreFreqInput.text() != "" and value):
            Fcentre = float(self.CentreFreqInput.text())
            if(Fcentre == 0):
                message = "Centre Frequency cannot be zero"
                value = False
        if(self.CentreFreqInput.text() == "" and value):
            message = "Please enter Centre Frequency"
            value = False

        return (value, message, Fsample, Fcentre)

    def importvalue(self):
        result = self.checkvalue()
        if(not result[0]):
            self.setVizualizationside(False)
            choice = QtGui.QMessageBox.warning(self, "Error", str(
                result[1]), QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            if choice == QtGui.QMessageBox.Ok:
                pass
        else:
            filename = self.FileNameDisplay.text()
            file_extension = os.path.splitext(filename)[1]
            Fsample = result[2]
            Fcentre = result[3]
            if(file_extension == ".wav"):
                data = read_wav.loaddata(filename)
            elif(file_extension == ".dat"):
                data = read_dat.loaddata(filename)
            else:
                data = read_txt.loaddata(filename)

            self.SignalMeta.setvalues(filename=filename, filetype=file_extension,
                                      filedata=data, Fsample=Fsample * 1e6, Fcentre=Fcentre * 1e6)

            self.setVizualizationside(True)

    def setVizualizationside(self, value):
        self.TimeLaunchButton.setEnabled(value)
        self.FourierLaunchButton.setEnabled(value)
        self.PowerLaunchButton.setEnabled(value)
        self.SpectrogramLaunchButton.setEnabled(value)
        self.BandpassLaunchButton.setEnabled(value)

    def initializeAnalysiscreen(self):
        self.MainTab.setEnabled(True)

        self.validator = ValidFreq()
        self.SampleFreqInput.setValidator(self.validator)
        self.CentreFreqInput.setValidator(self.validator)

        self.setVizualizationside(False)
        self.FileSelectButton.clicked.connect(self.launchfileselect)
        self.ImportValueButton.clicked.connect(self.importvalue)

    def launchtimedomain(self):
        self.timescreenwindow = TimeDomainScreen(self.SignalMeta)
        self.timescreenwindow.exec_()

    def launchfourier(self):
        self.freqscreenwindow = FreqDomainScreen(self.SignalMeta)
        self.freqscreenwindow.exec_()

    def launchpower(self):
        self.powerscreenwindow = PowerDomainScreen(self.SignalMeta)
        self.powerscreenwindow.exec_()

    def launchspect(self):
        self.spectscreenwindow = SpectDomainScreen(self.SignalMeta)
        self.spectscreenwindow.exec_()

    def launchfilter(self):
        self.filterscreenwindow = FilterDomainScreen(self.SignalMeta)
        self.filterscreenwindow.exec_()


class TimeDomainScreen(QtGui.QDialog, timescreen.Ui_Dialog):

    def __init__(self, SignalMeta):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.SignalInfo = SignalMeta
        self.initialize()

    def initialize(self):

        image_directory = path.join(os.getcwd(), 'img')
        imagefile = path.join(image_directory, 'logo_small.png')
        pixmap = QtGui.QPixmap(imagefile)
        self.LogoDisplay.setPixmap(pixmap)

        value = self.SignalInfo.getvalues()

        if(value[1] == ".wav"):
            time = int(len(value[2]) / value[3])
            image_directory = path.join(os.getcwd(), 'img')
            imagefile = path.join(image_directory, 'wav_file.png')
            pixmap = QtGui.QPixmap(imagefile)
            self.FileLogoDisplay.setPixmap(pixmap)
        elif(value[1] == ".dat"):
            time = int(len(value[2]) / (2 * value[3]))
            image_directory = path.join(os.getcwd(), 'img')
            imagefile = path.join(image_directory, 'dat_file.png')
            pixmap = QtGui.QPixmap(imagefile)
            self.FileLogoDisplay.setPixmap(pixmap)
        else:
            time = int(len(value[2]) / (value[3]))
            image_directory = path.join(os.getcwd(), 'img')
            imagefile = path.join(image_directory, 'txt_file.png')
            pixmap = QtGui.QPixmap(imagefile)
            self.FileLogoDisplay.setPixmap(pixmap)

        self.FileNameDisplay.setText(value[0])
        self.SampleFreqDisplay.setText(str(value[3]))
        self.CentreFreqDisplay.setText(str(value[4]))
        self.TimeSignalDisplay.setText(str(time))

        validator1 = QtGui.QIntValidator(0, time - 2, self)
        self.StartTimeInput.setValidator(validator1)
        validator2 = QtGui.QIntValidator(0, time - 1, self)
        self.EndTimeInput.setValidator(validator2)

        self.ActionButton.clicked.connect(self.TimeDomainPlot)

    def TimeDomainPlot(self):

        start = int(self.StartTimeInput.text())
        end = int(self.EndTimeInput.text())
        signal_plot.SignalTimePlot(self.SignalInfo, start, end)


class FreqDomainScreen(QtGui.QDialog, freqscreen.Ui_Dialog):

    def __init__(self, SignalMeta):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.SignalInfo = SignalMeta
        self.initialize()

    def initialize(self):

        image_directory = path.join(os.getcwd(), 'img')
        imagefile = path.join(image_directory, 'logo_small.png')
        pixmap = QtGui.QPixmap(imagefile)
        self.LogoDisplay.setPixmap(pixmap)

        value = self.SignalInfo.getvalues()

        if(value[1] == ".wav"):
            time = int(len(value[2]) / value[3])
            image_directory = path.join(os.getcwd(), 'img')
            imagefile = path.join(image_directory, 'wav_file.png')
            pixmap = QtGui.QPixmap(imagefile)
            self.FileLogoDisplay.setPixmap(pixmap)
        elif(value[1] == ".dat"):
            time = int(len(value[2]) / (2 * value[3]))
            image_directory = path.join(os.getcwd(), 'img')
            imagefile = path.join(image_directory, 'dat_file.png')
            pixmap = QtGui.QPixmap(imagefile)
            self.FileLogoDisplay.setPixmap(pixmap)
        else:
            time = int(len(value[2]) / (value[3]))
            image_directory = path.join(os.getcwd(), 'img')
            imagefile = path.join(image_directory, 'txt_file.png')
            pixmap = QtGui.QPixmap(imagefile)
            self.FileLogoDisplay.setPixmap(pixmap)

        self.FileNameDisplay.setText(value[0])
        self.SampleFreqDisplay.setText(str(value[3]))
        self.CentreFreqDisplay.setText(str(value[4]))
        self.TimeSignalDisplay.setText(str(time))

        validator1 = QtGui.QIntValidator(0, time - 2, self)
        self.StartTimeInput.setValidator(validator1)
        validator2 = QtGui.QIntValidator(0, time - 1, self)
        self.EndTimeInput.setValidator(validator2)

        self.ActionButton.clicked.connect(self.FreqDomainPlot)

    def FreqDomainPlot(self):

        start = int(self.StartTimeInput.text())
        end = int(self.EndTimeInput.text())
        signal_plot_freq.SignalFreqPlot(self.SignalInfo, start, end)


class PowerDomainScreen(QtGui.QDialog, powerscreen.Ui_Dialog):

    def __init__(self, SignalMeta):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.SignalInfo = SignalMeta
        self.initialize()

    def initialize(self):

        image_directory = path.join(os.getcwd(), 'img')
        imagefile = path.join(image_directory, 'logo_small.png')
        pixmap = QtGui.QPixmap(imagefile)
        self.LogoDisplay.setPixmap(pixmap)

        value = self.SignalInfo.getvalues()

        if(value[1] == ".wav"):
            time = int(len(value[2]) / value[3])
            image_directory = path.join(os.getcwd(), 'img')
            imagefile = path.join(image_directory, 'wav_file.png')
            pixmap = QtGui.QPixmap(imagefile)
            self.FileLogoDisplay.setPixmap(pixmap)
        elif(value[1] == ".dat"):
            time = int(len(value[2]) / (2 * value[3]))
            image_directory = path.join(os.getcwd(), 'img')
            imagefile = path.join(image_directory, 'dat_file.png')
            pixmap = QtGui.QPixmap(imagefile)
            self.FileLogoDisplay.setPixmap(pixmap)
        else:
            time = int(len(value[2]) / (value[3]))
            image_directory = path.join(os.getcwd(), 'img')
            imagefile = path.join(image_directory, 'txt_file.png')
            pixmap = QtGui.QPixmap(imagefile)
            self.FileLogoDisplay.setPixmap(pixmap)

        self.FileNameDisplay.setText(value[0])
        self.SampleFreqDisplay.setText(str(value[3]))
        self.CentreFreqDisplay.setText(str(value[4]))
        self.TimeSignalDisplay.setText(str(time))

        validator1 = QtGui.QIntValidator(0, time - 2, self)
        self.StartTimeInput.setValidator(validator1)
        validator2 = QtGui.QIntValidator(0, time - 1, self)
        self.EndTimeInput.setValidator(validator2)

        self.ActionButton.clicked.connect(self.PowerDomainPlot)

    def PowerDomainPlot(self):

        start = int(self.StartTimeInput.text())
        end = int(self.EndTimeInput.text())
        signal_plot_power.SignalPowerPlot(self.SignalInfo, start, end)


class SpectDomainScreen(QtGui.QDialog, spectscreen.Ui_Dialog):

    def __init__(self, SignalMeta):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.SignalInfo = SignalMeta
        self.initialize()

    def initialize(self):

        image_directory = path.join(os.getcwd(), 'img')
        imagefile = path.join(image_directory, 'logo_small.png')
        pixmap = QtGui.QPixmap(imagefile)
        self.LogoDisplay.setPixmap(pixmap)

        value = self.SignalInfo.getvalues()

        if(value[1] == ".wav"):
            time = int(len(value[2]) / value[3])
            image_directory = path.join(os.getcwd(), 'img')
            imagefile = path.join(image_directory, 'wav_file.png')
            pixmap = QtGui.QPixmap(imagefile)
            self.FileLogoDisplay.setPixmap(pixmap)
        elif(value[1] == ".dat"):
            time = int(len(value[2]) / (2 * value[3]))
            image_directory = path.join(os.getcwd(), 'img')
            imagefile = path.join(image_directory, 'dat_file.png')
            pixmap = QtGui.QPixmap(imagefile)
            self.FileLogoDisplay.setPixmap(pixmap)
        else:
            time = int(len(value[2]) / (value[3]))
            image_directory = path.join(os.getcwd(), 'img')
            imagefile = path.join(image_directory, 'txt_file.png')
            pixmap = QtGui.QPixmap(imagefile)
            self.FileLogoDisplay.setPixmap(pixmap)

        self.FileNameDisplay.setText(value[0])
        self.SampleFreqDisplay.setText(str(value[3]))
        self.CentreFreqDisplay.setText(str(value[4]))
        self.TimeSignalDisplay.setText(str(time))

        self.ActionButton.clicked.connect(self.SpectDomainPlot)

    def SpectDomainPlot(self):

        cmap = self.ColormapInput.currentText()
        WaitWindow = WaitScreenReq()
        spectrogram.SpectrogramPlot(self.SignalInfo, cmap, WaitWindow)


class FilterDomainScreen(QtGui.QDialog, bandpassscreen.Ui_Dialog):

    def __init__(self, SignalMeta):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.SignalInfo = SignalMeta
        self.initialize()

    def initialize(self):

        image_directory = path.join(os.getcwd(), 'img')
        imagefile = path.join(image_directory, 'logo_small.png')
        pixmap = QtGui.QPixmap(imagefile)
        self.LogoDisplay.setPixmap(pixmap)

        value = self.SignalInfo.getvalues()

        if(value[1] == ".wav"):
            time = int(len(value[2]) / value[3])
            image_directory = path.join(os.getcwd(), 'img')
            imagefile = path.join(image_directory, 'wav_file.png')
            pixmap = QtGui.QPixmap(imagefile)
            self.FileLogoDisplay.setPixmap(pixmap)
        else:
            time = int(len(value[2]) / (2 * value[3]))
            image_directory = path.join(os.getcwd(), 'img')
            imagefile = path.join(image_directory, 'dat_file.png')
            pixmap = QtGui.QPixmap(imagefile)
            self.FileLogoDisplay.setPixmap(pixmap)

        self.FileNameDisplay.setText(value[0])
        self.SampleFreqDisplay.setText(str(value[3]))
        self.CentreFreqDisplay.setText(str(value[4]))
        self.TimeSignalDisplay.setText(str(time))

        validator = QtGui.QDoubleValidator(self)
        validator.setBottom(0.0)
        validator.setDecimals(4)
        self.FLowInput.setValidator(validator)
        self.FHighInput.setValidator(validator)

        self.ActionButton.clicked.connect(self.FilterPlot)

    def check(self):
        Flow = self.FLowInput.text()
        Fhigh = self.FHighInput.text()
        filename = self.FileSaveInput.text()

        if(Flow == "" or Fhigh == "" or filename == ""):
            choice = QtGui.QMessageBox.warning(
                self, "Error", "Please fill all the fields", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)

            if choice == QtGui.QMessageBox.Ok:
                pass

            return None, None, None, False

        if("." in filename):
            choice = QtGui.QMessageBox.warning(
                self, "Error", "No file extension allowed", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)

            if choice == QtGui.QMessageBox.Ok:
                pass

            return None, None, None, False

        Flow = float(Flow)
        Fhigh = float(Fhigh)
        fs = float(self.SampleFreqDisplay.text())
        fc = float(self.CentreFreqDisplay.text())
        mega = float(1e6)
        LowerLimit = (fc / mega) - (fs / (2 * mega))
        HigherLimit = (fc / mega) + (fs / (2 * mega))

        if(Flow >= Fhigh):
            choice = QtGui.QMessageBox.warning(
                self, "Error", "Flow cannot be greater than FHigh", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)

            if choice == QtGui.QMessageBox.Ok:
                pass

            return None, None, None, False

        if(Flow < LowerLimit or Flow > HigherLimit):
            choice = QtGui.QMessageBox.warning(
                self, "Error", "Invalid Flow", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)

            if choice == QtGui.QMessageBox.Ok:
                pass

            return None, None, None, False

        if(Fhigh < LowerLimit or Fhigh > HigherLimit):
            choice = QtGui.QMessageBox.warning(
                self, "Error", "Invaid FHigh", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)

            if choice == QtGui.QMessageBox.Ok:
                pass

            return None, None, None, False

        return Flow * 1e6, Fhigh * 1e6, filename, True

    def FilterPlot(self):

        Flow, Fhigh, filename, isvalid = self.check()
        if(isvalid):
            WaitWindow = WaitScreenReq()
            filename = filename + ".txt"
            bandpass.filter(self.SignalInfo, Flow, Fhigh, filename, WaitWindow)


class WaitScreenReq(QtGui.QDialog, waitscreen.Ui_Dialog):
    """docstring for CheckDependencies"""

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

    def updateprogress(self, current, levels):
        new_value = int(((current + 1) * 100) / levels)
        self.ProgressBar.setValue(new_value)

    def close(self):
        self.accept()


def main():
    app = QtGui.QApplication(sys.argv)
    MainWindow = ControlScreen()
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

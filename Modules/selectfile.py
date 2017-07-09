import sys
import os
from os.path import splitext
from PyQt4 import QtGui, QtCore

from Modules import SignalData

from Screens import SelectScreen

SignalMeta = SignalData.Signal()


class ImportScreen(QtGui.QDialog, SelectScreen.Ui_Dialog):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.initialize()

    def initialize(self):
        self.FileButton.clicked.connect(self.choosefile)
        self.ActionButton.clicked.connect(self.importvalues)

    def choosefile(self):
        filename = QtGui.QFileDialog.getOpenFileName()
        self.FileNameLabel.setText(filename)

    def importvalues(self):
        filename = self.FileNameLabel.text()
        _, file_extension = os.path.splitext(filename)
        fs = float(self.SampleFreqInput.text())
        fc = float(self.CentreFreqInput.text())
        SignalMeta.setvalues(filename=filename, filetype=file_extension,
                             filedata=None, Fsample=fs * 1e6, Fcentre=fc * 1e6)
        self.accept()


def select():

    app = QtGui.QApplication(sys.argv)
    Window = ImportScreen()
    Window.show()
    app.exec_()

    return SignalMeta

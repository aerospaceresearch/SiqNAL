import sys
import os
from os.path import splitext
from PyQt4 import QtGui, QtCore

from Screens import FolderScreen

foldername = ""


class ImportScreen(QtGui.QDialog, FolderScreen.Ui_Dialog):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.initialize()

    def initialize(self):
        self.FileButton.clicked.connect(self.choosefile)
        self.ActionButton.clicked.connect(self.importvalues)

    def choosefile(self):
        filename = str(QtGui.QFileDialog.getExistingDirectory(
            self, "Select Directory"))
        self.FileNameLabel.setText(filename)

    def importvalues(self):
        global foldername
        foldername = self.FileNameLabel.text()
        self.accept()


def select():

    app = QtGui.QApplication(sys.argv)
    Window = ImportScreen()
    Window.show()
    app.exec_()

    return foldername
    # return SignalMeta

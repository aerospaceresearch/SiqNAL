from PyQt4 import QtGui, QtCore
import sys
import os
from os import path

from Modules import checkmodules

from Screens import checkscreen


class CheckDependencies(QtGui.QDialog, checkscreen.Ui_checkscreen):
    """docstring for CheckDependencies"""

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.addlogo()
        self.StartButton.clicked.connect(self.check)
        self.ProceedButton.clicked.connect(self.close)

    def reset(self):
        self.ProgressBar.setValue(int(0))
        self.ProgressDisplay.clear()

    def addlogo(self):
        image_directory = path.join(os.getcwd(), 'img')
        imagefile = path.join(image_directory, 'logo.png')
        pixmap = QtGui.QPixmap(imagefile)
        self.LogoDisplay.setPixmap(pixmap)

    def updateprogress(self, levels):
        current_value = self.ProgressBar.value()
        new_value = current_value + int(100 / levels)
        self.ProgressBar.setValue(new_value)

    def check(self):
        results = True
        try:
            file = open("requirements.txt", "r")
            lines = file.readlines()
            levels = len(lines) + 1

            if (self.ProgressBar.value() != 0):
                self.reset()

            self.ProgressDisplay.append(
                10 * "#" + " Checking Required Dependencies " + 10 * "#" + "\n")

            self.ProgressDisplay.append(
                10 * "*" + " Checking for Python Version " + 10 * "*")
            value = checkmodules.check_version()
            results = results and value[0]
            self.ProgressDisplay.append(
                10 * "=" + " {} ".format(value[1]) + 10 * "=" + "\n")
            self.updateprogress(levels)

            for line in lines:
                package_name, package_version = line.split(">=")
                self.ProgressDisplay.append(
                    10 * "*" + " Checking for Module Name: {} ".format(package_name) + 10 * "*")
                value = checkmodules.check_lib(package_name, package_version)
                results = results and value[0]
                self.ProgressDisplay.append(
                    10 * "=" + " {} ".format(value[1]) + 10 * "=" + "\n")
                self.updateprogress(levels)

            if results:
                self.ProgressDisplay.append(
                    10 * "%" + " All dependencies satisfied " + 10 * "%")
                self.StartButton.setEnabled(False)
                self.ProceedButton.setEnabled(True)
            else:
                self.ProgressDisplay.append(
                    10 * "%" + " All dependencies not satisfied. Please resolve them using console output. " + 10 * "%")

        except FileNotFoundError:
            self.ProgressDisplay.append(
                10 * "*" + " Requirements.txt not found. Please include to check dependencies " + 10 * "*")

    def close(self):
        sys.exit(-1)


def main():
    app = QtGui.QApplication(sys.argv)
    Window = CheckDependencies()
    Window.show()
    app.exec_()


if __name__ == "__main__":
    main()

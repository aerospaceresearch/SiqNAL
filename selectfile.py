import sys
import os
from os.path import splitext
from PyQt4.QtGui import *


def select():

    app = QApplication(sys.argv)
    window = QWidget()

    filename = QFileDialog.getOpenFileName(window, 'Select File', './data')
    _, file_extension = os.path.splitext(filename)

    return filename, file_extension

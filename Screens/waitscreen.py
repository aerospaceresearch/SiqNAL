# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/matrix/Desktop/siqnal/qt/waitscreen.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 300)
        Dialog.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.WaitTextLabel = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Sans Serif"))
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.WaitTextLabel.setFont(font)
        self.WaitTextLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.WaitTextLabel.setObjectName(_fromUtf8("WaitTextLabel"))
        self.verticalLayout.addWidget(self.WaitTextLabel)
        self.ProgressBar = QtGui.QProgressBar(Dialog)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ProgressBar.sizePolicy().hasHeightForWidth())
        self.ProgressBar.setSizePolicy(sizePolicy)
        self.ProgressBar.setProperty("value", 0)
        self.ProgressBar.setInvertedAppearance(False)
        self.ProgressBar.setObjectName(_fromUtf8("ProgressBar"))
        self.verticalLayout.addWidget(self.ProgressBar)
        self.DummyLabel = QtGui.QLabel(Dialog)
        self.DummyLabel.setText(_fromUtf8(""))
        self.DummyLabel.setObjectName(_fromUtf8("DummyLabel"))
        self.verticalLayout.addWidget(self.DummyLabel)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.WaitTextLabel.setText(_translate(
            "Dialog", "Please Wait :)", None))

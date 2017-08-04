# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FolderScreen.ui'
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
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.ImportLabel = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Sans Serif"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.ImportLabel.setFont(font)
        self.ImportLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ImportLabel.setObjectName(_fromUtf8("ImportLabel"))
        self.verticalLayout.addWidget(self.ImportLabel)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.FileNameLabel = QtGui.QLineEdit(Dialog)
        self.FileNameLabel.setReadOnly(True)
        self.FileNameLabel.setObjectName(_fromUtf8("FileNameLabel"))
        self.horizontalLayout_3.addWidget(self.FileNameLabel)
        self.FileButton = QtGui.QPushButton(Dialog)
        self.FileButton.setObjectName(_fromUtf8("FileButton"))
        self.horizontalLayout_3.addWidget(self.FileButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.ActionButton = QtGui.QPushButton(Dialog)
        self.ActionButton.setObjectName(_fromUtf8("ActionButton"))
        self.verticalLayout.addWidget(self.ActionButton)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.ImportLabel.setText(_translate(
            "Dialog", "Folder Select Screen", None))
        self.FileButton.setText(_translate("Dialog", "Browse", None))
        self.ActionButton.setText(_translate("Dialog", "Confirm", None))

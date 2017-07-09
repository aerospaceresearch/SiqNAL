# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SelectScreen.ui'
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
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.SampleFreqLabel = QtGui.QLabel(Dialog)
        self.SampleFreqLabel.setObjectName(_fromUtf8("SampleFreqLabel"))
        self.horizontalLayout.addWidget(self.SampleFreqLabel)
        self.SampleFreqInput = QtGui.QLineEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SampleFreqInput.sizePolicy().hasHeightForWidth())
        self.SampleFreqInput.setSizePolicy(sizePolicy)
        self.SampleFreqInput.setObjectName(_fromUtf8("SampleFreqInput"))
        self.horizontalLayout.addWidget(self.SampleFreqInput)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.CentreFreqLabel = QtGui.QLabel(Dialog)
        self.CentreFreqLabel.setObjectName(_fromUtf8("CentreFreqLabel"))
        self.horizontalLayout_2.addWidget(self.CentreFreqLabel)
        self.CentreFreqInput = QtGui.QLineEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CentreFreqInput.sizePolicy().hasHeightForWidth())
        self.CentreFreqInput.setSizePolicy(sizePolicy)
        self.CentreFreqInput.setObjectName(_fromUtf8("CentreFreqInput"))
        self.horizontalLayout_2.addWidget(self.CentreFreqInput)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.ActionButton = QtGui.QPushButton(Dialog)
        self.ActionButton.setObjectName(_fromUtf8("ActionButton"))
        self.verticalLayout.addWidget(self.ActionButton)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.ImportLabel.setText(_translate("Dialog", "Import Screen", None))
        self.FileButton.setText(_translate("Dialog", "Browse", None))
        self.SampleFreqLabel.setText(_translate("Dialog", "Sampling Frequency (MHz)", None))
        self.CentreFreqLabel.setText(_translate("Dialog", "Centre Frequency (MHz)", None))
        self.ActionButton.setText(_translate("Dialog", "Import", None))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'timescreen.ui'
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
        Dialog.resize(620, 300)
        self.verticalLayout_5 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.LogoDisplay = QtGui.QLabel(Dialog)
        self.LogoDisplay.setText(_fromUtf8(""))
        self.LogoDisplay.setAlignment(QtCore.Qt.AlignCenter)
        self.LogoDisplay.setObjectName(_fromUtf8("LogoDisplay"))
        self.horizontalLayout_3.addWidget(self.LogoDisplay)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.ProgramNameDisplay = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Sans Serif"))
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.ProgramNameDisplay.setFont(font)
        self.ProgramNameDisplay.setAlignment(QtCore.Qt.AlignCenter)
        self.ProgramNameDisplay.setObjectName(_fromUtf8("ProgramNameDisplay"))
        self.verticalLayout.addWidget(self.ProgramNameDisplay)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.ProjectNameDisplay = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.ProjectNameDisplay.setFont(font)
        self.ProjectNameDisplay.setObjectName(_fromUtf8("ProjectNameDisplay"))
        self.horizontalLayout.addWidget(self.ProjectNameDisplay)
        self.CodeNameDisplay = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setItalic(True)
        self.CodeNameDisplay.setFont(font)
        self.CodeNameDisplay.setObjectName(_fromUtf8("CodeNameDisplay"))
        self.horizontalLayout.addWidget(self.CodeNameDisplay)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.MentorNameDisplay = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.MentorNameDisplay.setFont(font)
        self.MentorNameDisplay.setObjectName(_fromUtf8("MentorNameDisplay"))
        self.horizontalLayout_2.addWidget(self.MentorNameDisplay)
        self.AuthorNameDisplay = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.AuthorNameDisplay.setFont(font)
        self.AuthorNameDisplay.setObjectName(_fromUtf8("AuthorNameDisplay"))
        self.horizontalLayout_2.addWidget(self.AuthorNameDisplay)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.MetaDisplay = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.MetaDisplay.setFont(font)
        self.MetaDisplay.setAlignment(QtCore.Qt.AlignCenter)
        self.MetaDisplay.setObjectName(_fromUtf8("MetaDisplay"))
        self.verticalLayout_2.addWidget(self.MetaDisplay)
        self.FileLogoDisplay = QtGui.QLabel(Dialog)
        self.FileLogoDisplay.setText(_fromUtf8(""))
        self.FileLogoDisplay.setAlignment(QtCore.Qt.AlignCenter)
        self.FileLogoDisplay.setObjectName(_fromUtf8("FileLogoDisplay"))
        self.verticalLayout_2.addWidget(self.FileLogoDisplay)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.FileNameLabel = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.FileNameLabel.setFont(font)
        self.FileNameLabel.setObjectName(_fromUtf8("FileNameLabel"))
        self.horizontalLayout_7.addWidget(self.FileNameLabel)
        self.FileNameDisplay = QtGui.QLineEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FileNameDisplay.sizePolicy().hasHeightForWidth())
        self.FileNameDisplay.setSizePolicy(sizePolicy)
        self.FileNameDisplay.setReadOnly(True)
        self.FileNameDisplay.setObjectName(_fromUtf8("FileNameDisplay"))
        self.horizontalLayout_7.addWidget(self.FileNameDisplay)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.SampleFreqLabel = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.SampleFreqLabel.setFont(font)
        self.SampleFreqLabel.setObjectName(_fromUtf8("SampleFreqLabel"))
        self.horizontalLayout_4.addWidget(self.SampleFreqLabel)
        self.SampleFreqDisplay = QtGui.QLineEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SampleFreqDisplay.sizePolicy().hasHeightForWidth())
        self.SampleFreqDisplay.setSizePolicy(sizePolicy)
        self.SampleFreqDisplay.setReadOnly(True)
        self.SampleFreqDisplay.setObjectName(_fromUtf8("SampleFreqDisplay"))
        self.horizontalLayout_4.addWidget(self.SampleFreqDisplay)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.CentreFreqLabel = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.CentreFreqLabel.setFont(font)
        self.CentreFreqLabel.setObjectName(_fromUtf8("CentreFreqLabel"))
        self.horizontalLayout_5.addWidget(self.CentreFreqLabel)
        self.CentreFreqDisplay = QtGui.QLineEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CentreFreqDisplay.sizePolicy().hasHeightForWidth())
        self.CentreFreqDisplay.setSizePolicy(sizePolicy)
        self.CentreFreqDisplay.setReadOnly(True)
        self.CentreFreqDisplay.setObjectName(_fromUtf8("CentreFreqDisplay"))
        self.horizontalLayout_5.addWidget(self.CentreFreqDisplay)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.LengthSIgnalLabel = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.LengthSIgnalLabel.setFont(font)
        self.LengthSIgnalLabel.setObjectName(_fromUtf8("LengthSIgnalLabel"))
        self.horizontalLayout_6.addWidget(self.LengthSIgnalLabel)
        self.TimeSignalDisplay = QtGui.QLineEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TimeSignalDisplay.sizePolicy().hasHeightForWidth())
        self.TimeSignalDisplay.setSizePolicy(sizePolicy)
        self.TimeSignalDisplay.setReadOnly(True)
        self.TimeSignalDisplay.setObjectName(_fromUtf8("TimeSignalDisplay"))
        self.horizontalLayout_6.addWidget(self.TimeSignalDisplay)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_10.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.AnalysisDisplay = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.AnalysisDisplay.setFont(font)
        self.AnalysisDisplay.setAlignment(QtCore.Qt.AlignCenter)
        self.AnalysisDisplay.setObjectName(_fromUtf8("AnalysisDisplay"))
        self.verticalLayout_3.addWidget(self.AnalysisDisplay)
        self.DummyLabel = QtGui.QLabel(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DummyLabel.sizePolicy().hasHeightForWidth())
        self.DummyLabel.setSizePolicy(sizePolicy)
        self.DummyLabel.setMinimumSize(QtCore.QSize(294, 0))
        self.DummyLabel.setText(_fromUtf8(""))
        self.DummyLabel.setObjectName(_fromUtf8("DummyLabel"))
        self.verticalLayout_3.addWidget(self.DummyLabel)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.StartTimeLabel = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.StartTimeLabel.setFont(font)
        self.StartTimeLabel.setObjectName(_fromUtf8("StartTimeLabel"))
        self.horizontalLayout_9.addWidget(self.StartTimeLabel)
        self.StartTimeInput = QtGui.QLineEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.StartTimeInput.sizePolicy().hasHeightForWidth())
        self.StartTimeInput.setSizePolicy(sizePolicy)
        self.StartTimeInput.setObjectName(_fromUtf8("StartTimeInput"))
        self.horizontalLayout_9.addWidget(self.StartTimeInput)
        self.verticalLayout_3.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.EndTimeLabel = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.EndTimeLabel.setFont(font)
        self.EndTimeLabel.setObjectName(_fromUtf8("EndTimeLabel"))
        self.horizontalLayout_8.addWidget(self.EndTimeLabel)
        self.EndTimeInput = QtGui.QLineEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.EndTimeInput.sizePolicy().hasHeightForWidth())
        self.EndTimeInput.setSizePolicy(sizePolicy)
        self.EndTimeInput.setObjectName(_fromUtf8("EndTimeInput"))
        self.horizontalLayout_8.addWidget(self.EndTimeInput)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.ActionButton = QtGui.QPushButton(Dialog)
        self.ActionButton.setObjectName(_fromUtf8("ActionButton"))
        self.verticalLayout_3.addWidget(self.ActionButton)
        self.horizontalLayout_10.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_10)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.ProgramNameDisplay.setText(_translate("Dialog", "Google Summer of Code", None))
        self.ProjectNameDisplay.setText(_translate("Dialog", "Project Name: SIQNAL", None))
        self.CodeNameDisplay.setText(_translate("Dialog", "Code: <a href=\"https://github.com/aerospaceresearch/siqnal\">Github</a>", None))
        self.MentorNameDisplay.setText(_translate("Dialog", "Mentor: Andreas Horning", None))
        self.AuthorNameDisplay.setText(_translate("Dialog", "Author: Jay Krishna", None))
        self.MetaDisplay.setText(_translate("Dialog", "Meta Data", None))
        self.FileNameLabel.setText(_translate("Dialog", "File Name", None))
        self.SampleFreqLabel.setText(_translate("Dialog", "Sampling Frequency(Hz)", None))
        self.CentreFreqLabel.setText(_translate("Dialog", "Centre Frequency(Hz)", None))
        self.LengthSIgnalLabel.setText(_translate("Dialog", "Length of Signal(sec)", None))
        self.AnalysisDisplay.setText(_translate("Dialog", "Time Domain Vizualization Section", None))
        self.StartTimeLabel.setText(_translate("Dialog", "Start Time(sec)", None))
        self.StartTimeInput.setPlaceholderText(_translate("Dialog", "(Inclusive)", None))
        self.EndTimeLabel.setText(_translate("Dialog", "End Time(sec)", None))
        self.EndTimeInput.setPlaceholderText(_translate("Dialog", "(Exclusive)", None))
        self.ActionButton.setText(_translate("Dialog", "Plot", None))


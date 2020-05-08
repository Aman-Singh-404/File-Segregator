# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/aman/Desktop/File-Segregator/Interface/extensionMenu.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 330)
        Dialog.setMinimumSize(QtCore.QSize(500, 330))
        Dialog.setMaximumSize(QtCore.QSize(500, 330))
        self.addPB = QtWidgets.QPushButton(Dialog)
        self.addPB.setGeometry(QtCore.QRect(10, 300, 25, 25))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.addPB.setFont(font)
        self.addPB.setObjectName("addPB")
        self.removePB = QtWidgets.QPushButton(Dialog)
        self.removePB.setGeometry(QtCore.QRect(40, 300, 25, 25))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.removePB.setFont(font)
        self.removePB.setObjectName("removePB")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(324, 300, 166, 25))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.categoryTW = QtWidgets.QTreeWidget(Dialog)
        self.categoryTW.setGeometry(QtCore.QRect(5, 5, 490, 290))
        self.categoryTW.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.categoryTW.setTabKeyNavigation(False)
        self.categoryTW.setProperty("showDropIndicator", True)
        self.categoryTW.setAlternatingRowColors(True)
        self.categoryTW.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.categoryTW.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.categoryTW.setIndentation(25)
        self.categoryTW.setUniformRowHeights(False)
        self.categoryTW.setItemsExpandable(True)
        self.categoryTW.setAllColumnsShowFocus(False)
        self.categoryTW.setWordWrap(True)
        self.categoryTW.setHeaderHidden(False)
        self.categoryTW.setObjectName("categoryTW")
        self.categoryTW.headerItem().setTextAlignment(0, QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.categoryTW.headerItem().setFont(0, font)
        self.categoryTW.headerItem().setTextAlignment(1, QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.categoryTW.headerItem().setFont(1, font)
        self.categoryTW.header().setCascadingSectionResizes(False)
        self.categoryTW.header().setDefaultSectionSize(150)
        self.categoryTW.header().setMinimumSectionSize(150)
        self.categoryTW.header().setStretchLastSection(True)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Extension Menu"))
        self.addPB.setText(_translate("Dialog", "+"))
        self.removePB.setText(_translate("Dialog", "-"))
        self.categoryTW.headerItem().setText(0, _translate("Dialog", "   Category   "))
        self.categoryTW.headerItem().setText(1, _translate("Dialog", "Extensions"))

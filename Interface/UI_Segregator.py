# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Desktop/File-Segregator/Interface/Segregator.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(270, 300)
        MainWindow.setMinimumSize(QtCore.QSize(270, 300))
        MainWindow.setMaximumSize(QtCore.QSize(270, 300))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 270, 45))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(5, 50, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_1.setFont(font)
        self.label_1.setObjectName("label_1")
        self.line_1 = QtWidgets.QFrame(self.centralwidget)
        self.line_1.setGeometry(QtCore.QRect(0, 47, 270, 5))
        self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_1.setObjectName("line_1")
        self.desgCB = QtWidgets.QCheckBox(self.centralwidget)
        self.desgCB.setGeometry(QtCore.QRect(10, 120, 241, 25))
        self.desgCB.setObjectName("desgCB")
        self.segregatePB = QtWidgets.QPushButton(self.centralwidget)
        self.segregatePB.setGeometry(QtCore.QRect(140, 150, 120, 30))
        self.segregatePB.setObjectName("segregatePB")
        self.cancelPB = QtWidgets.QPushButton(self.centralwidget)
        self.cancelPB.setGeometry(QtCore.QRect(10, 150, 120, 30))
        self.cancelPB.setObjectName("cancelPB")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(0, 183, 270, 5))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setEnabled(False)
        self.label_2.setGeometry(QtCore.QRect(5, 185, 260, 50))
        self.label_2.setLineWidth(1)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.progressPB = QtWidgets.QProgressBar(self.centralwidget)
        self.progressPB.setEnabled(False)
        self.progressPB.setGeometry(QtCore.QRect(10, 245, 250, 25))
        self.progressPB.setProperty("value", 0)
        self.progressPB.setObjectName("progressPB")
        self.directoryL = QtWidgets.QLabel(self.centralwidget)
        self.directoryL.setGeometry(QtCore.QRect(10, 85, 250, 30))
        self.directoryL.setAutoFillBackground(False)
        self.directoryL.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 1px inset rgb(179, 176, 174);\n"
"border-radius: 2%;\n"
"")
        self.directoryL.setText("")
        self.directoryL.setObjectName("directoryL")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 270, 22))
        self.menuBar.setObjectName("menuBar")
        self.menufile = QtWidgets.QMenu(self.menuBar)
        self.menufile.setGeometry(QtCore.QRect(0, 0, 199, 100))
        self.menufile.setObjectName("menufile")
        MainWindow.setMenuBar(self.menuBar)
        self.actionModify = QtWidgets.QAction(MainWindow)
        self.actionModify.setObjectName("actionModify")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menufile.addAction(self.actionModify)
        self.menufile.addAction(self.actionExit)
        self.menuBar.addAction(self.menufile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Segregator"))
        self.label.setText(_translate("MainWindow", "File Segregator"))
        self.label_1.setText(_translate("MainWindow", "Enter directory path:"))
        self.desgCB.setText(_translate("MainWindow", "With desegregation of directory"))
        self.segregatePB.setText(_translate("MainWindow", "Segregate"))
        self.cancelPB.setText(_translate("MainWindow", "Cancel"))
        self.label_2.setText(_translate("MainWindow", "Wait! Process is ongoing...\n"
""))
        self.menufile.setTitle(_translate("MainWindow", "File"))
        self.actionModify.setText(_translate("MainWindow", "Extenstion category"))
        self.actionModify.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionExit.setText(_translate("MainWindow", "Close"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+X"))

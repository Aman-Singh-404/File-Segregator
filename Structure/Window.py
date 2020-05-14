import os
import shutil

from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox

from Interface.UI_Segregator import Ui_MainWindow
from Structure.ExtensionMenu import ExtensionMenu
from utils import FileSegregator


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.size())
        
        self.filesegregator = None
        self.process_activated = False
        self.safeDir = None
        self.total = 0
        
        self.directoryL.mouseDoubleClickEvent = self.browse

        self.actionExit.triggered.connect(self.close)
        self.actionModify.triggered.connect(self.openExtMenu)
        self.cancelPB.clicked.connect(self.close)
        self.segregatePB.clicked.connect(self.segregate)
    
    def browse(self, event):
        path = self.directoryL.text()
        path = QFileDialog.getExistingDirectory(self, "Select Directory", path)
        if path != "":
            self.directoryL.setText(path)

    def closeEvent(self, event):
        if self.process_activated:
            reply = QMessageBox.question(self, 'Alert', 'Stop segregation process?',QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                path = self.directoryL.text()
                shutil.rmtree(path)
                shutil.copytree(self.safeDir, path)
                shutil.rmtree(self.safeDir)
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
    
    def openExtMenu(self):
        extmenu = ExtensionMenu(self)
        extmenu.exec_()
    
    def segregate(self):
        path = self.directoryL.text()
        if path == "":
            QMessageBox.warning(self, 'Warning', 'Path location cannot be empty.')
        elif not(os.path.exists(path) and os.path.isdir(path)):
            QMessageBox.warning(self, 'Warning', "Directory doesn't exist.")
            self.directoryL.setText("")
        else:
            self.setWidget(False)
            self.safeDir = os.path.split(path)[1] + "_copy"
            self.process_activated = True
            shutil.copytree(path, self.safeDir)
            try:
                filesegregator = FileSegregator(path, self.updateProgress)
                self.total = filesegregator.total_size
                if self.desgCB.isChecked:
                    self.total *= 2
                filesegregator.segregateFolder(self.desgCB.isChecked())
                QMessageBox.information(self, 'Message Details', "Folder segregation completed.")
            except:
                QMessageBox.warning(self,'Warning',"Error occured.")
            shutil.rmtree(self.safeDir)
            self.process_activated = False
            self.setWidget(True)
    
    def setWidget(self, value):
        self.actionModify.setEnabled(value)
        self.cancelPB.setEnabled(value)
        self.desgCB.setEnabled(value)
        self.directoryL.setEnabled(value)
        self.label_1.setEnabled(value)
        self.segregatePB.setEnabled(value)
        
        self.label_2.setEnabled(not value)
        self.label_2.setText("")
        self.progressPB.setEnabled(not value)
        self.progressPB.setValue(0)
    
    def updateProgress(self, signal, message, bits_left):
        msg = "Wait! Process is ongoing...\nDesegregation in process\n"
        if signal:
            msg = "Wait! Process is ongoing...\nSegregation in process\n"
        self.label_2.setText(msg + message)
        self.progressPB.setValue(int((self.total - bits_left) / self.total * 100))

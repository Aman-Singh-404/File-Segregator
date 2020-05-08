import os
import json
import shutil

from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox

from Interface.UI_Segregator import Ui_MainWindow
from Structure.ExtensionMenu import ExtensionMenu


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.size())
        
        self.process_activated = False
        self.extensions = {}
        self.safeDir = None
        with open("extenstion_Category", 'r', encoding='utf-8') as fle:
            self.extensions = json.load(fle)
        
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
    
    def desegregateFolder(self, path, parent=None):
        msg = "Wait! Process is ongoing...\nDesegregation\n"
        if parent == None:
            parent = path
        for fs_obj in os.listdir(path):
            full_path = os.path.join(path, fs_obj)
            self.label_2.setText(msg + full_path)
            if os.path.isdir(full_path):
                self.desegregateFolder(full_path, parent)
                os.rmdir(full_path)
            else:
                if path != parent:
                    shutil.move(full_path, parent)

    def findCategory(self, fname):
        for label, categoryDict in self.extensions.items():
            for category, extensionList in categoryDict.items():
                for ext in extensionList:
                    if fname.endswith(ext.lower()):
                        return category
        return "Misc Files"

    def openExtMenu(self):
        extmenu = ExtensionMenu(self)
        extmenu.exec_()
    
    def segregate(self):
        path = self.directoryL.text()
        if path == "":
            QMessageBox.warning(self, 'Warning', 'Path location cannot be empty.', QMessageBox.Ok)
        elif not(os.path.exists(path) and os.path.isdir(path)):
            QMessageBox.warning(self,'Warning',"Directory doesn't exist.", QMessageBox.Ok)
            self.directoryL.setText("")
        else:
            self.label_1.setEnabled(False)
            self.directoryL.setEnabled(False)
            self.desgCB.setEnabled(False)
            self.cancelPB.setEnabled(False)
            self.segregatePB.setEnabled(False)
            
            self.label_2.setEnabled(True)
            self.progressPB.setEnabled(True)
            
            self.safeDir = os.path.split(path)[1] + "_copy"
            self.process_activated = True
            shutil.copytree(path, self.safeDir)
            self.segregateFolder(path, self.desgCB.isChecked())
            QMessageBox.information(self, 'Message Details', "Folder segregation completed.", QMessageBox.Ok)
            shutil.rmtree(self.safeDir)
            self.process_activated = False
            self.close()
    
    def segregateFolder(self, path, desg=False):
        msg = "Wait! Process is ongoing...\nSegregation\n"
        if desg:
            self.desegregateFolder(path)
        for fs_obj in os.listdir(path):
            full_path = os.path.join(path, fs_obj)
            self.label_2.setText(msg + full_path)
            if os.path.isfile(full_path):
                category = self.findCategory(fs_obj)
                os.makedirs(os.path.join(path, category), exist_ok=True)
                shutil.move(full_path, os.path.join(path, category, fs_obj))
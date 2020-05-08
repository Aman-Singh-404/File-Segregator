from PyQt5.QtWidgets import QDialog, QMessageBox

from Interface.UI_editCategory import Ui_Dialog


class EditCategory(QDialog):
    def __init__(self, parent, extensions, category='', extension=''):
        QDialog.__init__(self, parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())

        self.extensions = extensions
        self.prev_extension = [ext for ext in extension.split(', ')]
        self.ui.categoryLE.setText(category)
        self.ui.extensionTE.setText(extension)

        self.ui.buttonBox.accepted.connect(self.verify)
        self.ui.buttonBox.rejected.connect(self.reject)
    
    def checkExtension(self, extensions):
        extensionList = []
        for ext in extensions.split(','):
            ext = ext.strip()
            if ext.find(' ') != -1 or ext == '.' or ext == '' or ext[0] != '.':
                print('2')
                return False
            else:
                extensionList.append(ext.upper())
        print(extensionList)
        for ext in extensionList:
            if ext not in self.prev_extension and ext in self.extensions:
                print("3")
                return False
        return True

    def run(self):
        if self.exec_():
            category = self.ui.categoryLE.text().title()
            extensionList = self.ui.extensionTE.toPlainText().replace('\n', '').replace(' ', '').split(',')
            extensions = ", ".join([ext.upper() for ext in extensionList])
            return [category, extensions]
        self.show()
        
    def verify(self):
        if self.ui.categoryLE.text().strip() == '':
            QMessageBox.warning(self, "Alert", "Category can't be empty.")
        elif self.ui.extensionTE.toPlainText().replace('\n', '').strip() == '':
            QMessageBox.warning(self, "Alert", "Extensions can't be empty.")
        elif not self.checkExtension(self.ui.extensionTE.toPlainText().replace('\n', '').strip()):
            QMessageBox.warning(self, "Alert", "Extensions are invalid.")
        else:
            self.accept()

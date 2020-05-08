import json

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QHeaderView, QLabel, QMessageBox, QStyledItemDelegate, QTreeWidgetItem

from Interface.UI_extensionMenu import Ui_Dialog
from Structure.EditCategory import EditCategory


class ExtensionMenu(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.categoryTW.header().setSectionResizeMode(0, QHeaderView.Fixed)
        self.ui.categoryTW.header().setSectionResizeMode(1, QHeaderView.Fixed)
        self.setFixedSize(self.size())

        self.groupHead = None
        self.extensions = []
        self.stat = {}
        self.user_defined = 0
        self.extFile = 'extenstion_Category'
        self.read()

        self.ui.categoryTW.itemDoubleClicked.connect(self.modify)
        
        self.ui.addPB.clicked.connect(self.addRow)
        self.ui.removePB.clicked.connect(self.removeRow)
        self.ui.buttonBox.accepted.connect(self.write)
        self.ui.buttonBox.rejected.connect(self.reject)
    
    def addRow(self):
        editcategory = EditCategory(self, self.extensions)
        reply = editcategory.run()
        if reply != None:
            category, extensions = reply
            self.extensions += extensions.split(', ')
            treeitem = QTreeWidgetItem(self.groupHead, [category, extensions])
            treeitem.setTextAlignment(0, Qt.AlignTop|Qt.AlignLeft)

    def modify(self, item, column):
        parent = item.parent()
        if parent == None or parent.text(0) == 'Primitive':
            return None
        editcategory = EditCategory(self, self.extensions, item.text(0), item.text(1))
        previous = item.text(1).split(', ')
        reply = editcategory.run()
        if reply != None:
            category, extensions = reply
            if extensions != item.text(1):
                for p in previous:
                    self.extensions.remove(p)
                self.extensions += extensions.split(', ')
            item.setText(0, category)
            item.setText(1, extensions)
    
    def read(self):
        stat = {}
        with open(self.extFile, 'r', encoding='utf-8') as fle:
            stat = json.load(fle)
        self.stat['Primitive'] = stat['Primitive']
        self.user_defined = len(list(stat['User-defined'].keys()))
        for label, categorydict in stat.items():
            self.groupHead = QTreeWidgetItem(self.ui.categoryTW, [label])
            for category, extensionList in categorydict.items():
                self.extensions += extensionList
                treeitem = QTreeWidgetItem(self.groupHead, [category, ", ".join(extensionList)])
                treeitem.setTextAlignment(0, Qt.AlignTop|Qt.AlignLeft)
        self.ui.categoryTW.setItemDelegate(MyDelegate())
    
    def removeRow(self):
        items = self.ui.categoryTW.selectedItems()
        flag = False
        for item in items:
            parent = item.parent()
            if parent == None or parent.text(0) == 'Primitive':
                flag = True
            else:
                parent.removeChild(item)
        if flag:
            QMessageBox.warning(self, "Alert", "You can't delete primitive category.")
    
    def write(self):
        if self.groupHead.childCount() == self.user_defined:
            self.reject()
        else:
            self.stat['User-defined'] = {}
            for index in range(self.groupHead.childCount()):
                category = self.groupHead.child(index).text(0)
                extensionList = self.groupHead.child(index).text(1).split(', ')
                self.stat['User-defined'][category] = extensionList
            with open(self.extFile, 'w', encoding='utf-8') as fle:
                json.dump(self.stat, fle, ensure_ascii=False, indent=4)
            QMessageBox.information(self, "Info", "Data saved.")
            self.accept()

class MyDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        text = index.model().data(index)
        minimum_height = 30
        width = 150
        if index.column():
            width = 340
        label = QLabel(text)
        label.setWordWrap(True)
        label.setFixedWidth(width)
        label.adjustSize()
        size = super(MyDelegate, self).sizeHint(option, index)
        if label.height() > minimum_height:
            size.setHeight(label.height())
        else:
            size.setHeight(minimum_height)
        return size

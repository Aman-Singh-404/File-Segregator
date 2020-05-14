import json
import os
import shutil


class FileSegregator:
    def __init__(self, path, on_progress_callback=None):
        self._bits_remaining = self.__getSize(path)
        fle = open("extenstion_Category", 'r', encoding='utf-8')
        self.extensions = json.load(fle)
        self._on_progress_callback = on_progress_callback
        self._path = path
        self.total_size = self.__getSize(path)

    def __desegregateFolder(self):
        flag = True
        for ins_path, directories, files in os.walk(self._path):
            for file_obj in files:
                full_path = os.path.join(ins_path, file_obj)
                if self._on_progress_callback != None:
                    self._bits_remaining -= os.path.getsize(full_path)
                    self._on_progress_callback(False, full_path, self._bits_remaining)
                if flag:
                    continue
                shutil.move(full_path, self._path)
            flag = False
        for ins_path, directories, files in os.walk(self._path):
            for directory in directories:
                shutil.rmtree(os.path.join(ins_path, directory))

    def segregateFolder(self, desg=True):
        if desg:
            self.__desegregateFolder()
            self._bits_remaining = self.__getSize(self._path)
        elif not desg and self._on_progress_callback != None:
            self._bits_remaining = self.__getSize(self._path, True)
            self._on_progress_callback(True, "Folder only", self._bits_remaining)
        categoryDict = {}
        for fs_obj in os.listdir(self._path):
            full_path = os.path.join(self._path, fs_obj)
            if os.path.isfile(full_path):
                category = self.__findCategory(fs_obj)
                if categoryDict.get(category) == None:
                    categoryDict[category] = []
                categoryDict[category].append(full_path)
        for category, files in categoryDict.items():
            os.makedirs(os.path.join(self._path, category), exist_ok=True)
            destination = os.path.join(self._path, category)
            for fs_obj in files:
                if self._on_progress_callback != None:
                    self._bits_remaining -= os.path.getsize(fs_obj)
                    self._on_progress_callback(True, fs_obj, self._bits_remaining)
                shutil.move(fs_obj, os.path.join(destination, os.path.split(fs_obj)[1]))

    def __findCategory(self, fname):
        for label, categoryDict in self.extensions.items():
            for category, extensionList in categoryDict.items():
                for ext in extensionList:
                    if fname.endswith(ext.lower()):
                        return category
        return "Misc Files"

    def __getSize(self, path, onlyFiles=False):
        total_Size = 0
        for ins_path, directories, files in os.walk(path):
            total_Size += sum([os.path.getsize(os.path.join(ins_path, file_obj)) for file_obj in files])
            if onlyFiles:
                break
        return total_Size

import sys
import os

from PyQt5.QtWidgets import QApplication

from Structure.Window import Window
from utils import FileSegregator

total_size = 0

def showProgress(signal, message, bits_left):
    msg = "Wait! Process is ongoing...\nDesegregation in process\n"
    if signal:
        msg = "Wait! Process is ongoing...\nSegregation in process\n"
    print(msg + message)
    print(total_size)
    print("Progress value: " + str((total_size - bits_left) / total_size * 100) + "%\n\n")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        app = QApplication(sys.argv)
        window = Window()
        window.show()
        sys.exit(app.exec_())
    else:
        path, sig = sys.argv[1].strip(), sys.argv[2].strip()
        if path != "" and os.path.exists(path) and os.path.isdir(path):
            try:
                print("\tFile Segregator Process\n\n")
                fs = FileSegregator(path, showProgress)
                total_size = fs.total_size
                if sys.argv[2].lower()[0] == "t":
                    fs.segregateFolder(True)
                elif sys.argv[2].lower()[0] == "f":
                    fs.segregateFolder(False)
                else:
                    print("Wrong inputs.")
            except:
                print("Error Occured.")
        else:
            print("Directory doesn't exist.")

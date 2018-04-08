from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5 import uic
import sys

MainFile = "Main.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(MainFile)
AddFile = "AddSupporter.ui" 
Ui_WindowAdd,_ = uic.loadUiType(AddFile)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.btnEmailCopy.clicked.connect(self.AddSupporterWindow)
        
        for i in range(100):
            item = QtWidgets.QListWidgetItem("%d Name Address Etc"%i)
            item.setToolTip("INfo stuff for %d"%i)
            self.listWidget.addItem(item)

        self.listWidget.clicked.connect(lambda:self.Show(self.listWidget.currentRow()))

    def Show(self,num):
        print(num)
 
    def AddSupporterWindow(self):
        print("Clicked")
        self.anotherwindow = AddSupporter()
        self.anotherwindow.show()

class AddSupporter(QtWidgets.QMainWindow, Ui_WindowAdd):
    def __init__(self):
        numSupport = 8
        QtWidgets.QMainWindow.__init__(self)
        Ui_WindowAdd.__init__(self)
        self.setupUi(self)

        #close the window
        self.btnEmailCopy.clicked.connect(self.Close)
        self.scrollPeople.maximum = numSupport
        self.scrollPeople.sliderMoved.connect(self.Slide)

    def Close(self):
        self.close()

    def Slide(self):
        print(self.scrollPeople.sliderPosition())


def login():
    # input("yo")
    return True

if __name__ == "__main__":
    app = 0 # if not the core will die
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
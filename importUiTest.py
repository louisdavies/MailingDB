import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow,QApplication, QDialog
from PyQt5.uic import loadUi 

class LouisClass(QMainWindow):
	def __init__(self):
		super(LouisClass,self).__init__()
		loadUi("test.ui",self)
		self.btnEmailCopy.clicked.connect(self.on_pushButton_clicked)
	# @pyqtSlot
	def on_pushButton_clicked(self):
		print("yo yo")

app = QApplication(sys.argv)
widget = LouisClass()
widget.show()
# input("yo")
sys.exit(app._exec())
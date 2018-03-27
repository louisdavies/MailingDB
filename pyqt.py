#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial 

In this example, we create a simple
window in PyQt5.

Author: Jan Bodnar
Website: zetcode.com 
Last edited: August 2017
"""

import sys
from PyQt5.QtWidgets import QAction, QMessageBox, QToolTip, QPushButton, qApp, QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import *

import csv


class Supporter():

	Fname = ""
	SName = ""
	Email = ""
	Address = ""
	Letters = list()

	def __init__(self, FName, SName, Email=None, Address=None, Letters = [1,1,1]):
		self.FName = FName
		self.SName = SName
		self.Email = Email
		self.Address = Address
		self.Letters = Letters

def csv_reader(file_obj,person_list):
	reader = csv.reader(file_obj)
	for row in reader:
		if row[0] != "":
			print ("---".join(row))
			print (row[0])
			print (row[1])
			print (row[2])
			# print (row[3])
			# person_list.append(Supporter(row[2],row[1],row[6],row[4],[row[8],row[9],row[3]]))



class Example(QMainWindow):
	
	Supporters = list()
	
	def __init__(self):
		super().__init__()
		
		self.initUI()
		
		
	def initUI(self):
		
		QToolTip.setFont(QFont('SansSerif', 10))
		
		# self.setToolTip('This is a <b>QWidget</b> widget')
		
		btn = QPushButton('Button', self)
		btn.setToolTip('This is a <b>QPushButton</b> widget')
		btn.resize(btn.sizeHint())
		btn.move(50, 50)       
		
		qbtn = QPushButton('Quit', self)
		qbtn.setToolTip('Press to quit')
		qbtn.clicked.connect(QApplication.instance().quit)
		qbtn.resize(qbtn.sizeHint())
		qbtn.move(50, 100) 

		exitAct = QAction(QIcon("exit.png"), '&Exit', self)        
		exitAct.setShortcut('Ctrl+Q')
		exitAct.setStatusTip('Exit application')
		exitAct.triggered.connect(self.closeEvent)

		loadAct = QAction('&Load', self)        
		loadAct.setShortcut('Ctrl+L')
		loadAct.setStatusTip('Load Database')
		loadAct.triggered.connect(self.loadDatabase)

		self.statusBar()

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(loadAct)
		fileMenu.addAction(exitAct)
		

		self.statusBar().showMessage('Ready')

		self.setGeometry(300, 300, 300, 200)
		self.setWindowTitle('Tooltips')    
		self.show()

	def closeEvent(self, event):
		"""Generate 'question' dialog on clicking 'X' button in title bar.

		Reimplement the closeEvent() event handler to include a 'Question'
		dialog with options on how to proceed - Save, Close, Cancel buttons
		"""
		reply = QMessageBox.question(
			self, "Message",
			"Are you sure you want to quit? Any unsaved work will be lost.",
			QMessageBox.Save | QMessageBox.Close | QMessageBox.Cancel,
			QMessageBox.Save)

		if reply == QMessageBox.Close:
			app.quit()
		else:
			pass   

	def LoadCSV(self, file_name):
		print(file_name)
		with open(file_name, "r") as f_obj:
			csv_reader(f_obj,self.Supporters)

	def loadDatabase(self):
		DBfile = self.openFileNameDialog()
		if DBfile != None:
			try:
				if (DBfile.split('.')[1] == "csv"):
					print("Loaded Database")
			except:
					print("Couldn't Load Database")
			self.LoadCSV(DBfile)

	def openFileNameDialog(self):    
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
		if fileName:
			return fileName
		else:
			return None
 
	def saveFileDialog(self):    
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
		if fileName:
			return fileName
		else:
			return None		
		
		
if __name__ == '__main__':
	
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())
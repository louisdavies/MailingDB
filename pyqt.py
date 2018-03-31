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

import csv,os

Supporters = list()

class Supporter():

	numSupporters = 0 

	def __init__(self, first, last, email=None, address=None, letters = [1,1,1], preference = 5):
		self.first = first
		self.last = last
		if email == "":
			self.email = None
		else:
			self.email = email
		self.address = address
		self.letters = letters
		if preference == "":
			self.preference = 5
		else:
			self.preference = preference
		Supporter.numSupporters += 1

	@property
	def fullname(self):
		return "{} {}".format(self.first,self.last)

	def __str__(self):
		if (self.email == None or self.preference == 1):
			return self.fullname + " of:\n" + self.address 
		else:
			return self.fullname + " - " + self.email 

	def LoadCSV(file_name):
		print(file_name)
		with open(file_name, "r") as f_obj:
			fileContent = f_obj.read()
			info = list()
			string = ""
			result = list()
			for char in fileContent:
				if char == ';':
					result.append(Supporter(info[2],info[1],info[6],info[4],[int(info[8]),int(info[9]),int(info[10])]))
					# print(info[0])
					# print(info[1])
					info = list()
				if char == ',':
					info.append(string)
					string = ""
				else:
					string += char
			return result



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
	Supporters = Supporter.LoadCSV("startlent18.csv")
	result = [0,0,0]
	for i in range(0,Supporters[0].numSupporters-1):
		result[0] += Supporters[i].letters[0]
		result[1] += Supporters[i].letters[1]
		result[2] += Supporters[i].letters[2]
	print(result)
	# print(Supporters[300])
	# app = QApplication(sys.argv)
	# ex = Example()
	# sys.exit(app.exec_())
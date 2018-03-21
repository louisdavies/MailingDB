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

class Example(QMainWindow):
	
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

	def loadDatabase(self):
		DBfile = self.openFileNameDialog()
		if DBfile != None:
			self.LoadCSV(DBfile)
			print("Loaded Database")

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
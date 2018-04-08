#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QAction, QMessageBox, QToolTip, QPushButton, qApp, QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import *
from supporter import Supporter
from fpdf import FPDF
import os


class DBApp(QMainWindow):
	
	DBfile = ""
	
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

		saveAct = QAction('&Save', self)        
		saveAct.setShortcut('Ctrl+S')
		saveAct.setStatusTip('Save Database')
		saveAct.triggered.connect(self.saveDatabase)

		loadAct = QAction('&Load', self)        
		loadAct.setShortcut('Ctrl+L')
		loadAct.setStatusTip('Load Database')
		loadAct.triggered.connect(self.loadDatabase)

		self.statusBar()

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(loadAct)
		fileMenu.addAction(saveAct)
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

	def saveDatabase(self):
		DBnewfile = self.saveFileDialog()
		try:
			if (DBnewfile.split('.')[1] == "csv"):
				Supporter.saveCSV(DBnewfile)
				print("Saved Database")
		except:
				print("Couldn't Save Database")


	def loadDatabase(self):
		self.DBfile = self.openFileNameDialog()
		if self.DBfile != None:
			try:
				if (self.DBfile.split('.')[1] == "csv"):
					print("Loaded Database")
			except:
					print("Couldn't Load Database")
			Supporter.loadCSV(self.DBfile)

	def openFileNameDialog(self):    
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Open Database CSV File", "","CSV Files (*.csv);;All Files (*)", options=options)
		print(_)
		if fileName:
			return fileName
		else:
			return None
 
	def saveFileDialog(self):    
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self,"Save Database CSV File","","CSV Files (*.csv)", options=options)
		if fileName:
			return fileName
		else:
			return None		
		
		
if __name__ == '__main__':
	# Supporter.loadCSV("startlent18.csv")
	# Supporter.makePDF("PDF.pdf")
	# result = [0,0,0]
	# for i in range(0,Supporter.numSupporters-1):
	# 	result[0] += Supporter.Supporters[i].letters[0]
	# 	result[1] += Supporter.Supporters[i].letters[1]
	# 	result[2] += Supporter.Supporters[i].letters[2]
	# print(result)
	# Supporter.saveCSV("test3.csv")
	# Supporter.emailList()
	# print(Supporters[300])
	app = QApplication(sys.argv)
	ex = DBApp()
	sys.exit(app.exec_())
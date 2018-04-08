#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QAction, QMessageBox, QToolTip, QPushButton, qApp, QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5 import QtWidgets

from supporter import Supporter
from fpdf import FPDF
import os

MainFile = "Main.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(MainFile)
AddFile = "AddSupporter2.ui" 
Ui_WindowAdd,_ = uic.loadUiType(AddFile)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
	
	currentlyDisplayed = list()

	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		self.btnAddSupporter.clicked.connect(self.AddSupporterWindow)
		self.btnEmailCopy.clicked.connect(Supporter.emailList)
		self.btnSearch.clicked.connect(lambda:self.Search(self.searchText.text()))
		self.btnPDF.clicked.connect(self.savePDF)
		self.searchText.returnPressed.connect(lambda:self.Search(self.searchText.text()))
		self.searchList.clicked.connect(lambda:self.Show(self.searchList.currentRow()))
		
		
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
		self.DisableAll()

	def Show(self,num):
		print(num)
		self.anotherwindow = AddSupporter(self.currentlyDisplayed[num])
		self.anotherwindow.show()
		self.anotherwindow.exec_()
		self.DisplaySupporters(self.currentlyDisplayed)
	
	def savePDF(self):
		DBPDF = self.saveFileDialog(title = "Save Envelope PDF",formats=["Portable Document Format (*.pdf)"],defaultName ="SupporterEnvelopes.pdf")
		try:
			if len(DBPDF.split('.')) == 1:
				Supporter.makePDF(DBPDF+".pdf")
			elif (DBPDF.split('.')[1] == "pdf"):
				Supporter.makePDF(DBPDF)
			print("Made Envelopes")
		except:
			print("Couldn't Make Envelopes")
		
	def Search(self,text):
		result = list()
		for supporter in Supporter.Supporters:
			if str(supporter).find(text.lower()) != -1:
				result.append(supporter)
		self.DisplaySupporters(result)
 
	def AddSupporterWindow(self):
		print("Clicked")
		self.anotherwindow = AddSupporter()
		self.anotherwindow.show()

	def closeEvent(self, event):
		# reply = QMessageBox.question(
		# 	self, "Message",
		# 	"Are you sure you want to quit? Any unsaved work will be lost.",
		# 	QMessageBox.Save | QMessageBox.Close | QMessageBox.Cancel,
		# 	QMessageBox.Save)

		# if reply == QMessageBox.Close:
		app.quit()
		# else:
		# 	pass   

	def saveDatabase(self):
		DBnewfile = self.saveFileDialog(defaultName ="Supporters.csv")
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
		self.EnableAll()
		self.DisplaySupporters(Supporter.Supporters)

	def DisableAll(self):
		self.btnEmailCopy.setEnabled(False)
		self.btnPDF.setEnabled(False)
		self.btnAddSupporter.setEnabled(False)
		self.btnSearch.setEnabled(False)
		self.searchText.setEnabled(False)
		self.searchList.setEnabled(False)
		pass

	def EnableAll(self):
		self.btnEmailCopy.setEnabled(True)
		self.btnPDF.setEnabled(True)
		self.btnAddSupporter.setEnabled(True)		
		self.btnSearch.setEnabled(True)
		self.searchText.setEnabled(True)
		self.searchList.setEnabled(True)
		pass

	def DisplaySupporters(self,supList):
		self.currentlyDisplayed = supList
		self.searchList.clear()
		for i in range(len(supList)):
			if supList[i].preference in Supporter.receiveEmail:
				item = QtWidgets.QListWidgetItem("%s - %s ..."%(supList[i].fullname,supList[i].email))
			else:
				item = QtWidgets.QListWidgetItem("%s - %s ..."%(supList[i].fullname,supList[i].address.split("\n")[0]))
			item.setToolTip("Name: %s\nEmail: %s\nAddress: %s"%(supList[i].fullname,supList[i].email,supList[i].address))
			self.searchList.addItem(item)

	def openFileNameDialog(self,title="Open Database CSV File",formats=["CSV Files (*.csv)","All Files (*)"],defaultName = ""):    
		formatString = ""
		for fo in formats:
			formatString += "{};;".format(fo)
		formatString = formatString[:-2]    
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,title,defaultName,formatString, options=options)
		print(_)
		if fileName:
			return fileName
		else:
			return None
 
	def saveFileDialog(self,title="Save Database CSV File",formats=["CSV Files (*.csv)"],defaultName = ""):
		formatString = ""
		for fo in formats:
			formatString += "{};;".format(fo)
		formatString = formatString[:-2]    
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self,title,defaultName,formatString, options=options)
		if fileName:
			return fileName
		else:
			return None	

class AddSupporter(QtWidgets.QDialog, Ui_WindowAdd):
	def __init__(self, supporter=None):

		QtWidgets.QMainWindow.__init__(self)
		Ui_WindowAdd.__init__(self)
		self.setupUi(self)
		
		for item in ["Email","Post","Email and Post"]:
			self.preferenceBox.addItem(item)
		for item in ["-","UK Post","Hand Delivered","International Post"]:
			self.postBox.addItem(item)

		if supporter == None:
			self.blankSupporter()
			self.supporter = None
		else:
			self.showSupporter(supporter)
			self.supporter = supporter

		self.preferenceBox.currentIndexChanged.connect(self.preferenceBoxChanged)
		self.postBox.currentIndexChanged.connect(self.postBoxChanged)
		self.btnEmailCopy.clicked.connect(self.Close)
		self.buttonBox.accepted.connect(self.SaveChanges)
		self.buttonBox.rejected.connect(self.DiscardChanges)
		# self.scrollPeople.maximum = numSupport
		self.scrollPeople.sliderMoved.connect(self.Slide)
		self.retranslateUi(self)

	def blankSupporter(self):
		self.numP.setValue(1)
		self.numF.setValue(1)
		self.numT.setValue(1)

	def SaveChanges(self):
		if self.supporter == None: #New supporter
			newSupporter = Supporter()
			newSupporter.fullname = self.nameEdit.text()
			newSupporter.email = self.emailEdit.text()
			newSupporter.address = self.addressEdit.toPlainText()
			newSupporter.letters = [self.numT.value(),self.numP.value(),self.numF.value()]
			
			prefVal = -1
			if self.preferenceBox.currentIndex() == 0:
				prefVal = 5
			else:
				if self.postBox.currentIndex() == 1:
					prefVal = 1
				elif self.postBox.currentIndex() == 2:
					prefVal = 3
				elif self.postBox.currentIndex() == 3:
					prefVal = 2

				if self.preferenceBox.currentIndex() == 1:
					prefVal += 5

			if prefVal == -1:
				sys.exit(1)

			newSupporter.preference = prefVal
			Supporter.Supporters.append(newSupporter)

		else: #Existing supporter
			Num = self.supporter.id
			Supporter.Supporters[Num].fullname = self.nameEdit.text()
			Supporter.Supporters[Num].email = self.emailEdit.text()
			Supporter.Supporters[Num].address = self.addressEdit.toPlainText()
			Supporter.Supporters[Num].letters = [self.numT.value(),self.numP.value(),self.numF.value()]
			
			prefVal = -1
			if self.preferenceBox.currentIndex() == 0:
				prefVal = 5
			else:
				if self.postBox.currentIndex() == 1:
					prefVal = 1
				elif self.postBox.currentIndex() == 2:
					prefVal = 3
				elif self.postBox.currentIndex() == 3:
					prefVal = 2

				if self.preferenceBox.currentIndex() == 1:
					prefVal += 5

			if prefVal == -1:
				sys.exit(1)

			Supporter.Supporters[Num].preference = prefVal


	def DiscardChanges(self):
		pass

	def preferenceBoxChanged(self,i):
		if i != 0:
			self.postBox.setEnabled(True)
			print(self.postBox.currentIndex)
			if self.postBox.currentIndex() == 0:
				self.postBox.setCurrentIndex(1)
		else:
			self.postBox.setEnabled(False)
				
		# self.changePostBox(i)

	def changePostBox(self, i):
		self.postBox.setCurrentIndex(i)

	def postBoxChanged(self,i):
		if i != 0:
			print(self.postBox.currentIndex)
			if self.preferenceBox.currentIndex() == 0:
				self.ppreferenceBox.setCurrentIndex(1)

	def showSupporter(self, supporter):
		try:
			self.emailEdit.setText(supporter.email)
			self.nameEdit.setText(supporter.fullname)
			self.addressEdit.setPlainText(supporter.address)
			self.numT.setValue(supporter.letters[0])
			self.numP.setValue(supporter.letters[1])
			self.numF.setValue(supporter.letters[2])
		except:
			pass
		self.postBox.setEnabled(True)
		# print(supporter.preference)
		if supporter.preference == 5:
			self.preferenceBox.setCurrentIndex(0)
			self.postBox.setEnabled(False)
		else:
			if supporter.preference in Supporter.receiveEmail:
				self.preferenceBox.setCurrentIndex(2)
			else:
				self.preferenceBox.setCurrentIndex(1)
			
			if supporter.preference in [1,6]:
				self.postBox.setCurrentIndex(1)
			elif supporter.preference in [3,4,8,9]:
				self.postBox.setCurrentIndex(2)
			elif supporter.preference in [2,7]:
				self.postBox.setCurrentIndex(3)
		print(supporter)

	def closeEvent(self, event):
		self.Close()
		   
	def Close(self):
		# reply = QMessageBox.question(
		# 	self, "Message",
		# 	"Are you sure? Supporter changes will not be saved.",
		# 	QMessageBox.Save | QMessageBox.Close | QMessageBox.Cancel,
		# 	QMessageBox.Save)

		# if reply == QMessageBox.Close:
		self.close()
		# else:
		# 	pass

	def Slide(self):
		print(self.scrollPeople.sliderPosition())


	
if __name__ == '__main__':
	Supporter.loadCSV("startlent18.csv")
	# sys.exit(app.exec_())
	app = 0 # if not the core will die
	app = QtWidgets.QApplication(sys.argv)
	window = MainWindow()
	window.show()
	window.EnableAll()
	window.DisplaySupporters(Supporter.Supporters)
	sys.exit(app.exec_())
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QAction, QMessageBox, QToolTip, QPushButton, qApp, QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import *

from fpdf import FPDF
import os
import pyperclip

class Supporter():

	Supporters = list()
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
			self.preference = int(preference)
		Supporter.numSupporters += 1

	@property
	def fullname(self):
		return "{} {}".format(self.first,self.last)

	def __str__(self):
		if (self.email == None or self.preference == 1):
			return self.fullname + " of:\n" + self.address 
		else:
			return self.fullname + " - " + self.email 
	
	@classmethod
	def makePDF(cls,PDFName):
		pdf = FPDF('P','mm',(220,110))
		for supporter in cls.Supporters:
			print(supporter.preference)
			envelope = [1,2,3,4,6,7,8,9]
			if supporter.preference	in envelope:
				pdf.add_page()
				font_size = 20
				line_spacing = 8
				pdf.set_font('Arial', 'B', font_size)
				pdf.set_xy(20, 20)
				x_orig = pdf.get_x()
				y_orig = pdf.get_y()
				print(x_orig)
				print(y_orig)
				pdf.cell(40, 0, supporter.fullname)
				addrLines = supporter.address.split("\n")
				for i in range(0,len(addrLines)):
					print(addrLines[i])
					pdf.set_xy(x_orig, y_orig + line_spacing*(i+1))
					pdf.set_font('Arial', 'B', font_size)
					pdf.cell(40, 0, addrLines[i])
				pdf.image('logo.jpg',120,35, 60,60)
				pdf.set_font('Arial', '', 6)
				stamptext = ""
				if supporter.preference in [3,4,8,9]:
					stamptext = "Hand"
				elif supporter.preference in [1,6]:
					stamptext = "UK"
				elif supporter.preference in [2,7]:
					stamptext = "Int"
				pdf.set_xy(180, 12)
				pdf.cell(15,20,stamptext,border = 1,align = 'C')
				pdf.set_xy(180, 14)
				pdf.cell(15,20,"{}T {}P {}F".format(supporter.letters[0],supporter.letters[1],supporter.letters[2]),border = 0,align = 'C')

		pdf.output(PDFName, 'F')

	@classmethod
	def loadCSV(cls,file_name):
		print(file_name)
		with open(file_name, "r") as f_obj:
			fileContent = f_obj.read()
			info = list()
			string = ""
			result = list()
			for char in fileContent:
				if char == ';':
					result.append(Supporter(info[2],info[1],info[6],info[4],[int(info[8]),int(info[9]),int(info[10])],info[3]))
					info = list()
				if char == ',':
					info.append(string)
					string = ""
				else:
					string += char
			cls.Supporters = result

	@classmethod
	def saveCSV(cls,file_name):
		with open(file_name, "w") as f_obj:
			count = 0
			for supporter in Supporter.Supporters:
				count += 1
				csvstring = "{},{},{},{},{},".format(count,supporter.last,supporter.first,supporter.preference,supporter.address)
				csvstring += ",{},,{},{},{},;\n".format(supporter.email,supporter.letters[0],supporter.letters[1],supporter.letters[2])
				f_obj.write(csvstring)
		print("{} Saved succesfully".format(file_name))

	@classmethod
	def emailList(cls):
		emails = ""
		for supporter in cls.Supporters:
			if supporter.preference in [5,6,7,8,9]:
				emails += "{} <{}>,".format(supporter.fullname,supporter.email)
		emails = emails[:-1]
		print(emails)
		pyperclip.copy(emails)# r.update()
		return emails


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
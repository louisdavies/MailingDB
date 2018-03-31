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

from fpdf import FPDF
import os

if __name__ == '__main__':
	

	pdf = FPDF('L','mm',(150,100))
	pdf.add_page()
	pdf.set_font('Arial', 'B', 16)
	pdf.cell(40, 10, 'Hello World!')
	pdf.output('tuto1.pdf', 'F')

	# app = QApplication(sys.argv)
	# ex = Example()
	# sys.exit(app.exec_())
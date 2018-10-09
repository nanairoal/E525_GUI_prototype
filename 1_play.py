import sys
import subprocess
#from PyQt4 import QtGui, QtCore
from PyQt5.QtWidgets import (QWidget, QCheckBox, QComboBox, QLabel, QApplication, QPushButton, QGridLayout, QMessageBox, QLineEdit)
from PyQt5.QtCore import Qt


class ButtonWidget(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		global mode
		mode = QComboBox(self)
		mode.addItem("0:not calibration")
		mode.addItem("1:calibration")

		ch_label = QLabel("ch", self)
		global ch
		ch = QComboBox(self)
		for i in range(16):
			ch.addItem("%d" %i)

		global date
		date = QLineEdit()
		date_label = QLabel("date", self)

		global run_number
		run_number = QLineEdit()
		run_number_label = QLabel("Run#", self)

		Done = QPushButton("Done", self)
		Done.clicked.connect(self.DonebuttonClicked)		

		layout = QGridLayout()
		layout.addWidget(date_label, 0,0)
		layout.addWidget(date, 1,0)
		layout.addWidget(run_number_label, 2,0)
		layout.addWidget(run_number, 3,0)
		layout.addWidget(ch, 5,1)
		layout.addWidget(ch_label,5,0)
		layout.addWidget(mode, 7,0)
		layout.addWidget(Done, 7,2)

		self.setLayout(layout)
		self.setGeometry(200, 200, 300, 300)
		self.show()

	def DonebuttonClicked(self):
		subprocess.call(["sh", "hello_world.sh", date.text(), run_number.text(),str(ch.currentIndex()), str(mode.currentIndex())])
		#print(mode.currentIndex())

def main():
	app = QApplication(sys.argv)
	btn = ButtonWidget()
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()


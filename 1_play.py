import sys
import subprocess
from PyQt4 import QtGui, QtCore

class ButtonWidget(QtGui.QWidget):
	def __init__(self):
		super(ButtonWidget, self).__init__()
		self.initUI()

	def initUI(self):
		global mode
		mode = QtGui.QComboBox(self)
		mode.addItem("0:not calibration")
		mode.addItem("1:calibration")

		ch_label = QtGui.QLabel("ch", self)
		global ch
		ch = QtGui.QComboBox(self)
		for i in range(16):
			ch.addItem("%d" %i)

		global date
		date = QtGui.QLineEdit()
		date_label = QtGui.QLabel("date", self)

		global run_number
		run_number = QtGui.QLineEdit()
		run_number_label = QtGui.QLabel("Run#", self)

		Done = QtGui.QPushButton("Done", self)
		Done.clicked.connect(self.DonebuttonClicked)		

		layout = QtGui.QGridLayout()
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
	app = QtGui.QApplication(sys.argv)
	btn = ButtonWidget()
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()


import sys
from PyQt5.QtWidgets import (QWidget, QCheckBox, QComboBox, QLabel, QApplication, QPushButton, QGridLayout, QMessageBox, QLineEdit)
from PyQt5.QtCore import Qt
import subprocess
#from PyQt4.QtGui import *
#from PyQt4.QtCore import *

class ButtonBoxWidget(QWidget):
        def __init__(self):
                super().__init__()
                self.initUI()

        def initUI(self):
                """combo_daq = []
                for i in list(range(8)):
                        exec("ch%d" % i)
                        "ch%d"%i=QComboBox(self)
                        "ch%d"%i.addItem("Not_use")
                        #exec("ch%d.addItem('Ge')" % i)
                        #exec("ch%d.addItem('CsI')" % i)
                        #exec("ch%d.addItem('LqS')" % i)
                 for i in list(range(8)):
                        combo_daq[i]=QComboBox
                        combo_daq[i].addItem("Not_use")
                        combo_daq[i].addItem("Ge")
                        combo_daq[i].addItem("CsI")
                        combo_daq[i].addItem("LS")
                """
                combo_daq = QComboBox(self)
                combo_daq.addItem("kill")
                combo_daq.addItem("Ge")
                combo_daq.addItem("CsI")
                combo_daq.addItem("Ls")

                combo_beam = QComboBox(self)
                combo_beam.addItem("30 MeV")
                combo_beam.addItem("246 MeV")

                combo_RI = QComboBox(self)
                combo_RI.addItem("137Cs")
                combo_RI.addItem("60Co")
                combo_RI.addItem("22Na")
                combo_RI.addItem("252Cf")
                combo_RI.addItem("241AmBe")
                combo_RI.addItem("Background")

                event = QLabel("n")
                time = QLabel("t")	
                source = QLabel("Source")
                beam = QLabel("Beam")
                RI = QLabel("RI")
                event_edit = QLineEdit(self)
                time_edit = QLineEdit(self)

                Run = QPushButton("Run", self)
                Edit = QPushButton("Edit", self)
                Edit.clicked.connect(self.EditbuttonClicked)
                Stop = QPushButton("Stop", self)

                ch = list(range(8))
                for i in list(range(8)):
                    ch[i] = QLabel("ch%d" %i, self)

                layout = QGridLayout()
                """for i in list(range(8)):
                        layout.addWidget(ch[i], i, 0)
                """
                for i in list(range(8)):
                        layout.addWidget(ch[i],i,0)
                """layout.addWidget(ch, 0, 1)
                layout.addWidget(ch, 1, 1)
                layout.addWidget(ch, 2, 1)
                layout.addWidget(ch, 3, 1)
                layout.addWidget(ch, 4, 1)
                layout.addWidget(ch, 5, 1)
                layout.addWidget(ch, 6, 1)
                layout.addWidget(ch, 7, 1)"""

                layout.addWidget(combo_daq, 0, 1)
                layout.addWidget(combo_daq, 1, 1)
                layout.addWidget(combo_daq, 2, 1)
                layout.addWidget(combo_daq, 3, 1)
                layout.addWidget(combo_daq, 4, 1)
                layout.addWidget(combo_daq, 5, 1)
                layout.addWidget(combo_daq, 6, 1)
                layout.addWidget(combo_daq, 7, 1)
                layout.addWidget(event, 10, 0)
                layout.addWidget(event_edit, 10, 1)
                layout.addWidget(time, 11, 0)
                layout.addWidget(time_edit, 11 ,1)
                layout.addWidget(source, 12, 0)	
                layout.addWidget(beam, 13, 0)
                layout.addWidget(RI, 13, 1)
                layout.addWidget(combo_beam, 14, 0)	
                layout.addWidget(combo_RI, 14, 1)
                layout.addWidget(Run, 15, 4)
                layout.addWidget(Edit, 15, 2)
                layout.addWidget(Stop, 15, 0)
                self.setLayout(layout)

                self.setGeometry(100, 200, 300, 400)
                self.show()

        def EditbuttonClicked(self):
                subprocess.call(["sh", "edit.sh"])

        #def StopbuttonClicked(self):
                #

        #def RunbuttonClicked(self):
                #subprocess.call([])

        def start_timer(self):
                if self.count > 0:
                        self.timer.start()

        def stop_timer(self):
                self.timer.stop()

        def closeEvent(self, event):
                reply = QMessageBox.question(self, "Message", "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    event.accept()
                else:
                    event.ignore()

def main():
        app = QApplication(sys.argv)
        #left = QtGui.QFrame(self)
        #left.setFrameShape(QtGui.QFrame.StyledPanel)

        #right = QtGui.QFrame(self)
        #right.setFrameShape(QtGui.QFrame.StyledPanel)

        #splitter = QtGui.QSplitter(self)
        #splitter.addWidget(left)
        #splitter.addWidget(right)

        #hbox.addWidget(splitter)
        #hbox.addWidget(combo)
        #self.setLayout(hbox)

        #self.setGeometry(300, 300, 700 ,500)
        #self.setWindowTitle("test")
        #self.show()
        btn = ButtonBoxWidget()
        #ButtonBoxWidget.Run.clicked.connect(Running)
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()

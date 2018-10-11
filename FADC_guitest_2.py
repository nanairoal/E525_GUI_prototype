import sys
from PyQt5.QtWidgets import (QWidget, QCheckBox, QComboBox, QLabel, QApplication, QPushButton, QGridLayout, QMessageBox, QLineEdit, QDialog)
from PyQt5.QtCore import Qt
from datetime import datetime
import subprocess
#from PyQt4.QtGui import *
#from PyQt4.QtCore import *

class ButtonBoxWidget(QWidget):
        def __init__(self):
                super().__init__()
                self.initUI_set()

        def initUI_set(self):
                global det0, det1, det2, det3, det4, det5, det6, det7, combo_mode
                det0 = QComboBox(self)
                det1 = QComboBox(self)
                det2 = QComboBox(self)
                det3 = QComboBox(self)
                det4 = QComboBox(self)
                det5 = QComboBox(self)
                det6 = QComboBox(self)
                det7 = QComboBox(self)
                combo_mode = QComboBox(self)
                combo_mode.addItem("test")
                combo_mode.addItem("physics")
                combo_mode.addItem("calibration")
                combo_mode.currentIndexChanged.connect(self.ChangeMode)

                global combo_detector
                combo_detector = [det0, det1, det2, det3, det4, det5, det6, det7]
                for i in combo_detector:
                        i.addItem("kill")
                        i.addItem("Ge")
                        i.addItem("CsI")
                        i.addItem("LqS")
                        i.setEnabled(False)

                global combo_beam
                combo_beam = QComboBox(self)
                combo_beam.addItem("None")
                combo_beam.addItem("30 MeV")
                combo_beam.addItem("246 MeV")
                combo_beam.setEnabled(False)

                global combo_RI
                combo_RI = QComboBox(self)
                combo_RI.addItem("None")
                combo_RI.addItem("137Cs")
                combo_RI.addItem("60Co")
                combo_RI.addItem("22Na")
                combo_RI.addItem("252Cf")
                combo_RI.addItem("241AmBe")
                combo_RI.addItem("Background")
                combo_RI.setEnabled(False)

                mode = QLabel("Run mode")
                beam = QLabel("Beam")
                RI = QLabel("RI")

                run = QPushButton("Run", self)
                run.setStyleSheet("background-color: rgb(134,218,255)")
                run.clicked.connect(self.RunbuttonClicked)
                edit = QPushButton("Edit", self)
                edit.clicked.connect(self.EditbuttonClicked)
                stop = QPushButton("Stop", self)

                box0 = QCheckBox("ch0", self)
                box0.stateChanged.connect(self.ChangeState0)
                box1 = QCheckBox("ch1", self)
                box1.stateChanged.connect(self.ChangeState1)
                box2 = QCheckBox("ch2", self)
                box2.stateChanged.connect(self.ChangeState2)
                box3 = QCheckBox("ch3", self)
                box3.stateChanged.connect(self.ChangeState3)
                box4 = QCheckBox("ch4", self) 
                box4.stateChanged.connect(self.ChangeState4)
                box5 = QCheckBox("ch5", self)
                box5.stateChanged.connect(self.ChangeState5)
                box6 = QCheckBox("ch6", self)
                box6.stateChanged.connect(self.ChangeState6)
                box7 = QCheckBox("ch7", self)
                box7.stateChanged.connect(self.ChangeState7)
                check_box = [box0, box1, box2, box3, box4, box5, box6, box7]
               
                global layout
                layout = QGridLayout()
                for i in list(range(8)):
                        layout.addWidget(check_box[i], i, 0)
                for i in list(range(8)):
                        layout.addWidget(combo_detector[i], i, 1)
                layout.addWidget(mode, 10, 0)
                layout.addWidget(combo_mode, 11, 0)
                layout.addWidget(beam, 12, 0)
                layout.addWidget(RI, 12, 1)
                layout.addWidget(combo_beam, 13, 0)	
                layout.addWidget(combo_RI, 13, 1)
                layout.addWidget(run, 14, 4)
                layout.addWidget(edit, 14, 2)
                layout.addWidget(stop, 14, 0)
                self.setLayout(layout)
                self.setGeometry(100, 100, 400, 500)
                self.show()

        def ChangeState0(self, state):
                if state == Qt.Checked:
                        combo_detector[0].setEnabled(True)
                else:
                        combo_detector[0].setCurrentIndex(0)
                        combo_detector[0].setEnabled(False)

        def ChangeState1(self, state):
                if state == Qt.Checked:
                        combo_detector[1].setEnabled(True)
                else:
                        combo_detector[1].setCurrentIndex(0)
                        combo_detector[1].setEnabled(False)

        def ChangeState2(self, state):
                if state == Qt.Checked:
                        combo_detector[2].setEnabled(True)
                else:
                        combo_detector[2].setCurrentIndex(0)
                        combo_detector[2].setEnabled(False)

        def ChangeState3(self, state):
                if state == Qt.Checked:
                        combo_detector[3].setEnabled(True)
                else:
                        combo_detector[3].setCurrentIndex(0)
                        combo_detector[3].setEnabled(False)

        def ChangeState4(self, state):
                if state == Qt.Checked:
                        combo_detector[4].setEnabled(True)
                else:
                        combo_detector[4].setCurrentIndex(0)
                        combo_detector[4].setEnabled(False)

        def ChangeState5(self, state):
                if state == Qt.Checked:
                        combo_detector[5].setEnabled(True)
                else:
                        combo_detector[5].setCurrentIndex(0)
                        combo_detector[5].setEnabled(False)

        def ChangeState6(self, state):
                if state == Qt.Checked:
                        combo_detector[6].setEnabled(True)
                else:
                        combo_detector[6].setCurrentIndex(0)
                        combo_detector[6].setEnabled(False)

        def ChangeState7(self, state):
                if state == Qt.Checked:
                        combo_detector[7].setEnabled(True)
                else:
                        combo_detector[7].setCurrentIndex(0)
                        combo_detector[7].setEnabled(False)

        def ChangeMode(self, state):
                if state == 0:
                        combo_beam.setCurrentIndex(0)
                        combo_beam.setEnabled(False)
                        combo_RI.setCurrentIndex(0)
                        combo_RI.setEnabled(False)
                elif state == 1:
                        combo_beam.setEnabled(True)
                        combo_RI.setCurrentIndex(0)
                        combo_RI.setEnabled(False)
                else:
                        combo_beam.setCurrentIndex(0)
                        combo_beam.setEnabled(False)
                        combo_RI.setEnabled(True)

        def EditbuttonClicked(self):
                subprocess.call(["sh", "edit.sh"])

        #def StopbuttonClicked(self):
                #

        def RunbuttonClicked(self):
                subprocess.call(["sh", "check.sh", file_name_edit.text(), str(combo_detector[0].currentIndex()), str(combo_beam.currentIndex()) ,str(combo_RI.currentIndex())])
                subwindow = InformationWindow()
                subwindow.show()

        def closeEvent(self, event):
                reply = QMessageBox.question(self, "Message", "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    event.accept()
                else:
                    event.ignore()



class InformationWindow(QWidget):
        def __init__(self):
                super().__init__()
                self.initUI_info()
 
        def initUI_info(self, parent=None):
                self.w = QDialog(parent)
                label_info = QLabel("Run information")
                information = QLabel("hogehoge")
                start_time_label = QLabel("Acquisition start")
                #start_time = QLabel(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
                #current_time
                #measurement_time
                get_events = QPushButton("Current events", self)
                get_events.clicked.connect(self.GetCurrentEvents)
                lines = QLabel()
                plot = QPushButton("Plot", self)
                acquisition_start = QPushButton("Acquisition start", self)
                quit = QPushButton("Quit", self)

                layout = QGridLayout()
                layout.addWidget(label_info, 0, 0)
                layout.addWidget(information, 1, 0)
                layout.addWidget(start_time_label, 2, 0)
                layout.addWidget(get_events, 3, 0)
                layout.addWidget(lines, 3, 1)
                layout.addWidget(plot, 4, 0)
                layout.addWidget(acquisition_start, 5, 0)
                layout.addWidget(quit, 6, 0)
                self.w.setLayout(layout)
                self.setGeometry(200, 200, 300, 400)

        def show(self):
                self.w.exec_()


        def GetCurrentEvents(self):
                lines = subprocess.call(["wc", "-l", "wave0.txt"])
                self.SendEvents(lines)

        def SendEvents(self, lines):
                self.lines = lines

def main():
        app = QApplication(sys.argv)
        btn = ButtonBoxWidget()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()

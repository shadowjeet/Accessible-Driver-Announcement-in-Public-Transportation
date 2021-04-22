import sys
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.uic import loadUi
import new_thread_file
import re


class recording_Ui(QtWidgets.QMainWindow):


    def __init__(self, parent=None):
        super(recording_Ui, self).__init__(parent)
        uic.loadUi('interface/recording_view.ui', self)

        self.screen_size = QtWidgets.QDesktopWidget().screenGeometry()
        self.full_screen = False
        self.start_announcement = False
        self.transcription = ""
        self.threadclass = new_thread_file.ThreadClass()
        self.threadclass.lan_code = ""

        self.record_button.clicked.connect(self.startThread)
        self.label.setText("<font color='white'>Announcement:</font>")
        self.label.setStyleSheet("background-color: grey")

        self.set_english()
        self.en_us_btn.clicked.connect(self.set_english)
        self.nb_no_btn.clicked.connect(self.set_norwegian)
        self.full_screen_btn.clicked.connect(self.set_full_screen)

        self.time = ""
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def startThread(self):
        print(self.start_announcement)
        if self.start_announcement:
            self.set_notspeaking_icon()
            self.start_announcement=False
            self.threadclass.terminate()
            print("Final text:" + self.transcription)
            transcription_file = open("transcription_logs/transcription.txt", "a+")
            transcription_file.write("\n"+self.time +"||--||"+self.transcription)
            print("Thread terminated")

        else:
            self.set_speaking_icon()
            self.threadclass.tick.connect(self.updateAnnouncementBoard)
            self.threadclass.start()
            self.start_announcement = True

    def update_time(self):
        self.time = QtCore.QTime.currentTime().toString()
        self.current_time.setText(self.time)

    def updateAnnouncementBoard(self, value):
        self.transcription = value
        self.message_label.setText("<font color='yellow'>Attention Passengers: "+str(self.transcription)+".</font>")
        self.message_label.setStyleSheet("background-color: black")

        if re.search(r'\b(emergency)\b', self.transcription, re.I):
            self.info_icon.setPixmap(QtGui.QPixmap("interface/images/warning_icon.jpg"))
            #print(self.transcription+"==>Emergency..")
        elif re.search(r'\b(delay)\b', self.transcription, re.I):
            self.info_icon.setPixmap(QtGui.QPixmap("interface/images/info_icon.png"))
            #print(self.transcription+"==>Delay...")

    def set_speaking_icon(self):
        mic_on_icon = QtGui.QIcon()
        mic_on_icon.addPixmap(QtGui.QPixmap("interface/images/mic_on_small.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.record_button.setIcon(mic_on_icon)
        self.label.setText("<font color='white'>Broadcasting...</font>")
        self.label.setStyleSheet("background-color: green")


    def set_notspeaking_icon(self):
        mic_on_icon = QtGui.QIcon()
        mic_on_icon.addPixmap(QtGui.QPixmap("interface/images/mic_off_small.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.record_button.setIcon(mic_on_icon)
        self.label.setText("<font color='white'>Announcement:</font>")
        self.label.setStyleSheet("background-color: grey")




    def close_function(self):
        pass

    def set_full_screen(self):
        window_width, window_height = 1020, 600
        x_axis = (self.screen_size.width()/2) - (window_width/2)
        y_axis = (self.screen_size.height()/2) - (window_height/2)

        if self.full_screen:
            self.setGeometry(x_axis, y_axis, window_width, window_height)
            print(str(self.screen_size))
            self.full_screen = False
        else:
            self.setGeometry(0, 0, self.screen_size.width(), self.screen_size.height())
            self.full_screen = True
        pass

    """
    def set_language(self):
        if self.en_us_btn.setDisabled(True):
            self.threadclass.lan_code = "en-US"
            self.nb_no_btn.setDisabled(False)
            print("En")
            
        elif self.nb_no_btn.setDisabled(True):
            self.threadclass.lan_code = "nb-NO"
            
            print("Nr")"""

    def set_english(self):
        self.threadclass.lan_code = "en-US"
        self.en_us_btn.setDisabled(True)
        self.nb_no_btn.setDisabled(False)
        print(self.threadclass.lan_code)

    def set_norwegian(self):
        self.threadclass.lan_code = "nb-NO"
        self.nb_no_btn.setDisabled(True)
        self.en_us_btn.setDisabled(False)
        print(self.threadclass.lan_code)

app = QtWidgets.QApplication(sys.argv)
widget = recording_Ui()
widget.show()
sys.exit(app.exec_())
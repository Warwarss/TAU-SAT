import sys
import time

import serial
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import csv

class Worker1(QThread):
    def __init__(self, telemetri, thread, harita):
        super(Worker1,self).__init__()
        self.Telemetri = telemetri
        self.Thread = thread
        self.Harita = harita
    def Telemetri_Update(self,display):
        if self.Telemetri.Telemetri.rowCount() < 100:
            self.Telemetri.Telemetri.insertRow(0)
        else:
            self.Telemetri.Telemetri.removeRow(100)
            self.Telemetri.Telemetri.insertRow(0)
        i = 0
        for x in range(len(display)):
            item = QTableWidgetItem()
            self.Telemetri.Telemetri.setItem(0, x, item)
            item.setText(display[x])
        self.Harita.longtitude = float(display[11])
        self.Harita.latitude = float(display[12])
        self.Harita.SetupUi()
        print(self.Harita.latitude)
        # self.Harita.SetupUi()
    # def GPS_Update(self,gps_data):
    #     self.Harita.longtitude = gps_data[]

    def run(self):
        self.Thread.Telemetri_Update.connect(self.Telemetri_Update)
        # self.Thread.GPS_Update.connect(self.GPS_Update)

    def stop(self):
        self.quit()
        self.exit()

class Worker2(QThread):
    def __init__(self, port, baudrate):
        super(Worker2,self).__init__()
        self.port = port
        self.baudrate = baudrate
    Telemetri_Update=pyqtSignal(list)
    Graph_Update=pyqtSignal(float)
    Model_Update=pyqtSignal(list)
    Status_Signal = pyqtSignal(bool)
    Gps_Update =pyqtSignal(list)
    def stop(self):
        self.ThreadActive = False
        self.ser.close()
        self.quit()
        self.exit()
    def run(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate)
            self.ThreadActive = True
            self.Status_Signal.emit(self.ThreadActive)
        except serial.serialutil.SerialException:
            self.ThreadActive = False
            self.Status_Signal.emit(self.ThreadActive)
            self.quit()
            self.exit()
        while self.ThreadActive:
            print(f"Pulling Data From;\nPort: {self.port}\nBaudrate: {self.baudrate}")
            display=str(self.ser.read_until())
            for x in escapes:
                display=display.replace(x ,"")
            display=display.split("_")
            print(display)
            with open('Telemetri_Verisi.csv', 'a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=',')
                csv_writer.writerow([display])
            print(len(display))
            if len(display) == 23:
                self.Telemetri_Update.emit(display)
                #self.Graph_Update.emit(display)
                angles = [display[19], display[20], display[21]]
                self.Model_Update.emit(angles)
            time.sleep(1)
        self.Status_Signal.emit(self.ThreadActive)

class Worker3(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(1)
        Capture.open(0, cv2.CAP_DSHOW)
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                print("Camera is working")
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(480, 360, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
    def stop(self):
        self.ThreadActive = False
        self.quit()

escapes = [r"\n", "b'", "r'", "\\"]

if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())
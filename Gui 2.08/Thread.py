import sys
import time

import serial
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import csv

class Worker1(QThread):
    def __init__(self, telemetri, thread, harita, gps1_lat, gps1_long, gps1_alt, gps2_lat, gps2_long, gps2_alt):
        super(Worker1,self).__init__()
        self.Telemetri = telemetri
        self.Thread = thread
        self.Harita = harita
        self.gps1_lat = gps1_lat
        self.gps1_long = gps1_long
        self.gps1_alt = gps1_alt
        self.gps2_lat = gps2_lat
        self.gps2_long = gps2_long
        self.gps2_alt = gps2_alt
    def Ui_Update(self,display):
        if self.Telemetri.Telemetri.rowCount() < 100:
            self.Telemetri.Telemetri.insertRow(0)
        else:
            self.Telemetri.Telemetri.removeRow(100)
            self.Telemetri.Telemetri.insertRow(0)
        for x in range(len(display)):
            item = QTableWidgetItem()
            self.Telemetri.Telemetri.setItem(0, x, item)
            item.setText(display[x])
        if self.i == 10:
            self.Harita.longtitude = float(display[11])
            self.Harita.latitude = float(display[12])
            self.Harita.SetupUi()
            self.i = 0
        else:
            self.i = self.i + 1
        self.gps1_lat.setText(display[11])
        self.gps1_long.setText(display[12])
        self.gps1_alt.setText(display[13])
        self.gps2_lat.setText(display[14])
        self.gps2_long.setText(display[15])
        self.gps2_alt.setText(display[16])

        # self.Harita.add_marker(display[11], display[12])

    def run(self):
        self.Thread.Telemetri_Update.connect(self.Ui_Update)
        # self.Thread.Graph_Update.connect(self.Graph_Update)
        self.i = 0
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
    Graph_Update=pyqtSignal(list)
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
                self.Graph_Update.emit([display[3],display[5],display[7],display[8],display[9]])
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

class Worker4(QThread):
    def __init__(self, thread, temp, alti, alti_diff, pressure, velocity):
        super(Worker4, self).__init__()
        self.Thread = thread

        self.temp_x = []
        self.temp_y = []
        self.alti_x = []
        self.alti_y = []
        self.alti_diff_x = []
        self.alti_diff_y = []
        self.pressure_x = []
        self.pressure_y = []
        self.velocity_x = []
        self.velocity_y = []
        self.temp_data_line = temp
        self.alti_data_line = alti
        self.alti_diff_data_line = alti_diff
        self.pressure_data_line = pressure
        self.velocity_data_line = velocity

    def Graph_Update(self, Data):
        try:
            self.temp_x.append(self.temp_x[-1] + 1)
            self.alti_x.append(self.alti_x[-1] + 1)
            self.alti_diff_x.append(self.alti_diff_x[-1] + 1)
            self.pressure_x.append(self.pressure_x[-1] + 1)
            self.velocity_x.append(self.velocity_x[-1] + 1)
        except:
            self.temp_x.append(1)
            self.alti_x.append(1)
            self.alti_diff_x.append(1)
            self.pressure_x.append(1)
            self.velocity_x.append(1)
        self.temp_y.append(float(Data[4]))
        self.alti_y.append(float(Data[1]))
        self.alti_diff_y.append(float(Data[2]))
        self.pressure_y.append(float(Data[0]))
        self.velocity_y.append(float(Data[3]))
        self.temp_data_line.setData(self.temp_x, self.temp_y)
        self.alti_data_line.setData(self.alti_x, self.alti_y)
        self.alti_diff_data_line.setData(self.alti_diff_x, self.alti_diff_y)
        self.pressure_data_line.setData(self.pressure_x, self.pressure_y)
        self.velocity_data_line.setData(self.velocity_x, self.velocity_y)
    def run(self):
        self.Thread.Graph_Update.connect(self.Graph_Update)
    def stop(self):
        self.quit()
        self.exit()

escapes = [r"\n", "b'", "r'", "\\"]

if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())
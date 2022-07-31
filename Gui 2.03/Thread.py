import sys
import serial
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#import cv2
import csv

class Worker1(QThread):
    def __init__(self,telemetri,thread):
        super(Worker1,self).__init__()
        self.Telemetri = telemetri
        self.Thread = thread
    def Telemetri_Update(self,display):
        self.Telemetri.Telemetri.insertRow(0)
        i = 0
        for x in range(len(display)):
            item = QTableWidgetItem()
            self.Telemetri.Telemetri.setItem(0, x, item)
            item.setText(display[x])
    def run(self):

    def stop(self):
        self.ThreadActive = False
        self.quit()

class Worker2(QThread):
    def __init__(self, port, baudrate):
        super(Worker2,self).__init__()
        self.port = port
        self.baudrate = baudrate
    Telemetri_Update=pyqtSignal(list)
    Graph_Update=pyqtSignal(float)
    Model_Update=pyqtSignal(list)
    Status_Signal = pyqtSignal(bool)
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
            print(f"Worker 2 is working\nPort: {self.port}\nBaudrate: {self.baudrate}")
            display=str(self.ser.read_until())
            for x in escapes:
                display=display.replace(x ,"")
            display=display.split("_")
            print(display)
            with open('Telemetri_Verisi.csv', 'a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=',')
                csv_writer.writerow([display])
            self.Telemetri_Update.emit(display)
            #self.Graph_Update.emit(display)
            #self.Model_Update.emit(display)
        self.Status_Signal.emit(self.ThreadActive)

escapes = [r"\n", "b'", "r'", "\\"]

if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())
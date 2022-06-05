import sys
import serial
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import csv

class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            print("Worker 1 is working")
            ret, frame = Capture.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(320, 240, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
    def stop(self):
        self.ThreadActive = False
        self.quit()

class Worker2(QThread):
    Telemetri_Update=pyqtSignal(list)
    Graph_Update=pyqtSignal(float)
    Model_Update=pyqtSignal(list)
    def run(self):
        self.ThreadActive = True
        ser = serial.Serial("COM5", "19200")
        while self.ThreadActive:
            print("Worker 2 is working")
            display=str(ser.read_until())
            for x in escapes:
                display=display.replace(x ,"")
            display=display.split("_")
            print(display)
            with open('Telemetri_Verisi.csv', 'a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=',')
                csv_writer.writerow([display])
            #self.Telemetri_Update.emit(display)
            #self.Graph_Update.emit(display)
            self.Model_Update.emit(display)

escapes = [r"\n", "b'", "r'", "\\"]

if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())
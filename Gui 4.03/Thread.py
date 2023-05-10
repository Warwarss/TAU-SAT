import sys
import time
import datetime
import paramiko
from scp import SCPClient
import serial
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import csv
import math

class Worker1(QObject):
    def __init__(self, telemetri, thread, harita):
        super(Worker1,self).__init__()
        self.Telemetri = telemetri
        self.Thread = thread
        self.Harita = harita
        # self.Thread.Telemetri_Update.connect(self.Ui_Update)
        self.Thread.Status_Signal.connect(self.Status_Update)

    def Ui_Update(self,display):
        pass
        # if self.Telemetri.rowCount() < 100:
        #     self.Telemetri.insertRow(0)
        # else:
        #     self.Telemetri.removeRow(100)
        #     self.Telemetri.insertRow(0)
        # for x in range(len(display)):
        #     item = QTableWidgetItem()
        #     self.Telemetri.setItem(0, x, item)
        #     item.setText(display[x])
        # if self.i == 10:
        #     try:
        #         self.Harita.latitude = float(display[12])
        #         self.Harita.longtitude = float(display[13])
        #         # self.Harita.longtitude2 = float(display[15])
        #         # self.Harita.latitude2 = float(display[14])
        #     except ValueError:
        #         pass
        #     self.Harita.SetupUi()
        #     self.i = 0
        # else:
        #     self.i = self.i + 1

        # self.Harita.add_marker(display[11], display[12])
    def Status_Update(self, Thread_Status):
        self.ThreadActive = Thread_Status
        print(f"Deneme: {self.ThreadActive}")
    def run(self):
        # self.Thread.Graph_Update.connect(self.Graph_Update)
        self.i = 0
        # self.Thread.GPS_Update.connect(self.GPS_Update)

    def stop(self):
        self.quit()
        self.exit()

class Worker2(QObject):
    def __init__(self, port, baudrate):
        super(Worker2,self).__init__()
        self.port = port
        self.packet = 1
        self.baudrate = baudrate
        self.PowerReset = False
        self.prev_packet = 0
    displayTelemetri = []
    time = datetime.datetime.now()
    time = time.strftime("%d-%b-%Y(%H.%M.%S)")
    filename = "Telemetri_Verisi" + "_" + time + ".csv"
    headerList = ["PAKET NUMARASI", "UYDU STATUSU", "HATA KODU", "GONDERME SAATI", "BASINC1", "BASINC2", "YUKSEKLIK1",
              "YUKSEKLIK2", "IRTIFA FARKI", "INIS HIZI", "SICAKLIK", "PIL GERILIMI", "GPS1 LATITUDE", "GPS1 LONGITUDE",
              "GPS1 ALTITUDE", "PITCH", "ROLL", "YAW", "TAKIM NO"]
    with open(filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')
        csv_writer.writerow(headerList)

    Telemetri_Update=pyqtSignal(list)
    Received = pyqtSignal()
    Alarm_Update = pyqtSignal(str)
    Graph_Update=pyqtSignal(list)
    Model_Update=pyqtSignal(list)
    State_Update=pyqtSignal(list)
    BatteryVoltage_Update = pyqtSignal(list)
    Status_Signal=pyqtSignal(bool)
    Gps_Update =pyqtSignal(list)
    def stop(self):
        self.ThreadActive = False
        self.Status_Signal.emit(self.ThreadActive)
        try:
            self.ser.close()
            print("Port kapandı")
        except:
            print("Port kapanmadı")

    def run(self):
        print("Runningxxx")
        try:
            self.ser = serial.Serial(self.port, self.baudrate)
            self.ThreadActive = True
            self.Status_Signal.emit(self.ThreadActive)
            print("Bağlandım")
        except serial.serialutil.SerialException:
            print("Bağlanamadım")
            self.ThreadActive = False
            self.Status_Signal.emit(self.ThreadActive)
            self.stop()
        if self.ThreadActive is False:
            self.stop()

        while self.ThreadActive:
            print("Running")
            print("İkinci versiyon Thread")
            print(f"Pulling Data From;\nPort: {self.port}\nBaudrate: {self.baudrate}")
            display=str(self.ser.read_until())
            self.Received.emit()
            for x in escapes:
                display=display.replace(x ,"")
            # displayTelemetri = display.replace(".", ",")
            # displayTelemetri = displayTelemetri.split("*")
            display = display.split("*")
            print(display)
            display.pop()
            for x in display:
                self.displayTelemetri.append(x.replace(".",","))
            print(f"İkinci döngü : {self.ThreadActive}")
            if len(display) == 19:
                pass
                # if self.PowerReset is False:
                #     self.packet = int(display[1])
                # if self.packet <  self.prev_packet:
                #     self.PowerReset = True
                #     display[1] =  str(self.prev_packet + 1)
                #     self.packet =  self.prev_packet
                # if self.PowerReset:
                #     self.packet = self.packet + 1
                #     display[1] = str(self.packet)
            try:
                with open(self.filename, 'a', newline='') as csv_file:
                    pass
                    csv_writer = csv.writer(csv_file, delimiter=';')
                    csv_writer.writerow(self.displayTelemetri)
                    self.displayTelemetri = []
            except PermissionError:
                print("PermissionError")
            # if True:
            #     self.Telemetri_Update.emit(display)
            if len(display) == 19:
                self.Telemetri_Update.emit(display)
                self.Graph_Update.emit([display[4],display[6],display[8],display[9],display[10]])
                angles = [display[15], display[16], display[17]]
                status = [display[1]]
                voltage = [display[11]]
                # hata_kodu = [display[2][0],display[2][1], display[2][2], display[2][3], display[2][4]]
                hata_kodu = display[2]
                self.BatteryVoltage_Update.emit(voltage)
                self.Alarm_Update.emit(hata_kodu)
                self.Model_Update.emit(angles)
                self.State_Update.emit(status)
            self.prev_packet = self.packet
            self.Status_Signal.emit(self.ThreadActive)
            time.sleep(1)
        self.Status_Signal.emit(self.ThreadActive)
        self.stop()

class Worker3(QThread):
    ImageUpdate = pyqtSignal(QImage)
    time = datetime.datetime.now()
    time = time.strftime("%d-%b-%Y(%H.%M.%S)")
    filename = "Video" + "_" + time + ".avi"
    def run(self):
        self.Record = False
        self.ThreadActive = True
        self.Writer = False
        Capture = cv2.VideoCapture(-1, cv2.CAP_DSHOW)
        Capture.open(0, cv2.CAP_DSHOW)
        frame_width = int(Capture.get(3))
        frame_height = int(Capture.get(4))
        size = (frame_width, frame_height)
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                if self.Writer is False and self.Record is True:
                    result = cv2.VideoWriter(self.filename, cv2.VideoWriter_fourcc(*'XVID'), 30.0, size)
                    self.Writer = True
                if self.Record is True:
                    result.write(frame)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(480, 360, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
        self.stop()
    def stop(self):
        self.ThreadActive = False
        self.quit()

class Worker4(QObject):
    def __init__(self, thread, temp, alti, alti_diff, pressure, velocity, batarya, batarya_progress):
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
        self.batarya = batarya
        self.batarya_progress = batarya_progress

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
        self.pressure_y.append(float(Data[0]))
        self.alti_y.append(float(Data[1]))
        self.alti_diff_y.append(float(Data[2]))
        self.velocity_y.append(float(Data[3]))
        self.temp_y.append(float(Data[4]))
        if len(self.pressure_y) >= 150:
            self.pressure_y.pop(0)
            self.alti_y.pop(0)
            self.alti_diff_y.pop(0)
            self.velocity_y.pop(0)
            self.temp_y.pop(0)
            self.temp_x.pop(0)
            self.alti_x.pop(0)
            self.alti_diff_x.pop(0)
            self.pressure_x.pop(0)
            self.velocity_x.pop(0)

        self.temp_data_line.setData(self.temp_x, self.temp_y)
        time.sleep(0.1)
        self.alti_data_line.setData(self.alti_x, self.alti_y)
        time.sleep(0.1)
        self.alti_diff_data_line.setData(self.alti_diff_x, self.alti_diff_y)
        time.sleep(0.1)
        self.pressure_data_line.setData(self.pressure_x, self.pressure_y)
        time.sleep(0.1)
        self.velocity_data_line.setData(self.velocity_x, self.velocity_y)
    def BatteryVoltage_Update(self, batarya_gerilimi):
        batarya_val = float(batarya_gerilimi[0])
        batarya_percentage = batarya_val - 2.7
        batarya_percentage = batarya_percentage * 66.666
        batarya_percentage = int(batarya_percentage)
        self.voltage.emit(batarya_percentage)
        # self.batarya_progress.setProperty("value", batarya_percentage)
        # batarya_percentage = str(batarya_percentage)
        # self.batarya.setText("%"+ batarya_percentage)
    voltage = pyqtSignal(int)
    def run(self):
        self.Thread.Graph_Update.connect(self.Graph_Update)
        self.Thread.BatteryVoltage_Update.connect(self.BatteryVoltage_Update)
    def stop(self):
        pass

class Worker5(QThread):
    def __init__(self, Model, angles):
        super(Worker5,self).__init__()
        self.Model = Model
        self.pitch = float(angles[0])
        self.roll = float(angles[1])
    def stop(self):
        self.quit()
        self.exit()
    def run(self):
        dz0 = math.cos(math.radians(self.pitch))
        dz = 4 * dz0
        print(dz)
        dy0 = math.sin(math.radians(self.pitch))
        dy = 4 * dy0
        if self.pitch < 0 :
            dy0 = dy0 * -1
            dy = dy * -1
        print(dy)
        dx0 = math.sin(math.radians(self.roll))
        dx = 4 * dx0
        if self.roll < 0 :
            dx0 = dx0 * -1
            dx = dx * -1
        print(dx)
        dz1 = math.cos(math.radians(self.roll))
        dz = 4 * dz1
        print(dz)
        for i in range(1000):
            self.Model.mesh_tasiyici.translate(dx=dx, dy=-dy, dz=dz)
            dz = dz + dz0
            dy = dy + dy0
            dx = dx + dx0
            time.sleep(0.01)
        self.stop

class Worker6(QObject):
    def stop(self):
        print("IP Thread is stopped")

    def __init__(self, ip, filename):
        super(Worker6, self).__init__()
        self.ip = ip
        self.filename = filename
        self.Connection = False
        self.retries = 0
        self.maximum_retries = 10
        # self.port2 = port2
        # self.baudrate = baudrate
        # self.Port = True
    finished = pyqtSignal()
    timeout = pyqtSignal()
    # def split_string(self, s, chunk_size):
    #     return [s[i:i + chunk_size] for i in range(0, len(s), chunk_size)]

    def Dosya_Gonder_fonk(self):
        # try:
        #     self.ser = serial.Serial(self.port2, 230400)
        #     self.Port = True
        # except serial.serialutil.SerialException:
        #     print("Bağlanamadım")
        #     self.stop()
        # with open(self.filename, "rb") as file:
        #     my_string = base64.b64encode(file.read())
        #     print(my_string)
        # packet_amount = int(len(my_string)/32+1)
        # Packet_list = self.split_string(my_string,29)
        # i = 0
        # for packet in Packet_list:
        #     self.ser.write(Packet_list[i] + b"*")
        #     i = i + 1

        # sent_packet = 0

        def createSSHClient(server, port, user, password):
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            while (self.retries < self.maximum_retries):
                try:
                    client.connect(server, port, user, password, timeout=1)
                    self.Connection = True
                    break
                except TimeoutError:
                    self.retries = self.retries + 1
                    if (self.retries >= self.maximum_retries):
                        self.timeout.emit()
                        self.finished.emit()
                    print(f"Connection retries: {self.retries}")
                    self.Connection = False
            return client
        server = self.ip
        port = 22
        user = "pi"
        password = "tausat1234"
        ssh = createSSHClient(server, port, user, password)
        if self.Connection is True:
            scp = SCPClient(ssh.get_transport())
            scp.put(self.filename.encode('utf-8'), "/home/pi/Video")
            ssh.close()
            scp.close()
            self.finished.emit()


escapes = [r"\n", "b'", "r'", "\\"]

if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())
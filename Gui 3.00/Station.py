# -*- coding: utf-8 -*-
import sys
sys.path.append(r"C:\Users\ACER\PycharmProjects\Gui\venv\Lib\site-packages")
from PyQt5.QtWidgets import QApplication, QMainWindow
from Telemetri import Ui_Form as telemetri
from grafikler import Grafik
import Thread
from Model3D import Model
from Map import Map
from ADI import qfi_ADI
import serial
from PyQt5 import QtCore, QtGui, QtWidgets

escapes=[r"\n","b'","r'","\\"]


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.Thread_Active = False

    def Ayril_fonk(self):
        if self.Thread_Active is True:
            self.Data_Thread.ser.write(b"a")
    def Baslat_fonk(self):
        if self.Thread_Active is True:
            self.Data_Thread.ser.write(b"b")
    def Video_Sec(self):
        pass
    def Video_Gonder(self):
        pass
    def Motor_Ac(self):
        if self.Thread_Active is True:
            self.Data_Thread.ser.write(b"c")
    def Motor_Kapa(self):
        if self.Thread_Active is True:
            self.Data_Thread.ser.write(b"d")
    def Kalibrasyon_fonk(self):
        if self.Thread_Active is True:
            self.Data_Thread.ser.write(b"s")
    def Asenkron_Video(self):
        if self.Thread_Active is True:
            self.Data_Thread.ser.write(b"f")
    def Motor_Tahrip_fonk(self):
        if self.Thread_Active is True:
            self.Data_Thread.ser.write(b"m")
    def RPM_1LEVEL_fonk(self):
        if self.Thread_Active is True:
            self.Data_Thread.ser.write(b"t")
    def RPM_2LEVEL_fonk(self):
        pass
    def RPM_3LEVEL_fonk(self):
        pass

    def Change_Thread_Status(self,Thread_Status):
            self.Thread_Active = Thread_Status
            print(f"29{self.Thread_Active}")
    def Start_Data_Thread(self,port="COM5",baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        if self.Thread_Active is False:
            self.Data_Thread=Thread.Worker2(port,baudrate)
            self.Data_Thread.start()

            self.Update_Thread = Thread.Worker1(self.Telemetri, self.Data_Thread, self.Harita, self.GPS1_Lat_Value, self.GPS1_Long_Value, self.GPS1_Alt_Value, self.GPS2_Lat_Value, self.GPS2_Long_Value, self.GPS2_Alt_Value)
            self.Update_Thread2 = Thread.Worker4(self.Data_Thread, self.temp_data_line, self.alti_data_line, self.alti_diff_data_line, self.pressure_data_line, self.velocity_data_line)
            self.Update_Thread.start()
            self.Update_Thread2.start()

            self.Data_Thread.Model_Update.connect(self.Model_Update)
            self.Data_Thread.Status_Signal.connect(self.Change_Thread_Status)
            return
        if self.Thread_Active is True:
            self.Data_Thread.stop()
            self.Update_Thread.stop()

            self.Data_Thread=Thread.Worker2(port,baudrate)
            self.Data_Thread.start()

            self.Update_Thread = Thread.Worker1(self.Telemetri, self.Data_Thread, self.Harita, self.GPS1_Lat_Value,
                                                self.GPS1_Long_Value, self.GPS1_Alt_Value, self.GPS2_Lat_Value,
                                                self.GPS2_Long_Value, self.GPS2_Alt_Value)
            self.Update_Thread2 = Thread.Worker4(self.Data_Thread, self.temp_data_line, self.alti_data_line,
                                                 self.alti_diff_data_line, self.pressure_data_line,
                                                 self.velocity_data_line)
            self.Update_Thread.start()
            self.Update_Thread2.start()

            self.Data_Thread.Model_Update.connect(self.Model_Update)
            self.Data_Thread.Status_Signal.connect(self.Change_Thread_Status)
            return

    def CreateActions(self):
        self.port = "COM5"
        self.baudrate = 115200
        self.COM1 = QtWidgets.QAction("&COM1", self)
        self.COM1.triggered.connect(lambda: self.Start_Data_Thread(port="COM1", baudrate=self.baudrate))
        self.COM2 = QtWidgets.QAction("&COM2", self)
        self.COM2.triggered.connect(lambda: self.Start_Data_Thread(port="COM2", baudrate=self.baudrate))
        self.COM3 = QtWidgets.QAction("&COM3", self)
        self.COM3.triggered.connect(lambda: self.Start_Data_Thread(port="COM3", baudrate=self.baudrate))
        self.COM4 = QtWidgets.QAction("&COM4", self)
        self.COM4.triggered.connect(lambda: self.Start_Data_Thread(port="COM4", baudrate=self.baudrate))
        self.COM5 = QtWidgets.QAction("&COM5", self)
        self.COM5.triggered.connect(lambda: self.Start_Data_Thread(port="COM5", baudrate=self.baudrate))
        self.COM6 = QtWidgets.QAction("&COM6", self)
        self.COM6.triggered.connect(lambda: self.Start_Data_Thread(port="COM6", baudrate=self.baudrate))
        self.COM7 = QtWidgets.QAction("&COM7", self)
        self.COM7.triggered.connect(lambda: self.Start_Data_Thread(port="COM7", baudrate=self.baudrate))
        self.COM8 = QtWidgets.QAction("&COM8", self)
        self.COM8.triggered.connect(lambda: self.Start_Data_Thread(port="COM8", baudrate=self.baudrate))
        self.COM9 = QtWidgets.QAction("&COM9", self)
        self.COM9.triggered.connect(lambda: self.Start_Data_Thread(port="COM9", baudrate=self.baudrate))
        self.COM10 = QtWidgets.QAction("&COM10", self)
        self.COM10.triggered.connect(lambda: self.Start_Data_Thread(port="COM10", baudrate=self.baudrate))
        self.COM11 = QtWidgets.QAction("&COM11", self)
        self.COM11.triggered.connect(lambda: self.Start_Data_Thread(port="COM11", baudrate=self.baudrate))
        self.COM12 = QtWidgets.QAction("&COM12", self)
        self.COM12.triggered.connect(lambda: self.Start_Data_Thread(port="COM12", baudrate=self.baudrate))
        self.COM13 = QtWidgets.QAction("&COM13", self)
        self.COM13.triggered.connect(lambda: self.Start_Data_Thread(port="COM13", baudrate=self.baudrate))
        self.COM14 = QtWidgets.QAction("&COM14", self)
        self.COM14.triggered.connect(lambda: self.Start_Data_Thread(port="COM14", baudrate=self.baudrate))
        self.COM15 = QtWidgets.QAction("&COM15", self)
        self.COM15.triggered.connect(lambda: self.Start_Data_Thread(port="COM15", baudrate=self.baudrate))
        self.COM16 = QtWidgets.QAction("&COM16", self)
        self.COM16.triggered.connect(lambda: self.Start_Data_Thread(port="COM16", baudrate=self.baudrate))
        self.COM17 = QtWidgets.QAction("&COM17", self)
        self.COM17.triggered.connect(lambda: self.Start_Data_Thread(port="COM17", baudrate=self.baudrate))
        self.COM18 = QtWidgets.QAction("&COM18", self)
        self.COM18.triggered.connect(lambda: self.Start_Data_Thread(port="COM18", baudrate=self.baudrate))
        self.COM19 = QtWidgets.QAction("&COM19", self)
        self.COM19.triggered.connect(lambda: self.Start_Data_Thread(port="COM19", baudrate=self.baudrate))
        self.COM20 = QtWidgets.QAction("&COM20", self)
        self.COM20.triggered.connect(lambda: self.Start_Data_Thread(port="COM20", baudrate=self.baudrate))

        self.Baudrate_9600 = QtWidgets.QAction("9600", self)
        self.Baudrate_9600.triggered.connect(lambda: self.Start_Data_Thread(port=self.port, baudrate=9600))
        self.Baudrate_115200 = QtWidgets.QAction("115200", self)
        self.Baudrate_115200.triggered.connect(lambda: self.Start_Data_Thread(port=self.port, baudrate=115200))
        self.Baudrate_230400 = QtWidgets.QAction("230400", self)
        self.Baudrate_230400.triggered.connect(lambda: self.Start_Data_Thread(port=self.port, baudrate=230400))
        self.Baudrate_1000000 = QtWidgets.QAction("1000000", self)
        self.Baudrate_1000000.triggered.connect(lambda: self.Start_Data_Thread(port=self.port, baudrate=1000000))
        self.Baudrate_2000000 = QtWidgets.QAction("2000000", self)
        self.Baudrate_2000000.triggered.connect(lambda: self.Start_Data_Thread(port=self.port, baudrate=2000000))

    def CreateMenuBar(self):
        menubar = QtWidgets.QMenuBar(MainWindow)
        menubar.setGeometry(QtCore.QRect(0, 0, 1920, 26))
        menubar.setObjectName("menubar")

        Ayarlar = QtWidgets.QMenu("&Ayarlar", self)
        menubar.addMenu(Ayarlar)

        Port = QtWidgets.QMenu("&Port",self)
        Port.addActions([self.COM1,self.COM2,self.COM3,self.COM4,self.COM5,self.COM6,self.COM6,self.COM7,self.COM8,self.COM9,self.COM10,self.COM11,self.COM12,self.COM13,self.COM14,self.COM15,self.COM16,self.COM17,self.COM18,self.COM19,self.COM20])
        Ayarlar.addMenu(Port)

        Baudrate = QtWidgets.QMenu("&Baudrate",self)
        Baudrate.addActions([self.Baudrate_9600,self.Baudrate_115200,self.Baudrate_230400,self.Baudrate_1000000,self.Baudrate_2000000])
        Ayarlar.addMenu(Baudrate)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowIcon(QtGui.QIcon('Logo.png'))
        MainWindow.resize(1920, 1080)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)

        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("#Top {\nbackground-color:rgb(26, 217, 255);\nbackground-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(34, 172, 209, 255), stop:1 rgba(214, 255, 252, 255));\n}\n\n#Bottom\n{\nbackground-color:rgb(198, 198, 198);\n}")
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.Bottom = QtWidgets.QWidget(self.centralwidget)
        self.Bottom.setEnabled(True)
        self.Bottom.setGeometry(QtCore.QRect(0, 100, 1920, 980))
        self.Bottom.setObjectName("Bottom")
        self.Left = QtWidgets.QWidget(self.Bottom)
        self.Left.setGeometry(QtCore.QRect(0, 0, 480, 760))
        self.Left.setStyleSheet("background-color:rgb(5, 107, 127)")
        self.Left.setObjectName("Left")

        self.Harita=Map(Window = self.Left)
        # self.Harita.SetupUi(self.Left)
        # self.Harita.layout.setGeometry(QtCore.QRect(0, 360, 480, 360))

        self.Right = QtWidgets.QWidget(self.Bottom)
        self.Right.setGeometry(QtCore.QRect(1440, 0, 480, 760))
        self.Right.setObjectName("Right")

        self.Model=Model()
        self.Model.SetupUi(self.Right)
        self.Model3D=self.Model.view
        self.Model3D.setGeometry(QtCore.QRect(0, 0, 480, 360))
        self.Model3D.setObjectName("Model3D")

        self.Angles = QtWidgets.QWidget(self.Right)
        self.Angles.setGeometry(QtCore.QRect(0, 0, 81, 111))
        self.Angles.setObjectName("Angles")
        self.Angles_Layout = QtWidgets.QVBoxLayout(self.Angles)
        self.Angles_Layout.setContentsMargins(0, 0, 0, 0)
        self.Angles_Layout.setObjectName("Angles_Layout")
        self.Roll = QtWidgets.QLabel(self.Angles)
        self.Roll.setTextFormat(QtCore.Qt.AutoText)
        self.Roll.setObjectName("Roll")
        self.Angles_Layout.addWidget(self.Roll)
        self.Pitch = QtWidgets.QLabel(self.Angles)
        self.Pitch.setObjectName("Pitch")
        self.Angles_Layout.addWidget(self.Pitch)
        self.Yaw = QtWidgets.QLabel(self.Angles)
        self.Yaw.setObjectName("Yaw")
        self.Angles_Layout.addWidget(self.Yaw)
        self.Roll.setText("Roll=0°")
        self.Pitch.setText("Pitch=0°")
        self.Yaw.setText("Yaw=0°")
        self.Angles.setStyleSheet("font-family: 'Lucida Console', 'Courier New', monospace; color:rgb(255,255,255); font-weight: 600;")

        self.adi = qfi_ADI(self)
        self.adi.resize(480, 360)
        self.adi.reinit()
        self.Gosterge = QtWidgets.QWidget(self.Right)
        self.Gosterge.setGeometry(QtCore.QRect(0, 330, 480, 360))
        self.Gosterge.setObjectName("Gosterge")
        self.Altimeter=QtWidgets.QGridLayout(self.Gosterge)
        self.Altimeter.addWidget(self.adi,0,0)

        self.Telemetri=telemetri()
        self.Telemetri.setupUi(self.Bottom)
        self.Telemetri.Telemetri.setGeometry(QtCore.QRect(480, 0, 960, 360))
        self.Telemetri.setObjectName("Telemetri")

        self.graphs=Grafik()
        self.graphs.setupUi(self.Bottom)
        self.graphs.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 670, 1920, 230))
        self.temp_x =[]
        self.temp_y = []
        self.temp_data_line=self.graphs.Temp.plot(self.temp_x,self.temp_y,pen=self.graphs.Temp_pen)
        self.alti_x = []
        self.alti_y = []
        self.alti_data_line = self.graphs.Altitude.plot(self.alti_x, self.alti_y, pen=self.graphs.Temp_pen)
        self.alti_diff_x = []
        self.alti_diff_y = []
        self.alti_diff_data_line = self.graphs.Altitude_Difference.plot(self.alti_diff_x, self.alti_diff_y, pen=self.graphs.Temp_pen)
        self.pressure_x = []
        self.pressure_y = []
        self.pressure_data_line = self.graphs.Pressure.plot(self.pressure_x, self.pressure_y, pen=self.graphs.Temp_pen)
        self.velocity_x = []
        self.velocity_y = []
        self.velocity_data_line = self.graphs.Velocity.plot(self.velocity_x, self.velocity_y, pen=self.graphs.Temp_pen)
        # self.temp_y = [700, 660, 630, 600, 580, 560, 550, 550, 500, 480]
        # self.graphs.Altitude.plot(self.temp_x,self.temp_y,pen=self.graphs.Temp_pen)
        # self.temp_y=[0, 10, 20, 25, 30, 40, 50, 70, 80, 90]
        # self.graphs.Altitude_Difference.plot(self.temp_x,self.temp_y,pen=self.graphs.Temp_pen)
        # self.temp_y=[880,900,940,960,970,980,990,1000,1010,1030]
        # self.graphs.Pressure.plot(self.temp_x,self.temp_y,pen=self.graphs.Temp_pen)
        # self.temp_y=[30,25,20,15,15,15,15,12,10,9]
        # self.graphs.Velocity.plot(self.temp_x,self.temp_y,pen=self.graphs.Temp_pen)


        self.Gps = QtWidgets.QFrame(self.Bottom)
        self.Gps.setGeometry(QtCore.QRect(485,365,400,300))
        self.Gps.setStyleSheet("")
        self.Gps.setFrameShape(QtWidgets.QFrame.Panel)
        self.Gps.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Gps.setLineWidth(3)
        self.Gps.setMidLineWidth(1)
        self.Gps.setObjectName("Gps")
        self.Gps.setStyleSheet(("background-color:rgbrgb(238, 236, 210);\n""color:rgb(80, 80, 80),;\n""font: 12pt \"Arial Rounded MT Bold\";\n""text-align:center;"))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.Gps)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.GPS1_Lat = QtWidgets.QLabel(self.Gps)
        self.GPS1_Lat.setObjectName("GPS1 Lat")
        self.horizontalLayout_2.addWidget(self.GPS1_Lat)
        self.GPS1_Long = QtWidgets.QLabel(self.Gps)
        self.GPS1_Long.setObjectName("GPS1_Long")
        self.horizontalLayout_2.addWidget(self.GPS1_Long)
        self.label = QtWidgets.QLabel(self.Gps)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.GPS1_Lat_Value = QtWidgets.QLabel(self.Gps)
        self.GPS1_Lat_Value.setObjectName("GPS1_Lat_Value")
        self.horizontalLayout_3.addWidget(self.GPS1_Lat_Value)
        self.GPS1_Long_Value = QtWidgets.QLabel(self.Gps)
        self.GPS1_Long_Value.setObjectName("GPS1_Long_Value")
        self.horizontalLayout_3.addWidget(self.GPS1_Long_Value)
        self.GPS1_Alt_Value = QtWidgets.QLabel(self.Gps)
        self.GPS1_Alt_Value.setObjectName("GPS1_Alt_Value")
        self.horizontalLayout_3.addWidget(self.GPS1_Alt_Value)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.GPS2_Lat = QtWidgets.QLabel(self.Gps)
        self.GPS2_Lat.setObjectName("GPS2_Lat")
        self.horizontalLayout_4.addWidget(self.GPS2_Lat)
        self.GPS2_Long = QtWidgets.QLabel(self.Gps)
        self.GPS2_Long.setObjectName("GPS2_Long")
        self.horizontalLayout_4.addWidget(self.GPS2_Long)
        self.GPS2_Alt = QtWidgets.QLabel(self.Gps)
        self.GPS2_Alt.setObjectName("GPS2_Alt")
        self.horizontalLayout_4.addWidget(self.GPS2_Alt)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.GPS2_Lat_Value = QtWidgets.QLabel(self.Gps)
        self.GPS2_Lat_Value.setObjectName("GPS2_at_Value")
        self.horizontalLayout_5.addWidget(self.GPS2_Lat_Value)
        self.GPS2_Long_Value = QtWidgets.QLabel(self.Gps)
        self.GPS2_Long_Value.setObjectName("GPS2_Long_Value")
        self.horizontalLayout_5.addWidget(self.GPS2_Long_Value)
        self.GPS2_Alt_Value = QtWidgets.QLabel(self.Gps)
        self.GPS2_Alt_Value.setObjectName("GPS2_Alt_Value")
        self.horizontalLayout_5.addWidget(self.GPS2_Alt_Value)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.GPS2_Lat.setBuddy(self.Gps)
        self.GPS1_Lat.setText( "GPS1 Lat.")
        self.GPS1_Long.setText( "GPS1 Long.")
        self.label.setText( "GPS1 Alt.")
        self.GPS1_Lat_Value.setText( "42.3424")
        self.GPS1_Long_Value.setText( "32.525")
        self.GPS1_Alt_Value.setText("230")
        self.GPS2_Lat.setText( "GPS2 Lat.")
        self.GPS2_Long.setText( "GPS2 Long.")
        self.GPS2_Alt.setText( "GPS2 Alt.")
        self.GPS2_Lat_Value.setText( "42.3424")
        self.GPS2_Long_Value.setText( "32.525")
        self.GPS2_Alt_Value.setText( "230")


        self.Top = QtWidgets.QWidget(self.centralwidget)
        self.Top.setEnabled(True)
        self.Top.setGeometry(QtCore.QRect(0, 0, 1920, 100))
        self.Top.setStyleSheet("")
        self.Top.setObjectName("Top")

        self.frame = QtWidgets.QFrame(self.Top)
        self.frame.setGeometry(QtCore.QRect(125, 0, 691, 100))
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(15)
        self.Button = QtWidgets.QWidget(self.frame)
        self.frame.setGraphicsEffect(self.shadow)
        self.Button.setGraphicsEffect(self.shadow)

        self.Button.setGeometry(QtCore.QRect(1, 10, 650, 100))
        self.Button.setFont(font)
        self.Button.setStyleSheet("color:rgb(0, 0, 0);\n""font: 7pt \"Arial Rounded MT Bold\";\n""")
        self.Button.setObjectName("Button")
        self.Buttons = QtWidgets.QGridLayout(self.Button)
        self.Buttons.setObjectName("Buttons")
        self.Ayril = QtWidgets.QPushButton(self.Button)
        self.Ayril.clicked.connect(self.Ayril_fonk)
        self.Ayril.setObjectName("Ayril")
        self.Buttons.addWidget(self.Ayril, 0, 0, 1, 1)
        self.Kalibrasyon = QtWidgets.QPushButton(self.Button)
        self.Kalibrasyon.setObjectName("Kalibrasyon")
        self.Kalibrasyon.clicked.connect(self.Kalibrasyon_fonk)
        self.Buttons.addWidget(self.Kalibrasyon, 0, 3, 1, 1)
        self.Video_Sec = QtWidgets.QPushButton(self.Button)
        self.Video_Sec.setStyleSheet("")
        self.Video_Sec.setObjectName("Video_Sec")
        self.Buttons.addWidget(self.Video_Sec, 0, 1, 1, 1)
        self.Asenkron_Video = QtWidgets.QPushButton(self.Button)
        self.Asenkron_Video.setObjectName("Asenkron_Video")
        self.Buttons.addWidget(self.Asenkron_Video, 1, 3, 1, 1)
        self.Baslat = QtWidgets.QPushButton(self.Button)
        self.Baslat.clicked.connect(self.Baslat_fonk)
        self.Baslat.setStyleSheet("")
        self.Baslat.setObjectName("Baslat")
        self.Buttons.addWidget(self.Baslat, 1, 0, 1, 1)
        self.Video_Gonder = QtWidgets.QPushButton(self.Button)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(7)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.Video_Gonder.setFont(font)
        icon = QtGui.QIcon.fromTheme("0")
        self.Video_Gonder.setIcon(icon)
        self.Video_Gonder.setObjectName("Video_Gonder")
        self.Buttons.addWidget(self.Video_Gonder, 1, 1, 1, 1)
        self.Motor_Ac = QtWidgets.QPushButton(self.Button)
        self.Motor_Ac.setObjectName("Motor_Ac")
        self.Buttons.addWidget(self.Motor_Ac, 0, 2, 1, 1)
        self.Motor_Kapa = QtWidgets.QPushButton(self.Button)
        self.Motor_Kapa.setObjectName("Motor_Kapa")
        self.Buttons.addWidget(self.Motor_Kapa, 1, 2, 1, 1)

        self.shadow2 = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow2.setBlurRadius(15)
        self.Button2 = QtWidgets.QWidget(self.Top)
        self.Button2.setGraphicsEffect(self.shadow2)
        self.Button2.setGeometry(QtCore.QRect(1200, 10, 450, 100))
        self.Button2.setFont(font)
        self.Button2.setStyleSheet("color:rgb(0, 0, 0);\n""font: 7pt \"Arial Rounded MT Bold\";\n""")
        self.Button2.setObjectName("Button2")
        self.Buttons2 = QtWidgets.QGridLayout(self.Button2)
        self.Buttons2.setObjectName("Buttons2")
        self.Motor_Tahrip = QtWidgets.QPushButton(self.Button2)
        self.Motor_Tahrip.clicked.connect(self.Motor_Tahrip_fonk)
        self.Motor_Tahrip.setObjectName("Motor_Tahrip")
        self.Motor_Tahrip.setText("Motor Tahrik / Arttır")
        self.Buttons2.addWidget(self.Motor_Tahrip, 0, 0, 1, 1)
        self.RPM_1LEVEL = QtWidgets.QPushButton(self.Button2)
        self.RPM_1LEVEL.clicked.connect(self.RPM_1LEVEL_fonk)
        self.RPM_1LEVEL.setStyleSheet("")
        self.RPM_1LEVEL.setObjectName("RPM_1LEVEL")
        self.RPM_1LEVEL.setText("Motor Tahrik / Azalt")
        self.Buttons2.addWidget(self.RPM_1LEVEL, 1, 0, 1, 1)
        self.RPM_2LEVEL = QtWidgets.QPushButton(self.Button2)
        self.RPM_2LEVEL.setStyleSheet("")
        self.RPM_2LEVEL.setObjectName("RPM_2LEVEL")
        self.RPM_2LEVEL.setText("RPM 2. Kademe")
        self.RPM_2LEVEL.clicked.connect(self.RPM_2LEVEL_fonk)
        self.Buttons2.addWidget(self.RPM_2LEVEL, 0, 1, 1, 1)
        self.RPM_3LEVEL = QtWidgets.QPushButton(self.Button2)
        self.RPM_3LEVEL.setFont(font)
        icon = QtGui.QIcon.fromTheme("0")
        self.RPM_3LEVEL.setIcon(icon)
        self.RPM_3LEVEL.setObjectName("RPM_3LEVEL")
        self.RPM_3LEVEL.setText("RPM 3. Kademe")
        self.RPM_3LEVEL.clicked.connect(self.RPM_3LEVEL_fonk)
        self.Buttons2.addWidget(self.RPM_3LEVEL, 1, 1, 1, 1)


        # 485,365,400,300
        self.Durum = QtWidgets.QScrollArea(self.Bottom)
        self.Durum.setEnabled(True)
        self.Durum.setGeometry(QtCore.QRect(890, 365, 555, 300))
        self.Durum.setMinimumSize(QtCore.QSize(0, 0))
        self.Durum.setStyleSheet("background-color:rgb(26, 217, 255,0.1); font: 12pt")
        self.Durum.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.Durum.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.Durum.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.Durum.setWidgetResizable(True)
        self.Durum.setObjectName("Durum")

        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 277, 154))
        self.scrollAreaWidgetContents_2.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents_2.setStyleSheet("border: 2px solid black; background-color:rgb(0, 255, 0);;  font: 9pt 'Arial Rounded MT Bold';")
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.Red = "background-color:rgb(255, 0, 0);"
        self.Green = "background-color:rgb(0, 255, 0);"

        self.Bekleme_Asaması = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.Bekleme_Asaması.setObjectName("Bekleme_Asaması")
        self.Bekleme_Asaması.setStyleSheet(self.Red)
        self.verticalLayout_2.addWidget(self.Bekleme_Asaması)

        self.Yukselme_Asaması = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.Yukselme_Asaması.setObjectName("Yukselme_Asaması")
        self.verticalLayout_2.addWidget(self.Yukselme_Asaması)

        self.Pasif_Inıs_Asaması = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.Pasif_Inıs_Asaması.setObjectName("Pasif_Inıs_Asaması")
        self.verticalLayout_2.addWidget(self.Pasif_Inıs_Asaması)

        self.Aktif_Inıs_Ilk_Asama = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.Aktif_Inıs_Ilk_Asama.setObjectName("Aktif_Inıs_Ilk_Asama")
        self.verticalLayout_2.addWidget(self.Aktif_Inıs_Ilk_Asama)

        self.Askıda_Kalma_Asaması = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.Askıda_Kalma_Asaması.setObjectName("Askıda_Kalma_Asaması")
        self.verticalLayout_2.addWidget(self.Askıda_Kalma_Asaması)

        self.Aktif_Inıs_Ikıncı_Asama = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.Aktif_Inıs_Ikıncı_Asama.setObjectName("Aktif_Inıs_Ikıncı_Asama")
        # self.Aktif_Inıs_Ikıncı_Asama.setStyleSheet(self.Red)
        self.verticalLayout_2.addWidget(self.Aktif_Inıs_Ikıncı_Asama)

        self.Kurtarma_Asaması = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.Kurtarma_Asaması.setObjectName("Kurtarma_Asaması")
        self.verticalLayout_2.addWidget(self.Kurtarma_Asaması)

        self.Durum.setWidget(self.scrollAreaWidgetContents_2)

        self.Logo = QtWidgets.QLabel(self.Top)
        self.Logo.setGeometry(QtCore.QRect(15, 10, 100, 100))
        self.Logo.setAutoFillBackground(False)
        self.Logo.setStyleSheet("")
        self.Logo.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Logo.setText("")
        self.Logo.setPixmap(QtGui.QPixmap(":/newPrefix/Logo ve Afişler/TAU-SAT Model Uydu Takımı Logo.png"))
        self.Logo.setScaledContents(True)
        self.Logo.setWordWrap(False)
        self.Logo.setObjectName("Logo")
        self.shadow1 = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow1.setBlurRadius(15)
#         self.RPM = QtWidgets.QLabel(self.Top)
#         self.RPM.setGeometry(QtCore.QRect(810, 5, 100, 35))
#         self.RPM.setStyleSheet("color:rgb(0, 0, 0);\n"
# "font: 9pt \"Arial Rounded MT Bold\";\n"
# "background-color:rgb(255, 255, 255);\n"
# "text-align:center;")
#         self.RPM.setAlignment(QtCore.Qt.AlignCenter)
#         self.RPM.setObjectName("label")
#         self.RPM.setGraphicsEffect(self.shadow1)
#         self.shadow2 = QtWidgets.QGraphicsDropShadowEffect()
#         self.shadow2.setBlurRadius(15)
#         self.RPM_Value = QtWidgets.QLabel(self.Top)
#         self.RPM_Value.setGeometry(QtCore.QRect(810, 60, 100, 35))
#         self.RPM_Value.setGraphicsEffect(self.shadow2)
#         self.RPM_Value.setStyleSheet("color:rgb(255, 0, 0);\n"
# "font: 9pt \"Arial Rounded MT Bold\";\n"
# "background-color: rgb(255, 255, 255);\n"
# "text-align:center;")
#         self.RPM_Value.setAlignment(QtCore.Qt.AlignCenter)
#         self.RPM_Value.setObjectName("RPM_Value")
        self.progressBar = QtWidgets.QProgressBar(self.Top)
        self.progressBar.setGeometry(QtCore.QRect(800, 70, 241, 23))
        self.progressBar.setStyleSheet("color:rgb(0, 0, 0);\n""font: 7pt \"Arial Rounded MT Bold\";\n""")
        self.progressBar.setProperty("value", 23)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName("progressBar")
        self.Batarya_Container = QtWidgets.QWidget(self.Top)
        self.Batarya_Container.setGeometry(QtCore.QRect(1100, 33, 141, 80))
        self.Batarya_Container.setStyleSheet("#QProgressBar {\n""    border: 2px solid grey;\n""    border-radius: 5px;\n""}\n""\n""#QProgressBar::chunk {\n""    background-color: #05B8CC;\n""    width: 20px;\n""}")
        self.Batarya_Container.setObjectName("Batarya_Container")
        self.Batarya = QtWidgets.QProgressBar(self.Batarya_Container)
        self.Batarya.setGeometry(QtCore.QRect(10, 10, 31, 51))
        self.Batarya.setStyleSheet("#Batarya::chunk {\n""    background-color: rgb(255, 0, 4);\n""    height: 5px;\n""    margin: 0.5px;\n""}\n""#Batarya{\n""    border: 2px solid grey;\n""    border-color: rgb(255, 255, 255);\n""    text-align: center;\n""    background-color: rgb(255, 255, 255);\n""    border-radius: 5px;\n""}")
        self.Batarya.setMaximum(100)
        self.Batarya.setProperty("value", 25)
        self.Batarya.setTextVisible(False)
        self.Batarya.setOrientation(QtCore.Qt.Vertical)
        self.Batarya.setObjectName("Batarya")
        self.Batarya_Value = QtWidgets.QLabel(self.Batarya_Container)
        self.Batarya_Value.setGeometry(QtCore.QRect(45, 42, 55, 16))
        self.Batarya_Font = font
        self.Batarya_Font.setBold(False)
        self.Batarya_Font.setPointSize(8)
        self.Batarya_Value.setFont(self.Batarya_Font)
        self.Batarya_Value.setObjectName("Batarya_Value")
        self.Batarya_Value.setText("%25")
        self.shadow3 = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow3.setBlurRadius(15)
        self.Video_Aktarim = QtWidgets.QLabel(self.Top)
        self.Video_Aktarim.setGeometry(QtCore.QRect(830, 24, 171, 31))
        self.Video_Aktarim.setGraphicsEffect(self.shadow3)
        self.Video_Aktarim.setStyleSheet("color:rgb(0, 0, 0);\n""font: 7pt \"Arial Rounded MT Bold\";\n""background-color: rgb(255, 255, 255)\n""")
        self.Video_Aktarim.setAlignment(QtCore.Qt.AlignCenter)
        self.Video_Aktarim.setObjectName("Video_Aktarim")

        self.CreateActions()
        self.CreateMenuBar()


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.VBL = QtWidgets.QVBoxLayout(MainWindow)
        self.FeedLabel = QtWidgets.QLabel(MainWindow)
        self.VBL.addWidget(self.FeedLabel)
        self.Kamera = Thread.Worker3()
        self.Kamera.start()
        self.Kamera.ImageUpdate.connect(self.Camera_Update)
        self.VBL.setGeometry(QtCore.QRect(0,100,480,360))

    def Camera_Update(self, Image):
        self.FeedLabel.setPixmap(QtGui.QPixmap.fromImage(Image))

    def Camera_Update(self, Image):
        self.FeedLabel.setPixmap(QtGui.QPixmap.fromImage(Image))

    def Model_Update(self, angles):
        self.Model.view.removeItem(self.Model.mesh)
        self.Model.Restore()
        self.Model.view.addItem(self.Model.mesh)
        self.Model.mesh.rotate(angle=float(angles[2]), x=1, y=0, z=0)
        self.Model.mesh.rotate(angle=float(angles[0]), x=0, y=1, z=0)
        # self.Model.mesh.rotate(angle=10, x=1, y=0, z=0)
        # self.Model.mesh.rotate(angle=40, x=0, y=1, z=0)
        self.Model.mesh.rotate(angle=0, x=0, y=0, z=1)
        self.Roll.setText(f"Roll={angles[0]}°")
        self.Pitch.setText(f"Pitch={angles[1]}°")
        self.Yaw.setText(f"Yaw={angles[2]}°")
        self.adi.setRoll(float(angles[0]))
        self.adi.setPitch(float(angles[1]))
        self.adi.update()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Taü-Sat Yer İstasyonu"))
        self.Ayril.setText(_translate("MainWindow", "Ayrıl"))
        self.Kalibrasyon.setText(_translate("MainWindow", "Kalibrasyon"))
        self.Video_Sec.setText(_translate("MainWindow", "Video Seç"))
        self.Asenkron_Video.setText(_translate("MainWindow", "Asenkron Vid."))
        self.Baslat.setText(_translate("MainWindow", "Başlat"))
        self.Video_Gonder.setText(_translate("MainWindow", "Video Gönder"))
        self.Motor_Ac.setText(_translate("MainWindow", "Motor Aç"))
        self.Motor_Kapa.setText(_translate("MainWindow", "Motor Kapa"))
        self.Bekleme_Asaması.setText(_translate("MainWindow", "Bekleme Asaması"))
        self.Yukselme_Asaması.setText(_translate("MainWindow", "Yükselme Asaması"))
        self.Pasif_Inıs_Asaması.setText(_translate("MainWindow", "Pasif İniş Asaması"))
        self.Aktif_Inıs_Ilk_Asama.setText(_translate("MainWindow", "Aktif İniş İlk Asama"))
        self.Askıda_Kalma_Asaması.setText(_translate("MainWindow", "Askıda Kalma Asaması"))
        self.Aktif_Inıs_Ikıncı_Asama.setText(_translate("MainWindow", "Aktif İniş İkinci Asama"))
        self.Kurtarma_Asaması.setText(_translate("MainWindow", "Kurtarma Asaması"))
#       self.RPM.setText(_translate("MainWindow", "RPM"))
#       self.RPM_Value.setText(_translate("MainWindow", "10500"))
        self.Video_Aktarim.setText(_translate("MainWindow", "VİDEO AKTARIM DURUMU"))
import Source_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
from PyQt5 import QtWidgets,QtGui,QtCore,Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from Telemetri import Ui_Form
from grafikler import Grafik
from pushbuttons import Buttons
import Thread
from Model3D import Model
from Map import Map
from ADI import qfi_ADI
from random import randint
from pyqtgraph.opengl import GLViewWidget

escapes=[r"\n","b'","r'","\\"]



class Window(QMainWindow):
    def __init__(self):
        super(Window,self).__init__()
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowTitle("TAU-SAT Yer İstasyonu")
        self.setWindowIcon(QtGui.QIcon('Logo.png'))
        self.initUI()

    def initUI(self):
        self.buttons = Buttons()
        self.buttons.setupUi(self)

        self.Kamera = Thread.Worker1()
        self.VBL = QtWidgets.QVBoxLayout()
        self.FeedLabel = QtWidgets.QLabel(self)
        self.VBL.addWidget(self.FeedLabel)
        self.Kamera = Thread.Worker1()
        self.Kamera.start()
        self.Kamera.ImageUpdate.connect(self.Camera_Update)
        self.setLayout(self.VBL)
        self.VBL.setGeometry(QtCore.QRect(870,20,320,240))

        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 460, 221, 101))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")

        self.Serial_Port = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.Serial_Port.setFrameShape(QtWidgets.QFrame.Panel)
        self.Serial_Port.setObjectName("Serial_Port")
        self.Serial_Port.setText("Video aktarım durumu = Hayır")
        self.verticalLayout.addWidget(self.Serial_Port)

        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Uydu Durumu = Görev yükü iniş")
        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_3.setObjectName("label_3")
        self.label_3.setText("RPM = 11900")
        self.verticalLayout.addWidget(self.label_3)

        self.telemetri=Ui_Form()
        self.telemetri.setupUi(self)
        self.Data_Thread=Thread.Worker2()
        self.Data_Thread.start()
        self.Data_Thread.Telemetri_Update.connect(self.Telemetri_Update)

        self.graphs=Grafik()
        self.graphs.setupUi(self)
        self.temp_x =[1,2,3,4,5,6,7,8,9,10]
        self.temp_y = [23.5,24,24,24,24.5,25,26,27,28,28.5]
        self.temp_data_line=self.graphs.Temp.plot(self.temp_x,self.temp_y,pen=self.graphs.Temp_pen)
        self.temp_y = [700, 660, 630, 600, 580, 560, 550, 550, 500, 480]
        self.graphs.Altitude.plot(self.temp_x,self.temp_y,pen=self.graphs.Temp_pen)
        self.temp_y=[0, 10, 20, 25, 30, 40, 50, 70, 80, 90]
        self.graphs.Altitude_Difference.plot(self.temp_x,self.temp_y,pen=self.graphs.Temp_pen)
        self.temp_y=[880,900,940,960,970,980,990,1000,1010,1030]
        self.graphs.Pressure.plot(self.temp_x,self.temp_y,pen=self.graphs.Temp_pen)
        self.temp_y=[30,25,20,15,15,15,15,12,10,9]
        self.graphs.Velocity.plot(self.temp_x,self.temp_y,pen=self.graphs.Temp_pen)
        self.Data_Thread.Graph_Update.connect(self.Graph_Update)

        self.Model=Model()
        self.Model.SetupUi(self)
        self.Model3D=self.Model.view
        self.Model3D.setGeometry(QtCore.QRect(870, 280, 320, 300))
        self.Data_Thread.Model_Update.connect(self.Model_Update)

        self.map=Map()
        self.map.SetupUi(self)

        self.adi = qfi_ADI(self)
        self.adi.resize(300, 300)
        self.adi.reinit()
        self.Box = QtWidgets.QWidget(self)
        self.Box.setGeometry(QtCore.QRect(230,300,300,300))
        self.Box.setObjectName("Box")
        self.Altimeter=QtWidgets.QGridLayout(self.Box)
        self.Altimeter.addWidget(self.adi,0,0)

        self.Logo=QtWidgets.QLabel(self)
        self.PNG=QtGui.QImage("Logo.png",format="Format_ARGB32")
        self.PNG=self.PNG.scaled(300,300,1)
        self.PNG=QtGui.QPixmap.fromImage(self.PNG)
        self.Logo.setPixmap(self.PNG)
        self.Logo.setStyleSheet("QLabel{ background-color: transparent;}")
        self.Logo.setGeometry(QtCore.QRect(-20,0,300,300))

        self.Angles = QtWidgets.QWidget(self)
        self.Angles.setGeometry(QtCore.QRect(870, 280, 81, 111))
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
        self.Roll.setText("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n""<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n""p, li { white-space: pre-wrap; }\n""</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n""<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#ffffff;\">Roll = 0°</span></p></body></html>")
        self.Pitch.setText("<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#ffffff;\">Pitch = 0°</span></p></body></html>")
        self.Yaw.setText("<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#ffffff;\">Yaw = 0°</span></p></body></html>")

    def Telemetri_Update(self,display):
        self.Serial_Port.setText(display)
        self.telemetri.Telemetri.insertRow(0)
        item = QtWidgets.QTableWidgetItem()
        self.telemetri.Telemetri.setItem(0, 0, item)
        item.setText(display)


    def Camera_Update(self, Image):
        self.FeedLabel.setPixmap(QtGui.QPixmap.fromImage(Image))

    def Model_Update(self, data):
        self.Model.mesh.rotate(angle=float(data[0])/14, x=1,y=0,z=0)
        self.Model.mesh.rotate(angle=float(data[1])/14, x=0,y=1,z=0)
        self.Model.mesh.rotate(angle=float(data[2])/1, x=0,y=0,z=1)



    def Graph_Update (self,Temp):
        pass
          #print(display[display.find("Temp"):display.find("Temp")+10])
          #try:
          #    self.temp_x.append(self.temp_x[-1] + 1)
          #except:
          #    self.temp_x.append(1)
          #self.temp_y.append(float(Temp))
          #self.temp_data_line.setData(self.temp_x,self.temp_y)

pic="""MainWindow
{
background-image:url(C:/Users/ACER/PycharmProjects/Gui/Logo.png)
}"""
def window():
    app= QApplication(sys.argv)
    win= Window()
    win.show()
    #win.Update()
    sys.exit(app.exec_())

window()
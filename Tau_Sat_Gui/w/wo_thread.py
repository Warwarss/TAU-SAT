from PyQt5 import QtWidgets,QtGui,QtCore,Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
import sys
import serial
from Telemetri import Ui_Form
from grafikler import Grafik
from pushbuttons import Buttons
import csv
from Thread import Worker1
from ADI import qfi_ADI

escapes=[r"\n","b'","r'","\\"]



class Window(QMainWindow):
    def __init__(self):
        super(Window,self).__init__()
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowTitle("TAU-SAT Yer İstasyonu")
        self.initUI()
        self.timer_status=QTimer(self)
        self.timer_status.timeout.connect(lambda: self.Update())
        self.timer_status.start(1000)

    def initUI(self):
        self.buttons = Buttons()
        self.buttons.setupUi(self)

        self.Adi=qfi_ADI(self)
        self.Adi.init()

        self.Kamera = Worker1()
        self.VBL = QtWidgets.QVBoxLayout()
        self.FeedLabel = QtWidgets.QLabel(self)
        self.VBL.addWidget(self.FeedLabel)
        self.Kamera = Worker1()
        self.Kamera.start()
        self.Kamera.ImageUpdate.connect(self.ImageUpdateSlot)
        self.setLayout(self.VBL)
        self.VBL.setGeometry(QtCore.QRect(870,20,320,240))

        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 200, 221, 101))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")

        self.Serial_Port = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.Serial_Port.setFrameShape(QtWidgets.QFrame.Panel)
        self.Serial_Port.setObjectName("Serial_Port")
        self.verticalLayout.addWidget(self.Serial_Port)

        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)

        self.telemetri=Ui_Form()
        self.telemetri.setupUi(self)

        self.graphs=Grafik()
        self.graphs.setupUi(self)
        self.temp_x=[]
        self.temp_y=[]
        self.temp_data_line=self.graphs.Temp.plot(self.temp_x,self.temp_y,pen=self.graphs.Temp_pen)


    def Update(self):
        display=str(ser.read_until())
        for x in escapes:
            display=display.replace(x ,"")
        self.Serial_Port.setText(display)

        #self.Temp_Value=(display[display.find("Temp")+5:display.find("Temp")+10])

        #print(display[display.find("Temp"):display.find("Temp")+10])
        
       # try:
       #     self.temp_x.append(self.temp_x[-1] + 1)
       # except:
       #     self.temp_x.append(1)
       # self.temp_y.append(float(display))
       # self.temp_data_line.setData(self.temp_x,self.temp_y)

        self.telemetri.Telemetri.insertRow(0)
        item = QtWidgets.QTableWidgetItem()
        self.telemetri.Telemetri.setItem(0, 0, item)
        item.setText(display)

        with open('Telemetri_Verisi.csv', 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow([display])

    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QtGui.QPixmap.fromImage(Image))


def window():
    app= QApplication(sys.argv)
    win= Window()
    win.show()
    win.Update()
    sys.exit(app.exec_())



ser = serial.Serial("COM5","9600")
window()

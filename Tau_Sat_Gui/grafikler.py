from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph

class Grafik(object):
    def setupUi(self, Form):
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 600, 1200, 200))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.Temp = pyqtgraph.PlotWidget(self.horizontalLayoutWidget)
        self.Temp.setObjectName("widget_3")
        self.Temp.setBackground("w")
        #self.Temp.setXRange(0, 100, padding=0)
        #self.Temp.setYRange(20,30)
        self.Temp_pen = pyqtgraph.mkPen(color=(255, 0, 0))
        self.horizontalLayout_2.addWidget(self.Temp)


        self.Pressure = pyqtgraph.PlotWidget(self.horizontalLayoutWidget)
        self.Pressure.setObjectName("widget_5")
        self.horizontalLayout_2.addWidget(self.Pressure)
        self.Velocity = pyqtgraph.PlotWidget(self.horizontalLayoutWidget)
        self.Velocity.setObjectName("widget_4")
        self.horizontalLayout_2.addWidget(self.Velocity)
        self.Altitude = pyqtgraph.PlotWidget(self.horizontalLayoutWidget)
        self.Altitude.setObjectName("widget_2")
        self.horizontalLayout_2.addWidget(self.Altitude)
        self.Altitude_Difference = pyqtgraph.PlotWidget(self.horizontalLayoutWidget)
        self.Altitude_Difference.setObjectName("widget")
        self.horizontalLayout_2.addWidget(self.Altitude_Difference)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate

from pyqtgraph import PlotWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Grafik()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

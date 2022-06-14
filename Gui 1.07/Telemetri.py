
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        self.Telemetri = QtWidgets.QTableWidget(Form)
        self.Telemetri.setGeometry(QtCore.QRect(250, 20, 600,280))
        self.Telemetri.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Telemetri.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Telemetri.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.Telemetri.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.Telemetri.setShowGrid(True)
        self.Telemetri.setGridStyle(QtCore.Qt.SolidLine)
        self.Telemetri.setWordWrap(True)
        self.Telemetri.setRowCount(10)
        self.Telemetri.setColumnCount(23)
        self.Telemetri.setObjectName("Telemetri")
        self.Telemetri.horizontalHeader().setVisible(True)
        self.Telemetri.horizontalHeader().setCascadingSectionResizes(False)
        self.Telemetri.horizontalHeader().setDefaultSectionSize(80)
        self.Telemetri.horizontalHeader().setHighlightSections(False)
        self.Telemetri.horizontalHeader().setStretchLastSection(False)
        self.Telemetri.verticalHeader().setVisible(False)
        self.Telemetri.verticalHeader().setCascadingSectionResizes(False)
        self.Telemetri.setGridStyle(QtCore.Qt.NoPen)
        self.Telemetri.setAutoScroll(True)

        labels=("TAKIM NO","PAKET NUMARASI","GÖNDERME SAATİ","BASINÇ1","BASINÇ2","YÜKSEKLİK1","YÜKSEKLİK2","İRTİFA FARKI","İNİŞ HIZI","SICAKLIK","PİL GERİLİMİ","GPS1 LATITUDE","GPS1 LONGITUDE","GPS1 ALTITUDE","GPS2LATITUDE","GPS2 LONGITUDE","GPS2 ALTITUDE","UYDU STATÜSÜ","PITCH","ROLL","YAW","DÖNÜŞ SAYISI","VİDEO AKTARIM BİLGİSİ")
        self.Telemetri.setHorizontalHeaderLabels(labels)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.Telemetri.setFont(font)
        self.Telemetri.horizontalHeader().setFont(font)
        self.Telemetri.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.Telemetri.verticalHeader().setDefaultSectionSize(10)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.Telemetri.setSortingEnabled(False)
        __sortingEnabled = self.Telemetri.isSortingEnabled()
        self.Telemetri.setSortingEnabled(False)
        self.Telemetri.setSortingEnabled(__sortingEnabled)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

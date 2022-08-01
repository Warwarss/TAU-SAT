
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(QtWidgets.QTableWidget):
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
        self.Telemetri.rowCount()
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
        self.Telemetri.setAutoScroll(False)

        labels=("TAKIM\nNO","PAKET\nNUMARASI","GÖNDERME\nSAATİ","BASINÇ1","BASINÇ2","YÜKSEKLİK1","YÜKSEKLİK2","İRTİFA\nFARKI","İNİŞ\nHIZI","SICAKLIK","PİL\nGERİLİMİ","GPS1\nLATITUDE","GPS1\nLONGITUDE","GPS1\nALTITUDE","GPS2\nLATITUDE","GPS2\nLONGITUDE","GPS2\nALTITUDE","UYDU\nSTATÜSÜ","PITCH","ROLL","YAW","DÖNÜŞ\nSAYISI","VİDEO AKTARIM\nBİLGİSİ")
        self.Telemetri.setHorizontalHeaderLabels(labels)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.Telemetri.setFont(font)
        self.Telemetri.horizontalHeader().setFont(font)
        self.Telemetri.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.Telemetri.verticalHeader().setDefaultSectionSize(10)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

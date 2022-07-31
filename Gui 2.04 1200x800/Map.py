
import io
import folium # pip install folium
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine
from PyQt5 import QtCore

class Map(object):
    def SetupUi(self,Window):
        self.layout = QVBoxLayout()
        self.longtitude=41
        self.latitude=29
        #Window.setLayout(self.layout)
        coordinate = (self.longtitude, self.latitude)
        m = folium.Map(
        	tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        	zoom_start=13,
        	location=coordinate,
            attr='None'

        )
        # save map data to data object
        data = io.BytesIO()
        folium.Marker([self.longtitude, self.latitude]).add_to(m)
        m.save(data, close_file=False)
        self.webView = QWebEngineView(Window)
        self.webView.setHtml(data.getvalue().decode())
        self.layout.addWidget(self.webView)
        self.layout.setGeometry(QtCore.QRect(530, 310, 320, 270))

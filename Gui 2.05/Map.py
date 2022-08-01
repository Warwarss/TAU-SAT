
import io
import folium # pip install folium
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine
from PyQt5 import QtCore

class Map(object):
    def __init__(self, Window, longtitude = 42, latitude = 29):
        self.longtitude = longtitude
        self.latitude = latitude
        self.Window = Window
        self.webView = QWebEngineView(self.Window)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.webView)
        self.layout.setGeometry(QtCore.QRect(0, 360, 480, 360))
    def SetupUi(self):
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
        self.webView.setHtml(data.getvalue().decode())





import io
import folium # pip install folium
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine
from PyQt5 import QtCore
from jinja2 import Template

class Map(object):
    def __init__(self, Window, longtitude = 29, latitude = 41, longtitude2=29, latitude2=41):
        self.longtitude = longtitude
        self.latitude = latitude
        self.longtitude2 = longtitude2
        self.latitude2 = latitude2
        self.Window = Window
        self.webView = QWebEngineView(self.Window)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.webView)
        self.layout.setGeometry(QtCore.QRect(0, 0, 480, 360))
        self.FeatureGroup = folium.map.FeatureGroup(name="No")
        self.ControlLayer = folium.map.LayerControl()
        self.m = folium.Map(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', zoom_start=13, location=(self.longtitude, self.latitude), attr='None' )
        self.ControlLayer.add_to(self.m)
        data = io.BytesIO()
        self.m.save(data, close_file=False)
        self.webView.setHtml(data.getvalue().decode())
    def SetupUi(self):
        # save map data to data object
        coordinate = (self.latitude, self.longtitude)
        m = folium.Map(
        	tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        	zoom_start=13,
        	location=coordinate,
            attr='None'

        )
        # save map data to data object
        data = io.BytesIO()
        print(self.longtitude)
        folium.Marker([self.latitude, self.longtitude]).add_to(m)
        Red_Icon = folium.Icon(color='red')
        folium.Marker([self.latitude2, self.longtitude2], icon = Red_Icon).add_to(m)
        m.save(data, close_file=False)
        self.webView.setHtml(data.getvalue().decode())

    def add_marker(self, latitude, longitude):
        js = Template(
            """
        L.marker([{{latitude}}, {{longitude}}] )
            .addTo({{map}});
        """
        ).render(map=self.m.get_name(), latitude=float(latitude), longitude=float(longitude))
        self.webView.page().runJavaScript(js)
        print(latitude,longitude)


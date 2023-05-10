import io
import sys

from jinja2 import Template

import folium

from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView


class CoordinateProvider(QObject):
    coordinate_changed = pyqtSignal(float, float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._timer = QTimer(interval=1000)
        self._timer.timeout.connect(self.generate_coordinate)

    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.stop()

    def generate_coordinate(self):
        import random

        center_lat, center_lng = 41.8828, 12.4761
        x, y = (random.uniform(-0.001, 0.001) for _ in range(2))
        latitude = center_lat + x
        longitude = center_lng + y
        self.coordinate_changed.emit(latitude, longitude)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        coordinate = (41.8828, 12.4761)
        self.map = folium.Map(
            zoom_start=18, location=coordinate, control_scale=True, tiles=None
        )
        folium.raster_layers.TileLayer(
            tiles="http://mt1.google.com/vt/lyrs=m&h1=p1Z&x={x}&y={y}&z={z}",
            name="Standard Roadmap",
            attr="Google Map",
        ).add_to(self.map)
        folium.raster_layers.TileLayer(
            tiles="http://mt1.google.com/vt/lyrs=s&h1=p1Z&x={x}&y={y}&z={z}",
            name="Satellite Only",
            attr="Google Map",
        ).add_to(self.map)
        folium.raster_layers.TileLayer(
            tiles="http://mt1.google.com/vt/lyrs=y&h1=p1Z&x={x}&y={y}&z={z}",
            name="Hybrid",
            attr="Google Map",
        ).add_to(self.map)
        folium.LayerControl().add_to(self.map)
        folium.Marker(coordinate).add_to(self.map)

        data = io.BytesIO()
        self.map.save(data, close_file=False)

        self.map_view = QWebEngineView()
        self.map_view.setHtml(data.getvalue().decode())

        self.setCentralWidget(self.map_view)

    def add_marker(self, latitude, longitude):
        js = Template(
            """
        L.marker([{{latitude}}, {{longitude}}] )
            .addTo({{map}});
        L.circleMarker(
            [{{latitude}}, {{longitude}}], {
                "bubblingMouseEvents": true,
                "color": "#3388ff",
                "dashArray": null,
                "dashOffset": null,
                "fill": false,
                "fillColor": "#3388ff",
                "fillOpacity": 0.2,
                "fillRule": "evenodd",
                "lineCap": "round",
                "lineJoin": "round",
                "opacity": 1.0,
                "radius": 2,
                "stroke": true,
                "weight": 5
            }
        ).addTo({{map}});
        """
        ).render(map=self.map.get_name(), latitude=latitude, longitude=longitude)
        self.map_view.page().runJavaScript(js)


def main():
    app = QApplication(sys.argv)

    window = Window()
    window.showMaximized()

    provider = CoordinateProvider()
    provider.coordinate_changed.connect(window.add_marker)
    provider.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
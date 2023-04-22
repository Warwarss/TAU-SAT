import sys
import numpy as np
import time
from pyqtgraph.opengl import GLViewWidget, MeshData, GLMeshItem
from stl import mesh
from PyQt5.QtWidgets import *

class Model(object):
    def SetupUi(self,Window):
        np.seterr(divide='ignore', invalid='ignore')
        self.view = GLViewWidget(Window,rotationMethod='euler')
        self.stl_mesh = mesh.Mesh.from_file(r'C:\Users\ACER\PycharmProjects\Gui\gorev_yuku.stl')
        self.points =self.stl_mesh.points.reshape(-1, 3)
        self.faces = np.arange(self.points.shape[0]).reshape(-1, 3)
        self.mesh_data = MeshData(vertexes=self.points, faces=self.faces)
        self.mesh = GLMeshItem(meshdata=self.mesh_data, smooth=True, drawFaces=True, drawEdges=False, edgeColor=(0, 1, 0, 1), color=(0.047, 0.914, 0.752, 0), shader="normalColor")
        self.mesh.translate(dx=0, dy=0, dz=-95)
        self.view.addItem(self.mesh)
        self.stl_mesh = mesh.Mesh.from_file(r'C:\Users\ACER\PycharmProjects\Gui\Tasiyici.stl')
        self.points =self.stl_mesh.points.reshape(-1, 3)
        self.faces = np.arange(self.points.shape[0]).reshape(-1, 3)
        self.mesh_data = MeshData(vertexes=self.points, faces=self.faces)
        self.mesh = GLMeshItem(meshdata=self.mesh_data, smooth=True, drawFaces=True, drawEdges=False, edgeColor=(0, 1, 0, 1), color=(0.047, 0.914, 0.752, 0), shader="normalColor")
        self.mesh.translate(dx=0, dy=0, dz=155)
        self.view.addItem(self.mesh)
        self.view.setCameraPosition(azimuth=45,distance=400,elevation=50)

    def Restore(self):
        self.mesh = GLMeshItem(meshdata=self.mesh_data, smooth=True, drawFaces=False, drawEdges=True,edgeColor=(0, 1, 0, 1))
        self.mesh.translate(dx=0, dy=0, dz=0)
        #self.view.setCameraPosition(azimuth=45, distance=400, elevation=50)
        print(self.view.cameraParams())
    def Animasyon(self):
        dz = 0
        for x in range(5):
            for i in range(10000):
                self.mesh.translate(dx=0, dy=0, dz=dz)
                dz = 0+0.01

if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = QMainWindow()
    window.show()
    App.exec_()
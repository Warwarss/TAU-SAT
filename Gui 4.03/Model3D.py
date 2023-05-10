import sys, os
basedir = os.path.dirname(__file__)
import numpy as np
import time
from pyqtgraph.opengl import GLViewWidget, MeshData, GLMeshItem
from stl import mesh
from PyQt5.QtWidgets import *

class Model(object):
    def SetupUi(self,Window):
        np.seterr(divide='ignore', invalid='ignore')
        self.view = GLViewWidget(Window,rotationMethod='euler')
        self.stl_mesh = mesh.Mesh.from_file(os.path.join(basedir, 'gorev_yuku.stl'))
        self.points =self.stl_mesh.points.reshape(-1, 3)
        self.faces = np.arange(self.points.shape[0]).reshape(-1, 3)
        self.mesh_data_gy = MeshData(vertexes=self.points, faces=self.faces)
        self.mesh_gy = GLMeshItem(meshdata=self.mesh_data_gy, smooth=True, drawFaces=True, drawEdges=False, edgeColor=(0, 1, 0, 1), color=(0.047, 0.914, 0.752, 0), shader="normalColor")
        self.mesh_gy.translate(dx=0, dy=0, dz=-95)
        self.view.addItem(self.mesh_gy)
        self.stl_mesh = mesh.Mesh.from_file(os.path.join(basedir, 'Tasiyici.stl'))
        self.points =self.stl_mesh.points.reshape(-1, 3)
        self.faces = np.arange(self.points.shape[0]).reshape(-1, 3)
        self.mesh_data_tasiyici = MeshData(vertexes=self.points, faces=self.faces)
        self.mesh_tasiyici = GLMeshItem(meshdata=self.mesh_data_tasiyici, smooth=True, drawFaces=True, drawEdges=False, edgeColor=(0, 1, 0, 1), color=(0.047, 0.914, 0.752, 0), shader="normalColor")
        self.mesh_tasiyici.translate(dx=0, dy=0, dz=155)
        # self.view.addItem(self.mesh_tasiyici)
        self.view.setCameraPosition(azimuth=45,distance=400,elevation=50)
        self.mesh_gy.rotate(angle=-10.24, x=1, y=0, z=0)
        self.mesh_gy.rotate(angle=7.96, x=0, y=1, z=0)
        self.mesh_gy.rotate(angle=222.17, x=0, y=0, z=1)

    def Restore_gy(self):
        self.mesh_gy = GLMeshItem(meshdata=self.mesh_data_gy, smooth=True, drawFaces=True, drawEdges=False, edgeColor=(0, 1, 0, 1), color=(0.047, 0.914, 0.752, 0), shader="normalColor")
        self.mesh_gy.translate(dx=0, dy=0, dz=0)
        #self.view.setCameraPosition(azimuth=45, distance=400, elevation=50)
        print(self.view.cameraParams())

    def Restore_tasiyici(self):
        self.mesh_tasiyici = GLMeshItem(meshdata=self.mesh_data_tasiyici, smooth=True, drawFaces=True, drawEdges=False, edgeColor=(0, 1, 0, 1), color=(0.047, 0.914, 0.752, 0), shader="normalColor")
        self.mesh_tasiyici.translate(dx=0, dy=0, dz=0)

    def Animasyon(self):
        dz = 0
        for x in range(5):
            for i in range(100):
                self.mesh_tasiyici.translate(dx=0, dy=0, dz=dz)
                dz = 0+1

if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = QMainWindow()
    window.show()
    App.exec_()
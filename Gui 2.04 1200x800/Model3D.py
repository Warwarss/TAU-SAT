import sys
import numpy as np
from pyqtgraph.opengl import GLViewWidget, MeshData, GLMeshItem
from stl import mesh
from PyQt5.QtWidgets import *

class Model(object):
    def SetupUi(self,Window):
        np.seterr(divide='ignore', invalid='ignore')
        self.view = GLViewWidget(Window,rotationMethod='euler')
        self.stl_mesh = mesh.Mesh.from_file(r'C:\Users\ACER\PycharmProjects\Gui\gorev_yuku_acik.stl')
        self.points =self.stl_mesh.points.reshape(-1, 3)
        self.faces = np.arange(self.points.shape[0]).reshape(-1, 3)
        self.mesh_data = MeshData(vertexes=self.points, faces=self.faces)
        self.mesh = GLMeshItem(meshdata=self.mesh_data, smooth=True, drawFaces=False, drawEdges=True, edgeColor=(0, 1, 0, 1))
        self.mesh.translate(dx=0,dy=0,dz=-180)
        self.view.addItem(self.mesh)
        self.view.setCameraPosition(azimuth=45,distance=400,elevation=50)
    def Restore(self):
        self.mesh = GLMeshItem(meshdata=self.mesh_data, smooth=True, drawFaces=False, drawEdges=True,edgeColor=(0, 1, 0, 1))
        self.mesh.translate(dx=0, dy=0, dz=-180)
        #self.view.setCameraPosition(azimuth=45, distance=400, elevation=50)

        print(self.view.cameraParams())

if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = QMainWindow()
    window.show()
    App.exec_()
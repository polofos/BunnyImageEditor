from PyQt4.QtGui import QUndoCommand
from PyQt4 import QtCore, QtGui
from scipy import misc
from PIL import Image

class ComandoAbrir(QUndoCommand):
	def __init__(self,imagenes,nombre_archivo,archivo,ruta,imagen,imagenOriginal,desc):
		super(ComandoAbrir, self).__init__(desc)
		self.nombre_archivo = nombre_archivo
		self.imagenOriginal = imagenOriginal
		self.imagenes = imagenes
		self.imagenes.append((archivo, ruta, imagen))

	def redo(self):
		self.archivo = QtCore.QFileInfo(self.nombre_archivo).baseName()
		self.ruta = QtCore.QFileInfo(self.nombre_archivo).path()
		self.imagen = misc.imread(str(self.nombre_archivo))
		#carga imagen en el front end, incluye un resize
		self.mostrarImagen(self.imagenOriginal, self.imagen)

	def undo(self):
		#print(len(self.imagenes))
		if len(self.imagenes)<=1:
			self.archivo = ""
			self.ruta = ""
			self.imagen= []
			self.imagenOriginal.clear()
		else:
			imagen1 = self.imagenes.pop()
			self.archivo = imagen1[0]
			self.ruta = imagen1[1]
			self.imagen= imagen1[2]
			self.mostrarImagen(self.imagenOriginal, self.imagen)

	def mostrarImagen(self,label, Im):
		Im1 = Image.fromarray(Im)
		resolution = (532,546)
		scaler = Image.ANTIALIAS
		Im2 = Im1.resize(resolution, scaler)
		misc.imsave("Temp.tiff", Im2)
		label.setPixmap(QtGui.QPixmap("Temp.tiff"))
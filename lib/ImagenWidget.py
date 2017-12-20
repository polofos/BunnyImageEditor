from PyQt4 import QtGui, QtCore, uic
from PIL import Image
from scipy import misc

class ImagenWidget(QtGui.QDockWidget):

	# Señal cuando se enfoca la ventana
	# La señal contiene un atrivuto entero
	focusSignal = QtCore.pyqtSignal(int)	

	def __init__(self, mw):
		super(ImagenWidget,self).__init__(mw)
		self.setFocusPolicy(QtCore.Qt.StrongFocus)
		self.image = []						# image to display
		self.images = []					# state images
		self.imageOut = QtGui.QLabel("")	# label of the image
		self.nombre = "" 					# nombre de la imagen
		self.ruta = ""						# ruta de la imagen
		self.setWidget(self.imageOut)	
		self.index = 0						# index de la ImagenWidget en mw.imagenes[]

	def mostrarImagen(self, Im=[]):
		""" 
		Método que despliega la imagen en el ImagenWidget
		Args:
			Im: ndarray Opcional que contiene una imagen
				Si no se envía Im, se despliega la imagen definida en self.image
		"""
		if Im == []:
			Im = Image.fromarray(self.image)
		else:
			Im = Image.fromarray(Im)
		resolution = (532,546)
		scaler = Image.ANTIALIAS
		Im = Im.resize(resolution, scaler)
		misc.imsave("Temp.tiff", Im)
		self.imageOut.setPixmap(QtGui.QPixmap("Temp.tiff"))

	def focusInEvent(self,event):
		# Evento que se actiuva cuando la ventana se enfoca
		# el evento emite la señal focusSignal
		self.focusSignal.emit(self.index)

	def guardarImagen(self):
		# Método que guarda en la lista de imagenes la imagen actual (para deshacer)
		self.images.append(self.image)






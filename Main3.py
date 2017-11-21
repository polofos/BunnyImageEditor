import os
import sys
sys.path.append("lib")
sys.path.append("iconos")
import Iconos_rc
from scipy import misc
from PIL import Image
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import pyqtSlot
from Umbralizacion import umbralBinario, grises, mediana, moda
from pprint import pprint
import numpy as np

claseQT = uic.loadUiType("MainW2.ui")[0]

class VentanaP(QtGui.QMainWindow, claseQT):

	# Atributos de estado de la imagen
	ruta = ""
	archivo = ""
	imagen = []				# Imagen a trabajar
	imagenProcesada = []	# Imagen trabajada

	# Estados anteriores
	imagenes = []			# Imagenes a trabajar anteriores
	rutas = []

	#	Constructor
	#	Aqui se enlazan los botones con sus funciones
	#	mediante el metodo connect
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)
		self.actionAbrir.triggered.connect(self.abrir_click)
		self.actionGuardar.triggered.connect(self.guardar_click)
		self.actionCerrar.triggered.connect(self.cerrar_click)
		self.actionUmbralizar.triggered.connect(self.umbralizar_click)
		self.actionFijar.triggered.connect(self.fijar_click)
		
	##########################################################
	# Configuracion de los botones de la barra de herramientas
	##########################################################

	def abrir_click(self):
		nombre_archivo = QtGui.QFileDialog.getOpenFileName(self, 'Abrir archivo')
		if nombre_archivo:		
			# muestra un mensaje en status bar por 5 segundos
			self.statusBar().showMessage('"{}" archivo abierto'.format(nombre_archivo), 5000)			
			# carga imagen en el backend
			self.archivo = QtCore.QFileInfo(nombre_archivo).baseName()
			self.ruta = QtCore.QFileInfo(nombre_archivo).path()
			self.imagen = misc.imread(str(nombre_archivo))
			#carga imagen en el front end, incluye un resize
			self.mostrarImagen(self.imagenOriginal, self.imagen)

	def guardar_click(self):
		rutaGuardar = QtGui.QFileDialog.getSaveFileName(self, 'Guardar archivo', self.ruta+'/'+self.archivo+".jpg",
		 filter = "Images (*.png *.tiff *.jpg)")
		if rutaGuardar != '':
			# muestra un mensaje en status bar por 5 segundos
			self.statusBar().showMessage('"{}" archivo guardado'.format(self.ruta), 5000)
			Im = Image.fromarray(np.array(self.imagen))
			misc.imsave(rutaGuardar, Im)
			
	def umbralizar_click(self):
		# muestra un mensaje en status bar por 5 segundos
		self.statusBar().showMessage('"{}" Modo umbralizar'.format(self.archivo), 5000)
		# carga el widget flotante para escoger el umbral
		self.widgetUmbral = uic.loadUi("Umbral.ui")
		self.widgetUmbral.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
		self.widgetUmbral.show()
		# self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.widgetUmbral)
		self.widgetUmbral.radioButton.clicked.connect(self.umbralMedia)
		self.widgetUmbral.radioButton_2.clicked.connect(self.umbralMediana)
		self.widgetUmbral.radioButton_3.clicked.connect(self.umbralModa)
		self.widgetUmbral.radioButton_4.clicked.connect(self.umbralManual)
		self.widgetUmbral.aplicar.clicked.connect(self.umbralAplicar)
		self.widgetUmbral.aceptar.clicked.connect(self.umbralAceptar)
		self.widgetUmbral.cancelar.clicked.connect(self.umbralCancelar)
		self.widgetUmbral.umbralSlider.valueChanged.connect(self.umbralManualSlider)

	def cerrar_click(self):
		# Borrar estado del backend
		self.imagen = []
		self.imagenProcesada = []
		self.archivo = ""
		self.ruta = ""

		# Borrar imagenes dle frontend
		self.imagenOriginal.clear()
		self.imagenEditada.clear()

	def fijar_click(self):
		# Cambiar estado backend
		self.imagen = self.imagenProcesada
		self.imagenProcesada = []

		#Cambiar estado frontend
		self.imagenOriginal.setPixmap(QtGui.QPixmap("Temp.tiff"))
		self.imagenEditada.clear()


	#############################
	# Elementos del Widget Umbral
	#############################

	def umbralManual(self):
		self.widgetUmbral.umbralSlider.setEnabled(True)
		self.tipoUmbral = "manual"

	def umbralMedia(self):
		self.widgetUmbral.umbralSlider.setEnabled(False)
		self.tipoUmbral = "media"

	def umbralMediana(self):
		self.widgetUmbral.umbralSlider.setEnabled(False)
		self.tipoUmbral = "mediana"

	def umbralModa(self):
		self.widgetUmbral.umbralSlider.setEnabled(False)
		self.tipoUmbral = "moda"

	def umbralAplicar(self):
		# umbralizar en el backend
		I = Image.fromarray(self.imagen)
		Ig = grises(I)
		# switch tipo umbral
		if self.tipoUmbral == "manual":
			self.umbral = self.valorUmbral
		elif self.tipoUmbral == "media":
			self.umbral = int(Ig.mean())
		elif self.tipoUmbral == "mediana":
			self.umbral = mediana(Ig)
		elif self.tipoUmbral == "moda":
			self.umbral = moda(Ig)
		# print(self.umbral)
		Im = umbralBinario(Ig,self.umbral,self.widgetUmbral.invertir.checkState())
		self.imagenProcesada = Im
		self.archivo = self.archivo+'_umbral'
		# presentar umbralizada en el frontend
		self.mostrarImagen(self.imagenEditada,Im)

	def umbralManualSlider(self):
		self.valorUmbral = self.widgetUmbral.umbralSlider.value()*255/100
		self.widgetUmbral.sValue.setText(str(self.valorUmbral)+' %')

	def umbralAceptar(self):
		#self.umbralAplicar();
		self.widgetUmbral.close()

	def umbralCancelar(self):
		self.imagenEditada.clear()
		self.widgetUmbral.close()

	##############################
	# funciones auxiliares
	##############################

	def mostrarImagen(self,label, Im):
		Im1 = Image.fromarray(Im)
		resolution = (532,546)
		scaler = Image.ANTIALIAS
		Im2 = Im1.resize(resolution, scaler)
		misc.imsave("Temp.tiff", Im2)
		label.setPixmap(QtGui.QPixmap("Temp.tiff"))


################ Main de la app ###################################

def main():

	app = QtGui.QApplication(sys.argv)
	mv = VentanaP()
	mv.show()

	sys.exit(app.exec_())


if __name__ == '__main__':
    main()

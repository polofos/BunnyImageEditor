import os
import sys
sys.path.append("lib")
sys.path.append("iconos")
import Iconos_rc
import Comandos
from Histograma import graficarHistograma
from ImagenWidget import ImagenWidget
from scipy import misc
from PIL import Image
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QUndoStack, QComboBox 
from Umbralizacion import umbralBinario, umbralesBinarios, grises, mediana, moda
from OperacionesBasicas import RGB, suma, suma2, resta, mult
from OperacionesBasicas import lAnd1, lOr, lExor, lNot
from Histograma import histograma, expandirHistograma ,contraerHistograma
from Histograma import ecualizarHistograma, desplazarHistograma
from Filtros import filtroPromedio, filtroGausiano1, filtroLaplaciano
from Filtros import filtroPrewitt, filtroSobel, filtroRobert
from Filtros import filtroModa, filtroMediana, filtroMax, filtroMin
from Morfologia import cierre, apertura, cercoConvexo
from pprint import pprint
import numpy as np

claseQT = uic.loadUiType("MainW3.ui")[0]

class VentanaP(QtGui.QMainWindow, claseQT):

	# Atributos de estado de la imagen
	ruta = ""
	archivo = ""
	imagen = []				# Imagen a trabajar
	imagenProcesada = []	# Imagen trabajada
	imagenes = []			# Imagenes abiertas
	x = 0
	y = 0
	focus = 0
	# Estados anteriores
	estadosImagenes = []    # Lista de estados para "deshacer"

	#	Constructor
	#	Aqui se enlazan los botones con sus funciones
	#	mediante el metodo connect
	def __init__(self, parent=None):

		# Construye la MainWindow
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)

		# Define una QUndoStack (no usado)
		self.undoStack = QUndoStack(self)

		# Conecta los botones de la Barra de herramientas
		self.actionAbrir.triggered.connect(self.abrir_click)
		self.actionGuardar.triggered.connect(self.guardar_click)
		self.actionCerrar.triggered.connect(self.cerrar_click)
		self.actionUmbralizar.triggered.connect(self.umbralizar_click)
		self.actionEscalaDeGrises.triggered.connect(self.escalaGrises_click)
		self.actionRGB.triggered.connect(self.RGB_click)
		self.actionDeshacer.triggered.connect(self.deshacer_click)
		self.actionSuma.triggered.connect(self.suma_click)
		self.actionResta.triggered.connect(self.resta_click)
		self.actionMultiplicacion.triggered.connect(self.multiplicacion_click)
		self.actionAnd.triggered.connect(self.and_click)
		self.actionOr.triggered.connect(self.or_click)
		self.actionExor.triggered.connect(self.exor_click)
		self.actionNot.triggered.connect(self.not_click)
		self.actionHist.triggered.connect(self.hist_click)
		self.actionExpand.triggered.connect(self.expand_click)
		self.actionContr.triggered.connect(self.cont_click)
		self.actionDespl.triggered.connect(self.desp_click)
		self.actionEcu.triggered.connect(self.ecu_click)
		self.actionPromedio.triggered.connect(self.prom_click)
		self.actionPromedio_Pesado.triggered.connect(self.prom_pesado_click)
		self.actionFiltro_gausiano.triggered.connect(self.gausiano_click)
		self.actionLaplaciano.triggered.connect(self.laplaciano_click)
		self.actionPrewitt.triggered.connect(self.prewitt_click)
		self.actionSobel.triggered.connect(self.sobel_click)
		self.actionRobert.triggered.connect(self.robert_click)
		self.actionCierre.triggered.connect(self.cierre_click)
		self.actionApertura.triggered.connect(self.apertura_click)
		self.actionPasabanda.triggered.connect(self.pasabanda_click)
		self.actionMultiumbral.triggered.connect(self.multiumbral_click)
		
	##############################################################################
	# Configuracion de los botones de la barra de herramientas
	##############################################################################

	def abrir_click(self):
		# Método al que se conecta la señal del action Abrir

		# Obtenemos la ruta de un archivo con getOpenFile
		nombre_archivo = QtGui.QFileDialog.getOpenFileName(self, 'Abrir archivo')
		if nombre_archivo:		
			# muestra un mensaje en status bar por 5 segundos
			self.statusBar().showMessage('"{}" archivo abierto'.format(nombre_archivo), 5000)			
			# Abrir en ventanas
			# instanciamos ImagenWidget, subclase de QDockWidget
			dockWidget = ImagenWidget(self)
			
			# Conectamos la señal focusSignal con el método imagen_focus
			dockWidget.focusSignal.connect(self.imagen_focus)

			# Obtenemos archivo, ruta e imagen
			self.archivo = QtCore.QFileInfo(nombre_archivo).baseName()
			self.ruta = QtCore.QFileInfo(nombre_archivo).path()
			self.imagen = misc.imread(str(nombre_archivo))

			# Colocamos archivo, ruta e imagen en ImageWidget
			dockWidget.nombre = self.archivo
			dockWidget.ruta = self.ruta
			dockWidget.image = self.imagen

			# Creamos título, desactivamos áreas y damos todos los permisos a ImageWidget
			dockWidget.setWindowTitle(self.archivo)
			dockWidget.setAllowedAreas(QtCore.Qt.NoDockWidgetArea)
			dockWidget.setFeatures(dockWidget.AllDockWidgetFeatures)

			# Obtenemos y fijamos el index dento de imagenes[]
			dockWidget.index = len(self.imagenes)

			# Agregamos el ImageWidget a imagenes[]
			self.imagenes.append(dockWidget)

			# Pegamos la imagen en la etiqueta de la ImageWidget
			dockWidget.mostrarImagen()

			#Mostramos la ImageWidget
			self.addDockWidget(QtCore.Qt.TopDockWidgetArea, self.imagenes[dockWidget.index])
			
			# Hacemos la ImageWidget flotante y lo colocamos con move
			self.imagenes[dockWidget.index].setFloating(True)
			self.imagenes[dockWidget.index].move(100+self.x,100+self.y)

			# Llamamos aumentarXY para cambiar la posición de la siguiente ImageWidget
			self.aumentarXY()

	def guardar_click(self):
		# Método que se conecta con la señal del actionGuardar

		# Obtenemos ruta y archivo de imagenes[] con ayuda del index en self.focus
		ruta = self.imagenes[self.focus].ruta
		archivo = self.imagenes[self.focus].nombre

		# Obtenemos el nombre de archivo para guardar con getSaveFile
		rutaGuardar = QtGui.QFileDialog.getSaveFileName(self, 'Guardar archivo', ruta+'/'+archivo+".jpg",
		 filter = "Images (*.png *.tiff *.jpg)")
		if rutaGuardar != '':
			# Muestra un mensaje en status bar por 5 segundos
			self.statusBar().showMessage('"{}" archivo guardado'.format(ruta), 5000)
			# print(self.focus)

			# Cargamos la imagen desde imagenes[] y luego la guardamos
			Im = Image.fromarray(self.imagenes[self.focus].image)
			misc.imsave(rutaGuardar, Im)

	def cerrar_click(self):
		# Método que se conecta con la señal actionCerrar

		# Cerrar el ImageWidget enfocado (frontend)
		self.imagenes[self.focus].close()

		# eliminar ImageWidget enfocado de imagenes[] (backend)
		del self.imagenes[self.focus]
		for ventana in self.imagenes:
			if ventana.index > self.focus:
				ventana.index -= 1 
			
	def umbralizar_click(self):
		# Método que se conecta con la señal actionUmbralizar

		# Muestra un mensaje en status bar por 5 segundos
		self.statusBar().showMessage('"{}" Modo umbralizar'.format(self.archivo), 5000)
		self.imagenes[self.focus].guardarImagen()
		# Carga el widget flotante para escoger el umbral
		self.widgetUmbral = uic.loadUi("Umbral.ui")
		self.widgetUmbral.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
		# self.widgetUmbral.show()
		self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.widgetUmbral)
		self.widgetUmbral.setFloating(True)
		self.widgetUmbral.move(1000,300)

		# Conecta las señales provenientes del widgetUmbral
		self.widgetUmbral.media.clicked.connect(self.umbralMedia)
		self.widgetUmbral.mediana.clicked.connect(self.umbralMediana)
		self.widgetUmbral.moda.clicked.connect(self.umbralModa)
		self.widgetUmbral.manual.clicked.connect(self.umbralManual)
		self.widgetUmbral.aplicar.clicked.connect(self.umbralAplicar)
		self.widgetUmbral.aceptar.clicked.connect(self.umbralAceptar)
		self.widgetUmbral.cancelar.clicked.connect(self.umbralCancelar)
		self.widgetUmbral.umbralSlider.valueChanged.connect(self.umbralManualSlider)

	def multiumbral_click(self):
		self.statusBar().showMessage('"{}" Modo umbralizar'.format(self.archivo), 5000)
		self.imagenes[self.focus].guardarImagen()
		self.widgetUmbral = uic.loadUi('multiumbral.ui')
		self.widgetUmbral.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
		self.widgetUmbral.activar3.stateChanged.connect(self.multiActivar3)
		self.widgetUmbral.vs1.valueChanged.connect(self.vs1_change)
		self.widgetUmbral.vs2.valueChanged.connect(self.vs2_change)
		self.widgetUmbral.vs3.valueChanged.connect(self.vs3_change)
		self.widgetUmbral.aplicar.clicked.connect(self.multiAplicar)
		self.widgetUmbral.aceptar.clicked.connect(self.multiAceptar)
		self.widgetUmbral.cancelar.clicked.connect(self.multiCancelar)
		self.widgetUmbral.show()

	def escalaGrises_click(self):
		# Convierte la imagen desplegada a escala de grises y la despliega
		self.imagenes[self.focus].guardarImagen()
		Im = Image.fromarray(np.array(self.imagenes[self.focus].image))
		self.imagenes[self.focus].image = grises(Im)
		self.imagenes[self.focus].mostrarImagen()


	def RGB_click(self):
		# Convierte la imagen desplegada a alguno de sus canales RGB/YCM

		# Envía mensaje de 5 segundos
		self.statusBar().showMessage('"{}" Modo Canales'.format(self.archivo), 5000)
		self.imagenes[self.focus].guardarImagen()
		# Crea QDockWidget de canales y conecta sus 3 botones
		self.widgetCanal = uic.loadUi("Canal.ui")
		self.widgetCanal.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
		self.widgetCanal.show()
		self.widgetCanal.aplicar.clicked.connect(self.canalAplicar)
		self.widgetCanal.aceptar.clicked.connect(self.canalAceptar)
		self.widgetCanal.cancelar.clicked.connect(self.canalCancelar)

	def deshacer_click(self):
		self.imagenes[self.focus].image = self.imagenes[self.focus].images.pop()
		self.imagenes[self.focus].mostrarImagen()
		

	def suma_click(self):
		# Suma dos imágenes.
		self.imagenes[self.focus].images.append(self.imagenes[self.focus].image)
		self.operacionesPuntuales()
		self.op = "suma"

	def resta_click(self):
		# Resta dos imágenes.
		self.imagenes[self.focus].images.append(self.imagenes[self.focus].image)
		self.operacionesPuntuales()
		self.op = "resta"

	def multiplicacion_click(self):
		# Multiplica dos imágenes.
		self.imagenes[self.focus].images.append(self.imagenes[self.focus].image)
		self.operacionesPuntuales()
		self.op = "multiplicación"

	def and_click(self):
		# And de dos imágenes.
		self.imagenes[self.focus].images.append(self.imagenes[self.focus].image)
		self.operacionesPuntuales()
		self.op = "and"

	def or_click(self):
		# Or de dos imágenes.
		self.imagenes[self.focus].images.append(self.imagenes[self.focus].image)
		self.operacionesPuntuales()
		self.op = "or"

	def exor_click(self):
		# Exor de dos imágenes
		self.imagenes[self.focus].images.append(self.imagenes[self.focus].image)
		self.operacionesPuntuales()
		self.op = "exor"

	def not_click(self):
		# Invertir imagen.
		self.imagenes[self.focus].images.append(self.imagenes[self.focus].image)
		self.imagenes[self.focus].image = lNot(self.imagenes[self.focus].image)
		self.imagenes[self.focus].mostrarImagen()

	def hist_click(self):
		# Histograma.
		histograma(self.imagenes[self.focus].image)

	def expand_click(self):
		# expandir histograma
		self.imagenes[self.focus].images.append(self.imagenes[self.focus].image)
		self.operacionesHistograma("Expandir Histograma",2)		

	def cont_click(self):
		# contraer Histograma
		self.imagenes[self.focus].images.append(self.imagenes[self.focus].image)
		self.operacionesHistograma("Contraer Histograma",2)

	def desp_click(self):
		# desplazar Histograma
		self.imagenes[self.focus].images.append(self.imagenes[self.focus].image)
		self.operacionesHistograma("Desplazar Histograma", 1)

	def ecu_click(self):
		# ecualizar Histograma
		self.imagenes[self.focus].images.append(self.imagenes[self.focus].image)
		self.operacionesHistograma("Ecualizar Histograma", 0)

	def prom_click(self):
		# filtro Promedio
		self.imagenes[self.focus].images.append(self.imagenes[self.focus].image)
		I = self.imagenes[self.focus].image
		I = filtroPromedio(I)
		self.imagenes[self.focus].image = I
		self.imagenes[self.focus].mostrarImagen()

	def prom_pesado_click(self):
		# filtro Promedio Pesado
		self.imagenes[self.focus].images.append(self.imagenes[self.focus].image)
		self.filtro = 'promedio'
		self.WidgetFiltro = uic.loadUi("filtro.ui")
		self.WidgetFiltro.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
		self.WidgetFiltro.setWindowTitle("Filtro Promedio")
		self.WidgetFiltro.aplicar.clicked.connect(self.filtroAplicar)
		self.WidgetFiltro.aceptar.clicked.connect(self.filtroAceptar)
		self.WidgetFiltro.cancelar.clicked.connect(self.filtroCancelar)
		self.WidgetFiltro.show()

	def gausiano_click(self):
		# filtro gausiano
		self.imagenes[self.focus].images.append(self.imagenes[self.focus].image)
		self.filtro = 'gausiano'
		self.WidgetFiltro = uic.loadUi("filtro.ui")
		self.WidgetFiltro.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
		self.WidgetFiltro.setWindowTitle("Filtro Gausiano")
		self.WidgetFiltro.label.setText('Sigma:')
		self.WidgetFiltro.aplicar.clicked.connect(self.filtroAplicar)
		self.WidgetFiltro.aceptar.clicked.connect(self.filtroAceptar)
		self.WidgetFiltro.cancelar.clicked.connect(self.filtroCancelar)
		self.WidgetFiltro.show()

	def laplaciano_click(self):
		# filtro laplaciano
		self.imagenes[self.focus].images.append(self.imagenes[self.focus].image)
		self.filtro = 'laplaciano'
		self.WidgetFiltro = uic.loadUi("filtro.ui")
		self.WidgetFiltro.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
		self.WidgetFiltro.setWindowTitle("Filtro Laplaciano")
		self.WidgetFiltro.label.setText('Sigma:')
		self.WidgetFiltro.aplicar.clicked.connect(self.filtroAplicar)
		self.WidgetFiltro.aceptar.clicked.connect(self.filtroAceptar)
		self.WidgetFiltro.cancelar.clicked.connect(self.filtroCancelar)
		self.WidgetFiltro.show()

	def prewitt_click(self):
		# filtro prewitt
		self.imagenes[self.focus].images.append(self.imagenes[self.focus].image)
		I = self.imagenes[self.focus].image
		I = filtroPrewitt(I)
		self.imagenes[self.focus].image = I
		self.imagenes[self.focus].mostrarImagen()

	def sobel_click(self):
		# filtro prewitt
		self.imagenes[self.focus].images.append(self.imagenes[self.focus].image)
		I = self.imagenes[self.focus].image
		I = filtroSobel(I)
		self.imagenes[self.focus].image = I
		self.imagenes[self.focus].mostrarImagen()

	def robert_click(self):
		# filtro robert
		self.imagenes[self.focus].images.append(self.imagenes[self.focus].image)
		I = self.imagenes[self.focus].image
		I = filtroRobert(I)
		self.imagenes[self.focus].image = I
		self.imagenes[self.focus].mostrarImagen()	

	def pasabanda_click(self):
		self.imagenes[self.focus].images.append(self.imagenes[self.focus].image)
		self.widgetPasabanda = uic.loadUi("pasabanda.ui")
		self.widgetPasabanda.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
		self.widgetPasabanda.aplicar.clicked.connect(self.pasabandaAplicar)
		self.widgetPasabanda.aceptar.clicked.connect(self.pasabandaAceptar)
		self.widgetPasabanda.cancelar.clicked.connect(self.pasabandaCancelar)
		self.widgetPasabanda.show()

	def cierre_click(self):
		self.imagenes[self.focus].images.append(self.imagenes[self.focus].image)
		I = self.imagenes[self.focus].image
		est = np.zeros((3,3), dtype = int)
		est[:,1] = 1
		est[1,:] = 1
		I = cierre(I, est)
		self.imagenes[self.focus].image = I
		self.imagenes[self.focus].mostrarImagen()	

	def apertura_click(self):
		self.imagenes[self.focus].images.append(self.imagenes[self.focus].image)
		I = self.imagenes[self.focus].image
		est = np.zeros((3,3), dtype = int)
		est[:,1] = 1
		est[1,:] = 1
		I = apertura(I, est)
		self.imagenes[self.focus].image = I
		self.imagenes[self.focus].mostrarImagen()	
		

	############################################################################
	# Elementos del WidgetUmbral
	############################################################################

	def umbralManual(self):
		# Activa la Slider y fija el umbral en "manual"
		self.widgetUmbral.umbralSlider.setEnabled(True)
		self.tipoUmbral = "manual"

	def umbralManualSlider(self):
		# Define un umbral por medio de la Slider
		self.umbral = self.widgetUmbral.umbralSlider.value()*255/100
		self.widgetUmbral.sValue.setText(str(self.umbral))

	def umbralMedia(self):
		# Desactiva la Slider y fija el umbral en "media"
		self.widgetUmbral.umbralSlider.setEnabled(False)
		self.tipoUmbral = "media"

	def umbralMediana(self):
		# Desactiva la Slider y fija el umbral en "mediana"
		self.widgetUmbral.umbralSlider.setEnabled(False)
		self.tipoUmbral = "mediana"

	def umbralModa(self):
		# Desactiva la Slider y fija el umbral en "moda"
		self.widgetUmbral.umbralSlider.setEnabled(False)
		self.tipoUmbral = "moda"

	def umbralAplicar(self):
		# Aplica la umbralización según el radioButton elegido

		# umbralizar en el backend
		I = Image.fromarray(self.imagenes[self.focus].image)
		Ig = grises(I)

		# switch tipo umbral, se define el umbral con las funciones adecuadas
		if self.tipoUmbral == "manual":
			None
		elif self.tipoUmbral == "media":
			self.umbral = int(Ig.mean())
		elif self.tipoUmbral == "mediana":
			self.umbral = mediana(Ig)
		elif self.tipoUmbral == "moda":
			self.umbral = moda(Ig)

		# Se aplica la umbralización
		inv = self.widgetUmbral.invertir.checkState()
		gris = self.widgetUmbral.grises.checkState()
		self.IUmbral = umbralBinario(Ig,self.umbral,inv, gris)
				
		# Presenta la imagen umbralizada, frontend
		self.imagenes[self.focus].mostrarImagen(self.IUmbral)

	def umbralAceptar(self):
		# Agrega "_umbral" al nombre de ImagenWidget y cierra el widgetumbral
		# Se guarda la imagen umbralizada en ImageWidget.image
		self.imagenes[self.focus].image = self.IUmbral
		self.imagenes[self.focus].nombre = self.imagenes[self.focus].nombre+'_umbral'
		self.widgetUmbral.close()

	def umbralCancelar(self):
		# Recupera el estado inicial del ImagenWidget (image, images[]) 
		self.imagenes[self.focus].image = self.imagenes[self.focus].images.pop()

		# Despliega la imagen anterior a la umbralización y cierra el widgetUmbral
		self.imagenes[self.focus].mostrarImagen()
		self.widgetUmbral.close()

	###############################################################################	
	# Elementos del Widget Multiumbral
	###############################################################################

	def multiActivar3(self):
		if self.widgetUmbral.activar3.isChecked():
			self.widgetUmbral.vs3.setEnabled(True)
			self.widgetUmbral.grises3.setEnabled(True)
		else:
			self.widgetUmbral.vs3.setEnabled(False)
			self.widgetUmbral.grises3.setEnabled(False)

	def vs1_change(self):
		self.umbral1 = self.widgetUmbral.vs1.value()*255/100
		self.widgetUmbral.labelvs1.setText(str(self.umbral1))

	def vs2_change(self):
		self.umbral2 = self.widgetUmbral.vs2.value()*255/100
		self.widgetUmbral.labelvs2.setText(str(self.umbral2))

	umbral3 = 0
	def vs3_change(self):
		self.umbral3 = self.widgetUmbral.vs3.value()*255/100
		self.widgetUmbral.labelvs3.setText(str(self.umbral3))

	def multiAplicar(self):
		if self.widgetUmbral.activar3.isChecked():
			umbrales = [self.umbral1, self.umbral2, self.umbral3]
		else:
			umbrales = [self.umbral1, self.umbral2]
		I = Image.fromarray(self.imagenes[self.focus].image)
		Ig = grises(I)
		inv = self.widgetUmbral.invertir.isChecked()
		gris1 = self.widgetUmbral.grises1.isChecked()
		gris2 = self.widgetUmbral.grises2.isChecked()
		gris3 = self.widgetUmbral.grises3.isChecked()
		gris = [gris1, gris2, gris3]
		Iumbral = umbralesBinarios(Ig, umbrales, gris, inv)
		self.imagenes[self.focus].mostrarImagen(Iumbral)

	def multiAceptar(self):
		self.imagenes[self.focus].image = self.IUmbral
		self.imagenes[self.focus].nombre = self.imagenes[self.focus].nombre+'_umbral'
		self.widgetUmbral.close()

	def multiCancelar(self):
		self.imagenes[self.focus].image = self.imagenes[self.focus].images.pop()
		self.imagenes[self.focus].mostrarImagen()
		self.widgetUmbral.close()

	###############################################################################
	# Elementos del Widget Canal
	###############################################################################

	def canalAplicar(self):
		# Switch de que canal escoger
		if self.widgetCanal.cian.isChecked():
			canal = 0
		elif self.widgetCanal.magenta.isChecked():
			canal = 1
		elif self.widgetCanal.amarillo.isChecked():
			canal = 2
		elif self.widgetCanal.rojo.isChecked():
			canal = 3
		elif self.widgetCanal.verde.isChecked():
			canal = 4
		else:
			canal = 5

		# se obtiene el canal y se despliega
		self.imagen = RGB(self.imagenes[self.focus].image, canal)	
		self.imagenes[self.focus].mostrarImagen(self.imagen)
		
	def canalAceptar(self):
		# Agrega "_RGB" al nombre de ImagenWidget y cierra el widgetCanal
		# Se guarda la imagen del canal en ImageWidget.image
		self.imagenes[self.focus].image = self.imagen
		self.imagenes[self.focus].nombre = self.imagenes[self.focus].nombre+"_RGB"
		self.widgetCanal.close()

	def canalCancelar(self):
		# Recupera el estado inicial del ImagenWidget (image, images[]) 
		self.imagenes[self.focus].image = self.imagenes[self.focus].images.pop()

		# Despliega la imagen anterior a la umbralización y cierra el widgetUmbral
		self.imagenes[self.focus].mostrarImagen()
		self.widgetUmbral.close()

	#################################################################################
	# Elementos del Widget Operación Puntual
	#################################################################################

	def opAplicar(self):
		# Aplica la operación puntual en self.op y muestra el resultado
		
		# LLena el combobox de imagenes
		for ventana in self.imagenes:
			if ventana.nombre == self.WidgetOperacionPuntual.cbVentanas.currentText():
				imagen2 = ventana.image
				break
		imagen1 = self.imagenes[self.focus].image
		if self.op == "suma":
			self.imagenNueva = suma2(imagen1, imagen2)
		elif self.op == "resta":
			self.imagenNueva = resta(imagen1,imagen2)
		elif self.op == "multiplicación":
			self.imagenNueva = mult(imagen1, imagen2)
		elif self.op == "and":
			self.imagenNueva = lAnd1(imagen1, imagen2)
		elif self.op == "or":
			self.imagenNueva = lOr(imagen1, imagen2)
		elif self.op == "exor":
			self.imagenNueva = lExor(imagen1, imagen2)
		self.imagenes[self.focus].mostrarImagen(self.imagenNueva)

	def opAceptar(self):
		# Fija el resultado de la operación puntual
		self.imagenes[self.focus].image = self.imagenNueva
		self.imagenes[self.focus].nombre = self.imagenes[self.focus].nombre+"_"+self.op		
		self.WidgetOperacionPuntual.close()

	def opCancelar(self):
		# Cancela operación puntual
		self.imagenes[self.focus].image = self.imagenes[self.focus].images.pop()
		self.imagenes[self.focus].mostrarImagen()
		self.WidgetOperacionPuntual.close()
		
	###############################################################################
	# Elementos del Widget Histograma
	###############################################################################

	def operacionesHistograma(self, title, limites=2):
		self.histOp = title
		self.widgetHist = uic.loadUi("Histograma.ui")
		self.widgetHist.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
		self.widgetHist.setWindowTitle(title)
		self.widgetHist.show()
		if limites == 1:		#Caso desplazar histograma
			self.widgetHist.label_li.setVisible(False)
			self.widgetHist.label_ls.setText("Desplazamiento:")
			self.widgetHist.line_li.setVisible(False)
		elif limites == 0:
			self.widgetHist.label_li.setVisible(False)
			self.widgetHist.label_ls.setVisible(False)
			self.widgetHist.line_li.setVisible(False)
			self.widgetHist.line_ls.setVisible(False)	
		self.widgetHist.aplicar.clicked.connect(self.histAplicar)
		self.widgetHist.aceptar.clicked.connect(self.histAceptar)
		self.widgetHist.cancelar.clicked.connect(self.histCancelar)

	def histAplicar(self):
		gh = self.widgetHist.graficar.isChecked()
		if self.histOp == 'Expandir Histograma':
			li = int(self.widgetHist.line_li.text())
			lf = int(self.widgetHist.line_ls.text())
			I = expandirHistograma(self.imagenes[self.focus].image, li, lf, gh)
			self.imagenes[self.focus].mostrarImagen(I)
		elif self.histOp == 'Contraer Histograma':
			li = int(self.widgetHist.line_li.text())
			lf = int(self.widgetHist.line_ls.text())
			I = contraerHistograma(self.imagenes[self.focus].image, li, lf, gh)
			self.imagenes[self.focus].mostrarImagen(I)
		elif self.histOp == 'Desplazar Histograma':
			li = int(self.widgetHist.line_ls.text())
			I = desplazarHistograma(self.imagenes[self.focus].image, li, gh)
			self.imagenes[self.focus].mostrarImagen(I)	
		else:
			I = ecualizarHistograma(self.imagenes[self.focus].image, gh)
			self.imagenes[self.focus].mostrarImagen(I)
		self.imagenNueva = I

	def histAceptar(self):
		self.imagenes[self.focus].image = self.imagenNueva
		self.imagenes[self.focus].nombre = self.imagenes[self.focus].nombre+"_"+self.histOp		
		self.widgetHist.close()
		
	def histCancelar(self):
		self.imagenes[self.focus].image = self.imagenes[self.focus].images.pop()
		self.imagenes[self.focus].mostrarImagen()
		self.widgetHist.close()

	###############################################################################
	# Elementos de WidgetFiltro
	###############################################################################

	def filtroAplicar(self):
		N = self.WidgetFiltro.lineEdit.displayText()
		I = self.imagenes[self.focus].image
		if self.filtro == 'promedio':
			I = filtroPromedio(I, int(N))
		elif self.filtro == 'gausiano':
			I = filtroGausiano1(I, int(N))
		elif self.filtro == 'laplaciano':
			I = filtroLaplaciano(I, int(N))
		self.imagenes[self.focus].mostrarImagen(I)
		self.imagenNueva = I

	def filtroAceptar(self):
		self.imagenes[self.focus].image = self.imagenNueva
		self.imagenes[self.focus].nombre = self.imagenes[self.focus].nombre+"_fProm"		
		self.WidgetFiltro.close()

	def filtroCancelar(self):
		self.imagenes[self.focus].image = self.imagenes[self.focus].images.pop()
		self.imagenes[self.focus].mostrarImagen()
		self.WidgetFiltro.close()

	###############################################################################
	# Elementos de WidgetPasabanda
	###############################################################################

	def pasabandaAplicar(self):
		I = self.imagenes[self.focus].image
		if self.widgetPasabanda.mediana.isChecked():
			I = filtroMediana(I)
		elif self.widgetPasabanda.moda.isChecked():
			I = filtroModa(I)
		elif self.widgetPasabanda.min.isChecked():
			I = filtroMin(I)
		elif self.widgetPasabanda.max.isChecked():
			I = filtroMax(I)
		self.imagenes[self.focus].mostrarImagen(I)
		self.imagenNueva = I

	def pasabandaAceptar(self):
		self.imagenes[self.focus].image = self.imagenNueva
		self.imagenes[self.focus].nombre = self.imagenes[self.focus].nombre+"_fProm"		
		self.WidgetFiltro.close()

	def pasabandaCancelar(self):
		self.imagenes[self.focus].image = self.imagenes[self.focus].images.pop()
		self.imagenes[self.focus].mostrarImagen()
		self.WidgetFiltro.close()

	###############################################################################
	# funciones auxiliares
	###############################################################################

	def operacionesPuntuales(self):
		self.statusBar().showMessage('"{}" Modo Operaciones Puntuales'.format(self.imagenes[self.focus].nombre, 5000))

		# Carga un Widget con una lista de las imagenes abiertas, 
		self.WidgetOperacionPuntual = uic.loadUi("operacionPuntual.ui")
		self.WidgetOperacionPuntual.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)

		# Rellenamos combobox, excluyendo la imagen enfocada
		for ventana in self.imagenes:
			if ventana is not self.imagenes[self.focus]:
				self.WidgetOperacionPuntual.cbVentanas.addItem(ventana.nombre)

		# Conectamos los botones aplicar, aceptar y cancelar
		self.WidgetOperacionPuntual.aplicar.clicked.connect(self.opAplicar)
		self.WidgetOperacionPuntual.aceptar.clicked.connect(self.opAceptar)
		self.WidgetOperacionPuntual.cancelar.clicked.connect(self.opCancelar)

		self.WidgetOperacionPuntual.show()


	def imagenActiva(self):
		for ventana in self.imagenes:
			print(ventana.hasFocus())

	def aumentarXY(self):
		if self.y < 180:
			self.x += 30
			self.y += 30
		elif self.x < 360:
			self.x += 30
			self.y = 0
		else:
			self.x = 0
			self.y = 0

	@pyqtSlot(int)
	def imagen_focus(self,index):
		"""
		Método que se conecta a la señal fosucSignal
		Args:
			index: Recibe el índice de la imagen que emite la señal
		"""

		#print('todo funciona :v %s'% index)
		self.focus = index

################ Main de la app ######################################################

def main():

	app = QtGui.QApplication(sys.argv)
	mv = VentanaP()
	mv.show()
	mv.move(20,20)

	sys.exit(app.exec_())


if __name__ == '__main__':
    main()

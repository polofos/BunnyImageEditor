# Coding utf-8

import os
import sys
from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSlot

aplicacion = QtGui.QApplication(sys.argv)

class VentanaP(QtGui.QMainWindow):
	def __init__(self, padre=None):
		super(VentanaP, self).__init__(padre)
		icono_abrir = QtGui.QIcon(os.path.join('iconos', 'folder_add.png'))
		icono_guardar = QtGui.QIcon(os.path.join('iconos', 'Actions-document-save-icon.png'))

		# acción abrir
		accion_abrir = QtGui.QAction(icono_abrir, 'Abrir', self)
		accion_abrir.setShortcuts(QtGui.QKeySequence.Open)
		accion_abrir.setStatusTip('Abrir archivo')  # mensaje temporal
		accion_abrir.triggered.connect(self.abrir_archivo)  # signal triggered
		
		# acción guardar
		accion_guardar = QtGui.QAction(icono_guardar, 'Guardar', self)
		accion_guardar.setShortcuts(QtGui.QKeySequence.Save)
		accion_guardar.setStatusTip('Guardar archivo')  # mensaje temporal
		accion_guardar.triggered.connect(self.guardar)  # signal triggered
		
		# barra de herramientas
		barra_de_herramientas = QtGui.QToolBar()
		barra_de_herramientas.addAction(accion_abrir)
		barra_de_herramientas.addAction(accion_guardar)
		self.addToolBar(barra_de_herramientas)

		# barra de estado
		self.statusBar()

	# slot abrir archivo
	@pyqtSlot()
	def abrir_archivo(self):
		# si el usuario presiona Cancelar, retorna una cadena de texto vacía
		ruta = QtGui.QFileDialog.getOpenFileName(self, 'Abrir archivo')
		if ruta != '':
			self.statusBar().showMessage('"{}" archivo abierto'.format(ruta), 5000)  # muestra un mensaje por 5 segundos

	@pyqtSlot()
	def guardar(self):
		# si el usuario presiona Cancelar, retorna una cadena de texto vacía
		ruta = QtGui.QFileDialog.getSaveFileName(self, caption='Guardar archivo', filter='Imágenes (*.png)')
		if ruta!= '':
			self.statusBar().showMessage('"{}" archivo guardado'.format(ruta), 5000)



ventanaP = VentanaP()
ventanaP.setWindowTitle("App Analisis de imágenes")
ventanaP.resize(900,700)
ventanaP.move(200,100)
ventanaP.show()

sys.exit(aplicacion.exec_())

#Coding utf-8

import sys
from PyQt4 import QtGui

#Crea la aplicación
aplicacion = QtGui.QApplication(sys.argv)

# crea la ventana y establece sus propiedades

class Ventana(QtGui.QWidget):
	def __init__(self,padre=None):
		super(Ventana,self).__init__(padre)

	def crearVentanaHija(self):
		# ventana hija
		self.ventana_hija = Ventana()
		self.ventana_hija.setWindowTitle('Ventana hija')
		self.ventana_hija.resize(240, 200)

		# botón abrir ventana
		boton_abrir_ventana = QtGui.QPushButton('Abrir ventana')
		boton_abrir_ventana.clicked.connect(self.ventana_hija.show)  # signal clicked

		# botón cerrar ventana
		boton_cerrar_ventana = QtGui.QPushButton('Cerrar ventana')
		boton_cerrar_ventana.clicked.connect(self.ventana_hija.close)  # signal clicked

		# vertical box layout
		vlayout = QtGui.QVBoxLayout()
		vlayout.addStretch()
		vlayout.addWidget(boton_abrir_ventana)
		vlayout.addWidget(boton_cerrar_ventana)
		vlayout.addStretch()
		self.setLayout(vlayout)
"""
	def closeEvent(self, evento):
		# cierra su ventana hija
		self.ventana_hija.close()
"""
ventana = Ventana()
ventana.setWindowTitle('App Imagenes')  # titulo
ventana.resize(920, 750)  # tamanyo
ventana.move(200, 100)  # posición
ventana.show()  # muestra la ventana
ventana.crearVentanaHija()

# ejecuta la aplicación y espera su valor de retorno al finalizar
sys.exit(aplicacion.exec_())
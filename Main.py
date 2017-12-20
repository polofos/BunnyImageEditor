#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
Primera ventana con PyQt4


"""
from scipy import misc
import matplotlib.pyplot as plt
from PIL import Image
import sys
sys.path.append("..")
import os
from PyQt4 import QtGui, QtCore, uic
from Umbralizacion import UmbralBin, Grises

# Carga de ui en qt
claseQT = uic.loadUiType("MainW.ui")[0]

"""
Autor: fosykun
App para analisis de imagenes
con PyQt
"""

#	Clasede la ventana principal
class MiVentana(QtGui.QMainWindow, claseQT):
	#	Datos de la imagen
	ruta = ""
	archivo = ""
	imagen = []

	#	Constructor
	#	Aqui se enlazan los botones con sus funciones
	#	mediante el metodo connect
	def __init__(self, parent=None):
  		QtGui.QMainWindow.__init__(self, parent)
  		self.setupUi(self)
  		self.abrir.clicked.connect(self.abrir_click)
  		self.guardar.clicked.connect(self.guardar_click)
  		self.cerrar.clicked.connect(self.cerrar_click)
  		self.umbral.clicked.connect(self.umbral_click)
  	
  	#	Boton abrir, abre una imagen
  	def abrir_click(self):
		nombre_archivo = QtGui.QFileDialog.getOpenFileName(self, "Abrir fichero", self.ruta)
		if nombre_archivo:
			self.archivo = nombre_archivo
			self.setWindowTitle(QtCore.QFileInfo(nombre_archivo).fileName())
			self.ruta = QtCore.QFileInfo(nombre_archivo).path()
			self.ruta_label.setText(self.archivo)
			pic = QtGui.QLabel(self)
			pic.setPixmap(QtGui.QPixmap(self.archivo))
			self.scrollArea1.setWidget(pic)
			pic.show()
			self.imagen = misc.imread(str(self.archivo))
			#plt.imshow(self.imagen)
			#plt.show()


	#	Boton guardar
	#	Guarda la imagen examinada en el sistema de archivos
	def guardar_click(self):
		nombre_guardar = str(QtGui.QFileDialog.getSaveFileName(self, "Guardar Archivo", ".png", ".png"))
		if nombre_guardar:
			misc.imsave(nombre_guardar, self.imagen)
	#	Boton cerrar
	#	Cierra la imagen y borra sus datos
	def cerrar_click(self):
		pic = QtGui.QLabel(self)
		self.scrollArea1.setWidget(pic)
		self.ruta = ""
		self.archivo = ""
		self.imagen = []

	#	Boton umbral
	#	Abre un diálogo para ingresar datos y realizar una umbralización
	def umbral_click(self):
		I = Image.fromarray(self.imagen)
		Igris = Grises(I)
		Im = UmbralBin(Igris,100)
		#plt.imshow(Im, cmap='gray')
		#plt.show()
		#r,c = Im.shape
		#QIm = 	QtGui.QImage(Im,r, c,QtGui.QImage.Format_Indexed8)
		misc.imsave("Temp.tiff", Im)
		pic = QtGui.QLabel(self)
		pic.setPixmap(QtGui.QPixmap("Temp.tiff"))
		self.scrollArea2.setWidget(pic)
		pic.show()





 

################ Main de la app ###################################

def main():

	app = QtGui.QApplication(sys.argv)
	mv = MiVentana()
	mv.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
    main()


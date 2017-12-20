import numpy as np
from PIL import Image, ImageChops

def RGB(I, color):
	""" Regresa una imagen en rojo,azul o verde
	Args:
		I 		: Imagen np.ndarray en 3 canales
		color 	: clave para indicar el color a convertir
			1 : Rojo
			2 : Verde
			3 : Azul
	return:
		Icanal  : Imagen ndarray en el color indicado
	"""
	Icanal = I.copy()
	if color < 3:
		Icanal[:,:,color]=0
	elif color == 3:
		Icanal[:,:,1]=0
		Icanal[:,:,2]=0
	elif color == 4:
		Icanal[:,:,0]=0
		Icanal[:,:,2]=0
	elif color == 5:
		Icanal[:,:,0]=0
		Icanal[:,:,1]=0
	else:
		None
	return Icanal

def suma(I1, I2):
	""" Regresa una imagen con la suma aritmética de dos imagenes
	Args: 
		I1		: Primera imagen a sumar
		I2		: Segunda imagen a sumar
	return: Imagen suma de las dos entradas
	"""
	x1,y1,z1 = I1.shape
	x2,y2,z2 = I2.shape
	Im2 = Image.fromarray(I2)
	resolution = (x1,y1)
	scaler = Image.ANTIALIAS
	Im2 = Im2.resize(resolution, scaler)
	I2 = np.asarray(Im2)
	Isuma = I1.copy()
	for z in range(0,z1):
		I1c = np.matrix(I1[:,:,z])
		I2c = np.matrix(I2[:,:,z])

		Isuma[:,:,z] = I1c + I2c
	return Isuma

def suma2(I1, I2):
	x1,y1,z1 = I1.shape
	size = (x1,y1)
	Im1 = Image.fromarray(I1)
	Im2 = Image.fromarray(I2)
	Im2 = Im2.resize(size)
	return np.asarray(ImageChops.add(Im1,Im2,2))

def resta(I1,I2):
	x1,y1,z1 = I1.shape
	size = (x1,y1)
	Im1 = Image.fromarray(I1)
	Im2 = Image.fromarray(I2)
	Im2 = Im2.resize(size)
	return np.asarray(ImageChops.subtract(Im1,Im2,0.5))


def resta1(I1,I2):
	x1,y1 = I1.shape
	size = (x1,y1)
	Im1 = Image.fromarray(I1)
	Im2 = Image.fromarray(I2)
	Im2 = Im2.resize(size)
	return np.asarray(ImageChops.subtract(Im1,Im2,0.5))


def mult(I1, I2):
	x1,y1,z1 = I1.shape
	size = (x1,y1)
	Im1 = Image.fromarray(I1)
	Im2 = Image.fromarray(I2)
	Im2 = Im2.resize(size)
	return np.asarray(ImageChops.multiply(Im1,Im2))

def lAnd(I1,I2):
	x1,y1,z1 = I1.shape
	size = (x1,y1)
	Im1 = Image.fromarray(I1)
	Im2 = Image.fromarray(I2)
	Im2 = Im2.resize(size)
	print(Im1.mode)
	print(Im2.mode)
	return np.asarray(ImageChops.logical_and(Im1,Im2))

def lAnd1(I1, I2):
	x1,y1 = I1.shape
	size = (x1,y1)
	Im2 = Image.fromarray(I2)
	Im2 = Im2.resize(size)
	I2 = np.asarray(Im2)
	I2.setflags(write=1)
	# print(I2.flags)
	for i in range(0,x1):
		for j in range(0,y1):
			if I1[i,j] == 0:
				I2[i,j,0]=0
				I2[i,j,1]=0
				I2[i,j,2]=0					
	return I2



def lOr(I1,I2):
	x1,y1 = I1.shape
	size = (x1,y1)
	Im1 = Image.fromarray(I1)
	Im2 = Image.fromarray(I2)
	Im2 = Im2.resize(size)
	Im1 = Im1.convert('1')
	Im2 = Im2.convert('1')
	Im1 = ImageChops.logical_or(Im1,Im2)
	return np.asarray(Im1.convert('L'))

def lExor(I1,I2):
	x1,y1 = I1.shape
	size = (x1,y1)
	Im1 = Image.fromarray(I1)
	Im2 = Image.fromarray(I2)
	Im2 = Im2.resize(size)
	Im1 = Im1.convert('1')
	Im2 = Im2.convert('1')
	Im3 = ImageChops.logical_and(Im1, Im2)
	Im4 = ImageChops.logical_or(Im1, Im2)
	Im5 = ImageChops.invert(Im3)
	Im3 = ImageChops.logical_and(Im4,Im5)
	return np.asarray(Im3.convert('L'))


	return np.asarray(ImageChops.multiply(Im1,Im2))

def lNot(I1):
	Im1 = Image.fromarray(I1)
	return np.asarray(ImageChops.invert(Im1))
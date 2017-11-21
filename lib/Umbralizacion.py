import numpy as np
from matplotlib.pylab import plot, hist, show 
import matplotlib.pyplot as plt
from scipy import ndimage, misc
from PIL import Image 

def pruebaUmbral():
	# Convierte a gris, imprime datos y la imagen con Image
	I = Image.open('NSQ1.jpg')
	Igris = I.convert('L')
	# print(Igris.size, Igris.mode, Igris.format)
	Igris.show()
	# A partir de la Image, obtiene un arreglo uint8 y lo imprime
	Im = np.asarray(Igris, dtype=np.uint8) 
	plt.imshow(Im, cmap='gray')
	plt.show()

def moda(I):
	""" Regresa un numero entero con la primer moda de una imagen
	Args:
		I 	: Imagen np.array en escala de grises
	return:
		moda: Entero con la primer moda de la imagen I
	"""
	dic = dict()
	m, n = I.shape
	for row in range(0,m):
		for col in range(0,n):
			if I[row,col] in list(dic.keys()):
				dic[I[row,col]] =  dic[I[row,col]] + 1
			else:
				dic[I[row,col]] = 1
	index = np.argmax(list(dic.values()))
	moda = list(dic.keys())[index]
	return moda

def mediana(I):
	""" Regresa un numero entero con la mediana superior de una imagen
	Args:
		I 		: Imagen no.array en escala de grises
	return:
		mediana	: Entero con la mediana de la imagen I
	"""
	lista = []
	m, n = I.shape
	for row in range(0,m):
		for col in range(0,n):
			if I[row,col] in lista:
				None
			else:
				lista.append(I[row,col])
	lista = sorted(lista)
	n = len(lista)
	index = int(n/2)
	mediana = lista[index]
	return mediana


def umbralBinario(I, u, inv=0):
	""" Funcion que recibe una imagen en grises y un umbral int
	Args:
		I 	: Imagen np.array en escala de grises
		u 	: Umbral int
		inv : Binarizacion invertida con =1
	return:
		Ib: Imagen binaria umbralizada
	"""
	r, c = I.shape
	I2 = I.copy()
	if inv:
		piso = 255
		techo = 0
	else:
		piso = 0
		techo = 255
	for i in range(0,r):
		for j in range(0,c):
			if I[i,j] <= u:
				I2[i,j] = piso

			else:
				I2[i,j] = techo
	return I2

def umbralesBinarios(I, u, bina=0, inv=0):
	""" Funcion que recibe ,una imagen en grises y varios umbrales int[]
	Args:
		I 	: Imagen np.array en escala de grises
		u 	: Umbrales int[]
		inv : Umbralizacion invertida = 1
		bin : binario:
			- 0: bin,bin,bin
			- 1: bin,ran,bin
			- 2: ran,bin,ran PENDIENTE
			- 3: ran,ran,ran PENDIENTE
	"""
	r, c = I.shape
	I2 = I.copy()
	if bina == 0:
		# bin,bin,bin
		for i in range(0,r):
			for j in range(0,c):
				if inv:
					I2[i,j] = 255
				else:
					I2[i,j] = 0
		for um in u:
			for i in range(0,r): 
				for j in range(0,c):
					if I[i,j] > um:
						I2[i,j] = um
		for i in range(0,r):
			for j in range(0,c):
				if I[i,j] > um:
					if inv:
						I2[i,j] = 0
					else:
						I2[i,j] = 255
	elif bina == 1:
		# bin,ran,bin
		for i in range(0,r):
			for j in range(0,c):
				if inv:
						I2[i,j] = 255
				else:
						I2[i,j] = 0
		for um in u:
			for i in range(0,r): 
				for j in range(0,c):
					if I[i,j] > um:
						I2[i,j] = I[i,j]
			#plt.imshow(I2)
			#plt.show()
		for i in range(0,r):
			for j in range(0,c):
				if I[i,j] > um:
					if inv:
						I2[i,j] = 0
					else:
						I2[i,j] = 255

	return I2




def grises(I,p = 0):
	""" Funcion que recibe una imagen en 3 canales y devuelve
	una imagen en escala de grises. 
	Tambien imprime la imagen en gris si p = 1
	Args:
		I : Imagen abierta con PIL [Image.open('')]
		p : Opcional, 1 para imprimir la imagen
	return:
		Imagen np.array en escalade grises [np.asarray()]
	"""
	Igris = I.convert('L')
	Im = np.asarray(Igris, dtype=np.uint8)
	if p:
		plt.imshow(Im, cmap='gray')
		plt.show()
	return Im

"""
I = [[5,6,6,6,6],
	[1,2,3,4,5],
	[2,3,4,5,6],
	[5,4,3,2,1]]
I = np.array(I)
print(mediana(I))

I = Image.open('NSQ1.jpg')
Im = Grises(I)
f,axarr = plt.subplots(1,3)
axarr[0].imshow(I)
axarr[0].set_title("Original")
# Impresion de imagenes UmbralBin

I1 = UmbralBin(Im, 100)
I2 = UmbralBin(Im,100,1)

axarr[1].imshow(I1)
axarr[1].set_title("Binarizada")
axarr[2].imshow(I2)
axarr[2].set_title("Bin Inversa")


# Impresion de imagenes UmbralSeg

I3 = UmbralSeg(Im, [50,70,120])
axarr[1].imshow(I3, cmap="gray")
axarr[1].set_title("doble umbral gris")

I4 = UmbralSeg(Im,[50,120],1)
axarr[2].imshow(I4, cmap="gray")
axarr[2].set_title("doble umbral")

plt.show()
"""
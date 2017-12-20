import numpy as np
from matplotlib.pylab import plot, hist, show 
import matplotlib.pyplot as plt
from scipy import ndimage
from OperacionesBasicas import resta1 

def erosion(Im, estructura):
	#est = np.zeros((3,3), dtype = np.int)
	#est[:,1] = 1
	#est[1,:] = 1
	#print est
	Im = ndimage.binary_erosion(Im,estructura).astype('uint8')
	return Im

def dilatacion(Im, estructura):
	#est = np.zeros((3,3), dtype = np.int)
	#est[:,1] = 1
	#est[1,:] = 1
	Im = ndimage.binary_dilation(Im,estructura).astype('uint8')
	return Im 

def cierre(Im, estructura):
	# Primero dilatación, luego erosión
	Im = ndimage.grey_closing(Im, structure = estructura).astype(np.uint8)
	return Im	

def apertura(Im, estructura):
	# Primero erosión, luego dilatación
	Im = ndimage.grey_opening(Im, structure = estructura).astype(np.uint8)
	return Im 

def cercoConvexo(Im, estructura):
	Im2 = ndimage.grey_dilation(Im, structure = estructura).astype(np.uint8)
	Im3 = resta1(Im2,Im)
	return Im3  

"""
def pruebaErosion():

	M = np.zeros((30,30), dtype = np.int)
	m = np.matrix(M)

	est1 = ndimage.generate_binary_structure(2,1)
	#print est1

	est2 = np.zeros((7,7), dtype = np.int)
	#print est2

	est2[:,2:5] = 1
	est2[2:5,:] = 1
	
	print "Estructura de erosion"
	print est2
	print ""

	m[5:15,5:15] = 1
	m[5:18,15:25] = 1
	m[8:11,15] = 0
	m[18:30,10:19] = 1
	m[18:28,20:28] = 1
	print "Original"
	print m
	print " "

	plt.imshow(m)
	plt.show()
	
	print "Erosionada"
	m1 = ndimage.binary_erosion(m,est2).astype(np.int)
	print m1
	print " "

	plt.imshow(m1)
	plt.show()

	return m1, est2

def pruebaDilatacion(M, est):

	est[0,:] = 0
	est[6,:] = 0
	est[:,0] = 0
	est[:,6] = 0
	print "Estructura de dilatacion"
	print est
	print ""


	print "Dilatada"
	#print ndimage.binary_erosion(m,est2).astype(np.int)
	m1 = ndimage.binary_dilation(M, structure=est).astype(np.int)
	plt.imshow(m1)
	plt.show()


################ Main de la app ###################################

def main():
	
	M, est = pruebaErosion()
	pruebaDilatacion(M, est)


if __name__ == '__main__':
    main()

 """


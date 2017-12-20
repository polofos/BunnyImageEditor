import numpy as np
from scipy import misc, ndimage
from PIL import Image
from Umbralizacion import moda

def filtroPromedio(I,N=1):
	If = I.copy()
	Ir = If[:,:,0]
	Iv = If[:,:,1]
	Ia = If[:,:,2]
	k = [[1,1,1],
		[1,N,1],
		[1,1,1]]
	K = np.matrix(k)/(N+8)
	Ir = ndimage.convolve(Ir, K, mode='constant')
	Iv = ndimage.convolve(Iv, K, mode='constant')
	Ia = ndimage.convolve(Ia, K, mode='constant')
	If[:,:,0] = Ir 
	If[:,:,1] = Iv 
	If[:,:,2] = Ia 	
	return If	

def filtroGausiano(I):
	If = I.copy()
	Ir = If[:,:,0]
	Iv = If[:,:,1]
	Ia = If[:,:,2]
	k = [[1,2,1],
		[2,4,2],
		[1,2,1]]
	K = np.matrix(k)/(16)
	Ir = ndimage.convolve(Ir, K, mode='constant')
	Iv = ndimage.convolve(Iv, K, mode='constant')
	Ia = ndimage.convolve(Ia, K, mode='constant')
	If[:,:,0] = Ir 
	If[:,:,1] = Iv 
	If[:,:,2] = Ia 
	return If

def filtroGausiano1(I, s):
	If = I.copy()
	Ir = If[:,:,0]
	Iv = If[:,:,1]
	Ia = If[:,:,2]
	Ir = ndimage.gaussian_filter(Ir, s)
	Iv = ndimage.gaussian_filter(Iv, s)
	Ia = ndimage.gaussian_filter(Ia, s)
	If[:,:,0] = Ir 
	If[:,:,1] = Iv 
	If[:,:,2] = Ia 
	return If

def filtroSobel(I):
	If = I.copy()
	Ir = If[:,:,0]
	Iv = If[:,:,1]
	Ia = If[:,:,2]
	Ir = canalSobel(Ir)
	Iv = canalSobel(Iv)
	Ia = canalSobel(Ia)
	If[:,:,0] = Ir 
	If[:,:,1] = Iv 
	If[:,:,2] = Ia
	return If

def canalSobel(canal):
	m, n = canal.shape
	canal1 = canal.copy()
	for x in range(2,m-1):
		for y in range(2,n-1):
			canalx = (abs(-int(canal[x-1,y-1])-int(canal[x,y-1])-int(canal[x+1,y-1])
				+int(canal[x-1,y+1])+int(canal[x,y+1])+int(canal[x+1,y+1])))
			canaly = (abs(-int(canal[x-1,y-1])-int(canal[x-1,y])-int(canal[x-1,y+1])
				+int(canal[x+1,y-1])+int(canal[x+1,y])+int(canal[x+1,y+1])))
			canal1[x,y] = np.hypot(canalx, canaly)
	return canal1

def filtroLaplaciano(I, s):
	If = I.copy()
	Ir = If[:,:,0]
	Iv = If[:,:,1]
	Ia = If[:,:,2]
	Ir = ndimage.gaussian_laplace(Ir, s)
	Iv = ndimage.gaussian_laplace(Iv, s)
	Ia = ndimage.gaussian_laplace(Ia, s)
	If[:,:,0] = Ir 
	If[:,:,1] = Iv 
	If[:,:,2] = Ia 
	return If

def filtroPrewitt(I):
	If = I.copy()
	Ir = If[:,:,0]
	Iv = If[:,:,1]
	Ia = If[:,:,2]
	Ir = canalPrewitt(Ir)
	Iv = canalPrewitt(Iv)
	Ia = canalPrewitt(Ia)
	If[:,:,0] = Ir 
	If[:,:,1] = Iv 
	If[:,:,2] = Ia 
	return If

def canalPrewitt(canal):
	m, n = canal.shape
	canal1 = canal.copy()
	for x in range(1,m-1):
		for y in range(1,n-1):
			canalx = (abs(-int(canal[x-1,y-1])-2*int(canal[x,y-1])-int(canal[x+1,y-1])
				+int(canal[x-1,y+1])+2*int(canal[x,y+1])+int(canal[x+1,y+1])))
			canaly = (abs(-int(canal[x-1,y-1])-2*int(canal[x-1,y])-int(canal[x-1,y+1])
				+int(canal[x+1,y-1])+2*int(canal[x+1,y])+int(canal[x+1,y+1])))
			canal1[x,y] = np.hypot(canalx, canaly)
	return canal1


def filtroRobert(I):
	If = I.copy()
	Ir = If[:,:,0]
	Iv = If[:,:,1]
	Ia = If[:,:,2]
	Ir = canalRobert(Ir)
	Iv = canalRobert(Ivr)
	Ia = canalRobert(Ia)
	If[:,:,0] = Ir 
	If[:,:,1] = Iv 
	If[:,:,2] = Ia 	
	return If

def canalRobert(canal):
	m, n = canal.shape
	for x in range(1,m-1):
		for y in range(1,n-1):
			canal[x,y] = abs(int(canal[x,y])-int(canal[x+1,y+1])) + abs(int(canal[x+1,y]) - int(canal[x,y+1]))
	return canal

def filtroModa(I):
	If = I.copy()
	Ir = If[:,:,0]
	Iv = If[:,:,1]
	Ia = If[:,:,2]
	Ir = canalModa(Ir)
	Iv = canalModa(Iv)
	Ia = canalModa(Ia)
	If[:,:,0] = Ir 
	If[:,:,1] = Iv 
	If[:,:,2] = Ia 
	return If	

def canalModa(canal):
	m, n = canal.shape
	canal1 = canal.copy()
	for x in range(1, m-1):
		for y in range(1, n-1):
			canal1[x,y] = moda(canal[x-1:x+1,y-1:y+1])
	return canal1

def filtroMediana(I):
	If = I.copy()
	Ir = If[:,:,0]
	Iv = If[:,:,1]
	Ia = If[:,:,2]
	Ir = ndimage.median_filter(Ir, 3)
	Iv = ndimage.median_filter(Iv, 3)
	Ia = ndimage.median_filter(Ia, 3)
	If[:,:,0] = Ir 
	If[:,:,1] = Iv 
	If[:,:,2] = Ia 
	return If	

def filtroMin(I):
	If = I.copy()
	Ir = If[:,:,0]
	Iv = If[:,:,1]
	Ia = If[:,:,2]
	Ir = ndimage.minimum_filter(Ir, 3)
	Iv = ndimage.minimum_filter(Iv, 3)
	Ia = ndimage.minimum_filter(Ia, 3)
	If[:,:,0] = Ir 
	If[:,:,1] = Iv 
	If[:,:,2] = Ia 
	return If	

def filtroMax(I):
	If = I.copy()
	Ir = If[:,:,0]
	Iv = If[:,:,1]
	Ia = If[:,:,2]
	Ir = ndimage.maximum_filter(Ir, 3)
	Iv = ndimage.maximum_filter(Iv, 3)
	Ia = ndimage.maximum_filter(Ia, 3)
	If[:,:,0] = Ir 
	If[:,:,1] = Iv 
	If[:,:,2] = Ia 
	return If	

"""
m = [[1,0,1,0,1],
	[0,1,0,1,0],
	[1,0,1,0,1],
	[0,1,0,1,0],
	[1,0,1,0,1]]
 
M = np.matrix(m)

n = [[1,0,1,1,0],
	[1,1,0,1,0],
	[1,1,1,0,1],
	[0,1,0,1,0],
	[1,0,1,0,1]]

N = np.matrix(n)

k = [[1,1,1],
	[1,1,1],
	[1,1,1]]

K = np.matrix(k)/9

N = ndimage.convolve(N, K, mode='constant', cval=0.0)
N = np.round(N)



print(N)
"""





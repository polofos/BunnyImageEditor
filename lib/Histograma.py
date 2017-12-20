from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


#############################################################################
# Presentar el histograma, con media, varianza y asimetría
############################################################################# 

def histograma(I):
	"""
	Procedimiento que presenta un histograma de los 3 canales
	args:
		I = Imagen RGB guardada en un np.ndarray
	"""
	datosRojo, mediaR, asimR, varR = datos(I[:,:,0])
	datosVerde, mediaV, asimV, varV = datos(I[:,:,1])
	datosAzul, mediaA, asimA, varA = datos(I[:,:,2])
	legendRojo = "Canal rojo, Media= "+str(mediaR)+", Asimetría= "+str(asimR)+", Varianza= "+str(varR)
	legendVerde = "Canal verde, Media= "+str(mediaV)+", Asimetría= "+str(asimV)+", Varianza= "+str(varV)
	legendAzul = "Canal azul, Media= "+str(mediaA)+", Asimetría= "+str(asimA)+", Varianza= "+str(varA)
	labels = [legendRojo, legendVerde, legendAzul]
	graficarHistograma(datosRojo, datosVerde, datosAzul, labels)

##########################################################################
# Expandir histograma de una imagen
##########################################################################

def expandirHistograma(I, r1, r2, hist=False):
	"""
	Función que expande el histograma de la imagen, del rango dado a 0 - 255
	presenta al usuario el histograma resultante
	args:
		I = Imagen RGB guardada en un np.ndarray
		r1 = limite inferior que se va a expandir
		r2 = límite superior que se va a expandir
	return:
		I = Imagen RGB en un np.ndarray que contiene la imagen con el histograma
			expandido
	"""
	Inueva = I.copy()
	coef = (255)/(r2-r1)
	canalRojo = expCanal(I[:,:,0], coef, r1)
	canalVerde = expCanal(I[:,:,1], coef, r1)
	canalAzul = expCanal(I[:,:,2], coef, r1)
	Inueva[:,:,0] = canalRojo
	Inueva[:,:,1] = canalVerde
	Inueva[:,:,2] = canalAzul
	if hist:
		dr = datos(canalRojo, False)
		dv = datos(canalVerde, False)
		da = datos(canalAzul, False)
		graficarHistograma(dr, dv, da)
	return Inueva

def expCanal(canal, coef, r1):
	"""
	Función que expande un canal de la imagen de r1-r2 a 1-255
	usando la ecuación (r - r1) * coef
	args: 
		canal:	np.ndarray 2x2 con un canal RGB de la imagen
		coef:	float con el coeficiente a multiplicar
		r1:		límite inferior utilizado en la ecuación
	return:
		canal: 	np.ndarray 2x2 con el canal con histoframa expandido
	"""
	x, y = canal.shape
	for xi in range(0,x):
		for yi in range(0,y):
			canal[xi,yi] = (canal[xi, yi] - r1)* coef
	return canal

############################################################################
# Contraer histograma de una imagen
############################################################################

def contraerHistograma(I, r1, r2, hist=False):
	"""
	Función que contrae el histograma de la imagen, del 0 - 255 al rango dado
	presenta al usuario el histograma resultante
	args:
		I = Imagen RGB guardada en un np.ndarray
		r1 = limite inferior al que se va a contraer
		r2 = límite superior al que se va a contraer
	return:
		I = Imagen RGB en un np.ndarray que contiene la imagen con el histograma
			contraido
	"""
	Inueva = I.copy()
	coef = (r2 - r1) / 255
	canalRojo = contCanal(Inueva[:,:,0],coef,r1)
	canalVerde = contCanal(Inueva[:,:,1],coef,r1)
	canalAzul = contCanal(Inueva[:,:,2],coef,r1)
	Inueva[:,:,0] = canalRojo
	Inueva[:,:,1] = canalVerde
	Inueva[:,:,2] = canalAzul
	if hist:
		dr = datos(canalRojo, False)
		dv = datos(canalVerde, False)
		da = datos(canalAzul, False)
		graficarHistograma(dr,dv,da)
	return Inueva

def contCanal(canal, coef, r1):
	"""
	Función que expande un canal de la imagen de r1-r2 a 1-255
	usando la ecuación (r - r1) * coef
	args: 
		canal:	np.ndarray 2x2 con un canal RGB de la imagen
		coef:	float con el coeficiente a multiplicar
		r1:		límite inferior utilizado en la ecuación
	return:
		canal: 	np.ndarray 2x2 con el canal con histoframa expandido
	"""
	x, y = canal.shape
	for xi in range(0,x):
		for yi in range(0,y):
			canal[xi,yi] = canal[xi,yi]*coef + r1
	return canal

#########################################################################
# Desplazar histograma de una imagen
#########################################################################

def desplazarHistograma(I, d, hist=False):
	Inueva = I.copy()
	canalRojo = desplazarCanal(Inueva[:,:,0], d)
	canalVerde = desplazarCanal(Inueva[:,:,1], d)
	canalAzul = desplazarCanal(Inueva[:,:,2], d)
	Inueva[:,:,0] = canalRojo
	Inueva[:,:,1] = canalVerde
	Inueva[:,:,2] = canalAzul
	if hist:
		dr = datos(canalRojo, False)
		dv = datos(canalVerde, False)
		da = datos(canalAzul, False)
		graficarHistograma(dr,dv,da)
	return Inueva
	
def desplazarCanal(canal, d):
	x, y = canal.shape
	for xi in range(0,x):
		for yi in range(0,y):
			if canal[xi,yi] + d <= 255:
				if canal[xi,yi] + d >= 0:
					canal[xi,yi] = canal[xi,yi] + d
				else:
					canal[xi,yi] = 0
			else:
				canal[xi,yi] = 255
	return canal

#########################################################################
# Ecualizar el histograma de una imagen 
#########################################################################

def ecualizarHistograma(I, hist=False):
	Inueva = I.copy()
	canalRojo = ecualizarCanal(Inueva[:,:,0])
	canalVerde = ecualizarCanal(Inueva[:,:,1])
	canalAzul = ecualizarCanal(Inueva[:,:,2])
	Inueva[:,:,0] = canalRojo
	Inueva[:,:,1] = canalVerde
	Inueva[:,:,2] = canalAzul
	if hist:
		dr = datos(canalRojo, False)
		dv = datos(canalVerde, False)
		da = datos(canalAzul, False)
		graficarHistograma(dr,dv,da)
	return Inueva

def ecualizarCanal(canal):
	m, n = canal.shape
	dc = datos(canal, False)
	nuevosDatos = dict()
	coeficiente = 255/(m*n) 
	acumulado = 0
	dcnuevo = dict() 
	for k,v in dc.items():
		acumulado += v
		if int(acumulado * coeficiente) in nuevosDatos.keys():
			nuevosDatos[int(acumulado * coeficiente)] += v
		else:
			nuevosDatos[int(acumulado * coeficiente)] = v
		dcnuevo[k] = int(acumulado * coeficiente)
	# print(dc)
	# print(nuevosDatos)
	for x in range(0,m):
		for y in range(0,n):
			canal[x,y] = dcnuevo[canal[x,y]]
	return canal

#########################################################################
# Funciones auxiliares para generar y presentar el histograma
#########################################################################

def graficarHistograma(dr,dv,da,labels=None):
	"""
	Procedimiento que grafica el histograma utilizando matplotlib
	args: 
		dr, dv, da = diccionarios con la cuenta de las intensidades por pixel
					 de cada canal, rgb (rva)
					 [intensidad] -> N° de pixeles
		labels	   = lista con las leyendas respectivas a cada canal
					 es un argumento opcional.
	"""
	plt.figure(figsize=(8,6))
	if labels is not None:
		plt.plot(dr.keys(),dr.values(), 'r', label=labels[0])
		plt.plot(dv.keys(),dv.values(), 'g', label=labels[1])
		plt.plot(da.keys(),da.values(), 'b', label=labels[2])
	else:
		plt.plot(dr.keys(),dr.values(), 'r')
		plt.plot(dv.keys(),dv.values(), 'g')
		plt.plot(da.keys(),da.values(), 'b')
	plt.xlabel('Intesidad')
	plt.ylabel('Cantidad de pixeles')
	plt.title("Histograma")
	plt.legend()
	plt.show()

def datos(canal, estadisticos=True):
	"""
	Función que obtiene un diccionario de los datos de un canal de la imagen RGB
	Obtiene además los estadísticos: medía, varianza y asimetría
	args:
		canal 		 =	np.ndarray 2x2 con los datos de un canal RGB
		estadísticos =	booleano que activa la obtención de los estadísticos
						es un argumento opcional
	return:
		datos 		 =	diccionario con la cuenta de las intensidades por pixel
					 	del canal, rgb (rva)
	si estadísticos = True:
		media 		 = 	media del histograma del canal
		asimetría 	 = 	asimetría del histograma del canal
		varianza 	 = 	varianza del histograma del canal
	"""
	datos = dict()
	for i in range(0, 256):
		datos[i] = 0
	x, y = canal.shape
	for xi in range(1,x):
		for yi in range(1,y):
			datos[canal[xi, yi]] += 1   
	if estadisticos:
		arregloDatos = np.array(list(datos.values()))
		media = arregloDatos.mean()
		mediana = np.median(arregloDatos)		
		varianza = np.var(arregloDatos)
		asimetría = 3*(media - mediana)/varianza**(1/2)
		return datos, round(media,2), round(asimetría,2), round(varianza,2)
	else:
		return datos




import math
import numpy as np

Tiempo_llegada = [49, 66, 87, 33, 60, 67, 64, 52, 47, 44, 87, 63, 68, 80, 8, 30, 14, 71, 33, 46, 110, 31, 34, 51, 19, 77, 51, 54, 93, 37, 76, 76, 87, 46, 52, 51, 71, 47, 57, 58, 48, 37, 35, 46, 16, 54, 50, 54, 56, 32]

Tiempo_servicio = [3, 5, 5, 1, 4, 1, 5, 5, 6, 1, 3, 6, 1, 3, 5, 2, 4, 4, 1, 5, 4, 1, 3, 3, 5, 5, 3, 1, 3, 3, 4, 2, 3, 5, 6, 1, 5, 2, 2, 2, 2, 6, 4, 2, 4, 3, 5, 3, 2, 4]

Prioridad = [5, 1, 1, 3, 2, 0, 2, 0, 1, 4, 0, 3, 1, 4, 0, 3, 5, 3, 0, 0, 4, 0, 3, 1, 5, 2, 4, 2, 2, 3, 1, 0, 3, 5, 3, 3, 2, 5, 5, 4, 1, 0, 4, 2, 5, 4, 0, 2, 3, 4]

# Calculando media
k = 0
for i in Tiempo_llegada:
    k = k + i
media = k/len(Tiempo_llegada)

#Calculando desviación estandar
#k = 0
#for i in Tiempo_llegada:
    #k = k + (i-media)**2
#desviacion = k/(len(Tiempo_llegada)-1)

desviacion = np.std(Tiempo_llegada)
print ("Calculados Media {0} Desviacion estandar {1}".format(media,desviacion))

##Generacion de datos de tiempo de llegada con distribucion normal, redondear hacia arriba
print (np.random.normal(media,desviacion,50))

Mx = max(Tiempo_servicio)

b = ((len(Tiempo_servicio)+1)*Mx)/(len(Tiempo_servicio)-1)

print ("Calculo de b para la distribucion uniforme del tiempo de llegada {0}".format(b))

##Generacion de datos de tiempo de servicio con distribucion uniforme, redondear hacia arriba

print (np.random.uniform(0,b,50))
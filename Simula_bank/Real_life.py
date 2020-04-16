from Taller_calse.Simulation import Fifo, Lifo, Priority

cabecera = "TOTAL CLIENTES;TOTAL ATENDIDOS;DESERTADOS;PROMEDIO INTERMEDIO;PROMEDIO DE SERVICIO;PROMEDIO DE RETRASO;PROMEDIO DE ESPERA\n"

file = open('DatosFIFO.csv','w')
file.write(cabecera)
#Recolectando datos de la simulación ejecutada 100 veces con sistema de cola FIFO
for i in range(0,100):
    file.write(Fifo())
file.close()

file2 = open('DatosLIFO.csv','w')
file2.write(cabecera)
#Recolectando datos de la simulación ejecutada 100 veces con sistema de cola LIFO
for j in range(0,100):
    file2.write(Lifo())
file2.close()

file3 = open('DatosPRIORIDAD.csv','w')
file3.write(cabecera)
#Recolectando datos de la simulación ejecutada 100 veces con sistema de cola por prioridad
for k in range(0,100):
    file3.write(Priority())
file3.close()
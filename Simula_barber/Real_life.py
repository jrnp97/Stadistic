from Barber.Simulation import run
cabecera = "TOTAL CLIENTES;TOTAL ATENDIDOS;DESERTADOS;DESPUES DE CERRAR;PROMEDIO INTERMEDIO;PROMEDIO DE SERVICIO;PROMEDIO DE RETRASO;PROMEDIO DE ESPERA\n"

file = open('Datos.csv','w')
file.write(cabecera)
#Recolectando datos de la simulación ejecutada 100 veces con sistema de cola FIFO
for i in range(0,1000):
    file.write(run())
file.close()
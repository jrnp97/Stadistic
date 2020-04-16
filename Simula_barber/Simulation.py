from Barber.Generate import arrival, service
from Barber.Client import Client
from Barber.Shop import Shop

#Funcion que calcula datos de la simulacion
def promwork(Clientes, T, A, DESERT, AFTER):
    # tiempo intermedio
    acum = 0
    for i in range(0, len(Clientes)):
        if (Clientes[i].desert == False):
            acum = acum + Clientes[i].interA_time

    R = acum / len(Clientes)

    # tiempo de servicio
    acum = 0
    for i in range(0, len(Clientes)):
        if (Clientes[i].desert == False):
            acum = acum + Clientes[i].service_time

    S = acum / len(Clientes)

    # tiempo de retraso
    acum = 0
    for i in range(0, len(Clientes)):
        if (Clientes[i].desert == False):
            acum = acum + Clientes[i].queue_time
    D = acum / len(Clientes)

    # tiempo de espera
    acum = 0
    for i in range(0, len(Clientes)):
        if (Clientes[i].desert == False):
            acum = acum + Clientes[i].wait_time
    W = acum / len(Clientes)

    data = str(T) + ";" + str(A) + ";" + str(DESERT) + ";" + str(AFTER) + ";" + str(R) + ";" + str(S) + ";" + str(D) + ";" + str(W) + "\n"

    return data

"""
Simulando el tiempo en minutos donde 0min = 8:00am y 540min = 5:00pm
Entonces los clientes que llegan en la 1ra hora llegaran entre 0min - 60min,
los clientes que llegan en la 2da hora llegaran entre 61min - 120min,
los clientes que llegan en la 3ra hora llegaran entre 121min - 180min,
los clientes que llegan en la 4ta hora llegaran entre 181min - 240min,
los clientes que llegan en la 5ta hora llegaran entre 241min - 300min,
los clientes que llegan en la 6ta hora llegaran entre 301min - 360min,
los clientes que llegan en la 8va hora llegaran entre 361min - 420min,
los clientes que llegan en la 9na hora llegaran entre 421min - 480min,
los clientes que llegan en la 10ma hora llegaran entre 481min - 540min
En total el servicio de barberia se ejecuta durante 10 horas.
"""
def search(H, Clientes):
    cont = 0
    for i in Clientes:
        if(i.arrival_time==H):
            cont = cont + 1
    return cont

def change(T):
    h = int(T/60)
    return h

def run():
    # Creando objeto "tienda de barberias"
    Barber = Shop()

    # Calculando numero de clientes que llegan por hora
    cant_client_hour = arrival()

    print("Cantidad de clientes por hora {0}".format(cant_client_hour))

    # Generando los tiempos de servicio de cada cliente que llegaron en la hora x
    clientes = []
    h = 0
    id = 0
    for i in cant_client_hour:
        cont = 0
        while (cont < i):
            clientes.append(Client(ID=id,
                                   arrival_time=h,
                                   service_time=service()
                                   )
                            )
            cont = cont + 1
            id = id + 1
        h = h + 1

    Time = 0
    i = 0
    hora_actual = 0
    hora = 0
    entro = 0
    AFTER = 0
    while(True):
        #print ("Tiempo {0} - Hora {1}".format(Time,hora_actual))
        #Se restablece la cantidad de llegada de clientes
        Cant = 0
        #Sacando la cantidad de clientes por tiempo siempre que la hora cambie
        hora_actual = change(Time)
        if(hora_actual == hora):
            Cant = search(hora_actual,clientes)
            hora = hora + 1
        #Actualizando estado del barbero
        Barber.attend(Time)

        """
        if (Barber.status()):
            print ("BARBERO LIBRE")
        else:
            print("BARBERO OCUPADO")

        if (Barber.status_queue()):
            print ("COLA VACIA")
        else:
            print ("COLA LLENA")
        """

        if(hora<9):
            """
            Si la hora es menor a 9 se experan clientes aun.
            """
            #Ya extraida la cantidad de clientes que llegaron en la hora a analizar procedimos a simular su comportamiento en la cola
            if(Cant > 0 or (Cant == 0 and not Barber.status_queue())):
                """
                Si la cantidad que llego es mayor a 0 o si no llego nadie pero la cola sigue llena
                """
                cont = 0
                if((Barber.status() and Barber.status_queue())):
                    """
                    Si el barbero se encuentra libre se atiende al cliente,
                    1. se calcula el tiempo en que estara el cliente en la cola
                    2. se cambia su estado ha atendido
                    3. se establece el tiempo de inicio del servicio
                    4. se invoca el metodo attend que recalcula el estado del barbero.
                    5. se aumenta el valor de i para cambiar el cliente a tratar
                    6. se aumenta el valor del contador, el cual indica la cantidad de clientes que llegaron que se atendieron.
                    """
                    Barber.Max = Time + clientes[i].service_time
                    clientes[i].attend = True
                    clientes[i].Time_attend = Time
                    Barber.attend(Time)
                    #print("Atendiendo a cliente {0} que llega en la hora {2} tiempo de servicio {1} termina en el tiempo {3}".format(Clientes[i].ID, Clientes[i].service_time, Clientes[i].arrival_time,Barber.Max))
                    i = i + 1
                    cont = cont + 1
                elif(not Barber.status_queue() and Barber.status()):
                    """
                    Si la cola no se encuentra vacia y el estado del barbero es libre,
                    1. se saca al cliente de la cola.
                        1.1 extrayendo su informacion
                        1.2 eliminandolo de la cola
                    2. cambiando su estado de cola a falso.
                    3. establece su estado de atencion a true.
                    4. se establece el tiempo de inicio del servicio
                    5. se establece el tiempo maximo del barbero ocupado.
                    6. se invoca el metodo attend 
                    """
                    clien = Barber.Queue[0]
                    #print ("Sacando al cliente {0} de la cola".format(Clientes[clien.ID]))
                    Barber.Queue.popleft()
                    clientes[clien.ID].state_queue = False
                    clientes[clien.ID].attend = True
                    clientes[clien.ID].Time_attend = Time
                    Barber.Max = Time + clientes[clien.ID].service_time
                    Barber.attend(Time)
                while(cont<Cant):
                    #print ("Añadiendo al cliente {0} que llega en la hora {1} en la cola".format(Clientes[i].ID,Clientes[i].arrival_time))
                    """
                    Si se atendio o se extrajo de la cola a 1 cliente y quedan muchos por atender se agregan a la cola,
                    1. verificando si se agregaron correctamente (Maximos en cola 10).
                    2. De no ingresar a la cola se cambia el estado del cliente a desertado
                    3. Se aumenta el contador
                    4. Se aumenta el numero de clientes.
                    """
                    if (Barber.add_Queue(clientes[i])):
                        clientes[i].state_queue = True
                    else:
                        # El cliente se fue porque la cola estaba llena
                        clientes[i].desert = True
                    cont = cont + 1
                    i = i + 1
        else:
            if (entro == 0):
                AFTER = len(Barber.Queue)
                entro = 1
            """
            Cuando la hora se excede de 1 ya se atenderan a los clientes dentro de la barberia (ya cerro).
            """
            if (not Barber.status_queue() and Barber.status()):
                clien = Barber.Queue[0]
                Barber.Queue.popleft()
                clientes[clien.ID].state_queue = False
                clientes[clien.ID].attend = True
                clientes[clien.ID].Time_attend = Time
                Barber.Max = Time + clientes[clien.ID].service_time
                Barber.attend(Time)
                # Si la cola esta vacia y ya no llegaran mas clientes termina la ejecución
            if (Barber.status_queue()):
                break
        # Aumentando el tiempo
        Time = Time + 1
        #os.system("pause")

    count = 0
    for i in range(0, len(clientes)):
        # Calulando tiempo intermedio de llegada
        temp = abs(clientes[i].arrival_time - clientes[i - 1].arrival_time)
        clientes[i].setInterarrival_time(temp)
        # Si el cliente no deserto se calculan los datos
        if (clientes[i].desert == False):
            # Calculando tiempos restantes
            clientes[i].setQueue_time()
            clientes[i].setWait_time()
            clientes[i].setDeparture_time()
        else:
            # Contando cantidad de clientes que han desertados
            count = count + 1
    TOTAL = len(clientes)
    DESERT = count
    ATTEND = len(clientes) - count

    """
    Los calculos estadisticos que se pueden realizar son de 2 tipos

    - Estadisticas de promedio de trabajos
        - Promedio de tiempo intermedio (r)
        - Promedio de tiempo de servicio (s)
        - Promedio de retraso (d)
        - promedio de espera (w)

    - Estadisticas de promedio de tiempos

        - numero de trabajos en el nodo de servicio en el tiempo t
        - numero de trabajos en la cola en el tiempo t
        - numero de trabajos en servicio en el tiempo t

    """

    # Calculando promedios de trabajo y generando información

    data = promwork(clientes, TOTAL, ATTEND, DESERT, AFTER)
    return data
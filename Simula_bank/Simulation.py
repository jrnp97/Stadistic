from Taller_calse.Client import Client
from Taller_calse.Banco import Banco, Bancolifo, Bancopriority
from Taller_calse.Generate import T_arrival,T_service
from Taller_calse.FIFO import organize as FIFO
from Taller_calse.LIFO import organize as LIFO
import os
#Steps for generate simulation
# 1. Generate 50 arrival,service and tolerance time
# 2. Ordened the data with System FIFO or LIFO Queue
# 3. Create 50 Client's with the data ordened
# 4. Send to customer's to be attended in the bank

# Step 4

# Count the clients that arrival in the time T
def search(T, Clients):
    C = 0
    for i in Clients:
        if (i.arrival_time == T):
            C = C + 1
    return C

#Funcion que verifica los clientes en cola, si ya paso su tiempo de tolerancia
def desert_client(Tim, Clients, Bank):
    for i in Clients:
        if(i.state_queue and not i.desert):
            time_waiting = Tim - i.arrival_time
            if(time_waiting>i.wait_time):
                i.desert = True
                Bank.Queue.remove(i)

def c_desert(Clients):
    Count = 0
    for i in Clients:
        if(i.desert):
            Count = Count + 1
    return Count


def promwork(Clients, T,A,DESERT):
    # tiempo intermedio
    acum = 0
    for i in range(0, len(Clients)):
        if (Clients[i].desert == False):
            acum = acum + Clients[i].interA_time

    R = acum / len(Clients)

    # tiempo de servicio
    acum = 0
    for i in range(0, len(Clients)):
        if (Clients[i].desert == False):
            acum = acum + Clients[i].service_time

    S = acum / len(Clients)

    # tiempo de retraso
    acum = 0
    for i in range(0, len(Clients)):
        if (Clients[i].desert == False):
            acum = acum + Clients[i].queue_time
    D = acum / len(Clients)

    # tiempo de espera
    acum = 0
    for i in range(0, len(Clients)):
        if (Clients[i].desert == False):
            acum = acum + Clients[i].wait_time
    W = acum / len(Clients)

    data = str(T) + ";" + str(A) + ";" + str(DESERT) + ";" + str(R) + ";" + str(S) + ";" + str(D) + ";" + str(
        W) + "\n"

    return data

#Generate arrival, service and tolerance time with FIFO order
def Fifo():
    Priotity_t, Arrival_t, Service_t, Tolerance_t = FIFO(priority_t=T_service(b=6),
                                                         arrival_t=T_arrival(),
                                                         service_t=T_service(a=1),
                                                         tolerance_t=T_arrival(media=10, deviation=2)
                                                         )
    #Step 3
    #Generate 50 clients
    Clients = []
    for i in range(0,len(Arrival_t)):
        Clients.append(Client
                       (ID=i,
                        arrival_time=Arrival_t[i],
                        service_time=Service_t[i],
                        tolerance_time=Tolerance_t[i]
                        )
                       )
    #Creating object bank
    Bank = Banco()

    #Cicle that simule the time
    Time = 0
    i = 0

    while(True):
        #Verificando la caja
        Bank.attend(Time)

        #Calculando si un cliente en la cola se va
        desert_client(Time, Clients, Bank)
        #Si i se encuentra en el rango 0 - 49, aun hay clientes por llegar
        if (i < 50):
            #Bucamos la cantidad de clientes que ingresen en el tiempo Time
            C = search(Time, Clients)
            #Verificamos si la cantidad es diferente de 0 o si la cantidad es 0 pero hay clientes en la cola se procede a realizar las acciones
            if (C>0 or (C==0 and not Bank.status_queue())):
                #Inicializando contador en 0
                count = 0
                #Verificando si el cajero del banco esta ocupado y si la cola se encuentra ocupada o si es el primer cliente
                if((Bank.status() and Bank.status_queue()) or Time==Clients[0].arrival_time):
                    """
                    Si la condicion anterior se cumple el cliente se atendera,
                    se calcula el tiempo en el que estara en el caljero,
                    se cambia el estado a atendido,
                    y se envia a atencion,
                    ademas se aumenta i y el contador se establece en 1
                    """
                    Bank.Max = Time + Clients[i].service_time
                    Clients[i].attend = True
                    Clients[i].Time_attend = Time
                    Bank.attend(Time)
                    i = i + 1
                    count = 1
                elif(not Bank.status_queue() and Bank.status()):
                    """
                    La condicion anterior verifica si el cajero se encuentra ocupado,
                    y el estado de la cola si se encuentra llena o no, 
                    la cual prepara la accion de si no llega nadie se atienda al cliente de la cola, realizando lo siguiente
                    Se extrae el cliente de la cola,
                    Se elimina este de la cola,
                    Se establece el estado en cola a False, y su estado de atencion a True,
                    se establece el tiempo en que se atendio,
                    se calcula su tiempo maximo en el servicio y se envia a atencion
                    """
                    clien = Bank.Queue[0]
                    Bank.Queue.popleft()
                    Clients[clien.ID].state_queue = False
                    Clients[clien.ID].attend = True
                    Clients[clien.ID].Time_attend = Time
                    Bank.Max = Time + Clients[clien.ID].service_time
                    Bank.attend(Time)
                while(count<C):
                    """
                    Este ciclo se encarga de ingresar a los clientes a la cola por si llegaron 2 se atiende al 1 y el otro ingresa
                    a la cola, para ingresar un cliente a la cola se realiza lo siguiente
                    Se cambia su estado en cola a True, se agrega a la cola
                    se aumenta el contador
                    y se aumenta la variable i que indica el id del cliente
                    """
                    Clients[i].state_queue = True
                    Bank.add_Queue(Clients[i])
                    count = count + 1
                    i = i + 1
        else:
            """
            Aqui se maneja el caso de que i este en el rango 50 en adelante, eso quiere decir que no habra mas clientes,
            por ende simplemente se debe atender a los que se encuentren en la cola, para ello se reealiza lo siguiente
            se verifica el estado de la cola si no esta vacia y el estado del cajero si no encuentra ocupado,
            se extrae 1er cliente de la cola,
            se elimina este de la cola
            se cambia su estado de cola a False, se cambia el estado de atencion a True,
            se establece el tiempo en que se atendio,
            se calcula su tiempo en el servicio y se envia al cajero
            """
            if (not Bank.status_queue() and Bank.status()):
                clien = Bank.Queue[0]
                Bank.Queue.popleft()
                Clients[clien.ID].state_queue = False
                Clients[clien.ID].attend = True
                Clients[clien.ID].Time_attend = Time
                Bank.Max = Time + Clients[clien.ID].service_time
                Bank.attend(Time)
            #Si la cola esta vacia y ya no llegaran mas clientes termina la ejecución
            if (Bank.status_queue()):
                break
        #Aumentando el tiempo
        Time = Time + 1

    """
    En este punto los clientes ya han sido atendidos o han desertado,
    los no desertados cuentan con la siguiente informacion
    
    - arrival_time (Tiempo de llegada)
    - service_time (Tiempo de servicio)
    - Time that begins service (Tiempo de inicio del servicio)
    
    Por ende se deben calcular los 3 datos restantes que son
    
    - Delay in queue (Tiempo en cola)
    - Wait in the nodde (Tiempo de espera)
    - Departure time (Tiempo total en el sistema)
    - Interarrival time (Intervalo de tiempo)
    
    Nota: el calculo de los datos restantes se debe realizar en el orden mostrado. 
    """

    count = 0
    for i in range(0,len(Clients)):
        # Calulando tiempo intermedio de llegada
        temp = abs(Clients[i].arrival_time - Clients[i - 1].arrival_time)
        Clients[i].setInterarrival_time(temp)
        #Si el cliente no deserto se calculan los datos
        if(Clients[i].desert==False):
            #Calculando tiempos restantes
            Clients[i].setQueue_time()
            Clients[i].setWait_time()
            Clients[i].setDeparture_time()
        else:
            #Contando cantidad de clientes que han desertados
            count = count + 1
    TOTAL = len(Clients)
    DESERT = count
    ATTEND = len(Clients) - count

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

    data = promwork(Clients,TOTAL,ATTEND,DESERT)
    return data


def Lifo():
    Arrival_t, Service_t, Tolerance_t = LIFO(T_arrival(), T_service(a=1,b=6), T_arrival(media=10, deviation=2))

    # Step 3
    # Generate 50 clients
    Clients = []
    for i in range(0, len(Arrival_t)):
        Clients.append(Client
                       (ID=i,
                        arrival_time=Arrival_t[i],
                        service_time=Service_t[i],
                        tolerance_time=Tolerance_t[i]
                        )
                       )

    # Creating object bank
    Bank = Bancolifo()

    # Cicle that simule the time
    Time = 0
    i = 0

    while (True):
        # Verificando la caja
        Bank.attend(Time)

        # Calculando si un cliente en la cola se va
        desert_client(Time, Clients, Bank)
        # Si i se encuentra en el rango 0 - 49, aun hay clientes por llegar
        if (i < 50):
            # Bucamos la cantidad de clientes que ingresen en el tiempo Time
            C = search(Time, Clients)
            # Verificamos si la cantidad es diferente de 0 o si la cantidad es 0 pero hay clientes en la cola se procede a realizar las acciones
            if (C > 0 or (C == 0 and not Bank.status_queue())):
                # Inicializando contador en 0
                count = 0
                # Verificando si el cajero del banco esta ocupado y si la cola se encuentra ocupada o si es el primer cliente
                if ((Bank.status() and Bank.status_queue()) or Time == Clients[0].arrival_time):
                    """
                    Si la condicion anterior se cumple el cliente se atendera,
                    se calcula el tiempo en el que estara en el caljero,
                    se cambia el estado a atendido,
                    y se envia a atencion,
                    ademas se aumenta i y el contador se establece en 1
                    """
                    Bank.Max = Time + Clients[i].service_time
                    Clients[i].attend = True
                    Clients[i].Time_attend = Time
                    Bank.attend(Time)
                    i = i + 1
                    count = 1
                elif (not Bank.status_queue() and Bank.status()):
                    """
                    La condicion anterior verifica si el cajero se encuentra ocupado,
                    y el estado de la cola si se encuentra llena o no, 
                    la cual prepara la accion de si no llega nadie se atienda al cliente de la cola, realizando lo siguiente
                    Se extrae el cliente de la cola,
                    Se elimina este de la cola,
                    Se establece el estado en cola a False, y su estado de atencion a True,
                    se establece el tiempo en que se atendio,
                    se calcula su tiempo maximo en el servicio y se envia a atencion
                    """
                    clien = Bank.Queue[(len(Bank.Queue)-1)]
                    Bank.Queue.pop()
                    Clients[clien.ID].state_queue = False
                    Clients[clien.ID].attend = True
                    Clients[clien.ID].Time_attend = Time
                    Bank.Max = Time + Clients[clien.ID].service_time
                    Bank.attend(Time)
                while (count < C):
                    """
                    Este ciclo se encarga de ingresar a los clientes a la cola por si llegaron 2 se atiende al 1ro y el otro ingresa
                    a la cola, para ingresar un cliente a la cola se realiza lo siguiente
                    Se cambia su estado en cola a True, se agrega a la cola
                    se aumenta el contador
                    y se aumenta la variable i que indica el id del cliente
                    """
                    Clients[i].state_queue = True
                    Bank.add_Queue(Clients[i])
                    count = count + 1
                    i = i + 1
        else:
            """
            Aqui se maneja el caso de que i sobre el rango 50, eso quiere decir que no llegarán mas clientes,
            por ende simplemente se debe atender a los que se encuentren en la cola, para ello se realiza lo siguiente
            se verifica el estado de la cola si no esta vacia y el estado del cajero no encuentra ocupado,
            se extrae el cliente de la cola,
            se elimina este de la cola
            se cambia su estado de cola a False, se cambia el estado de atencion a True,
            se establece el tiempo en que se atendio,
            se calcula su tiempo en el servicio y se envia al cajero
            """
            if (not Bank.status_queue() and Bank.status()):
                clien = Bank.Queue[(len(Bank.Queue)-1)]
                Bank.Queue.pop()
                Clients[clien.ID].state_queue = False
                Clients[clien.ID].attend = True
                Clients[clien.ID].Time_attend = Time
                Bank.Max = Time + Clients[clien.ID].service_time
                Bank.attend(Time)
            # Si la cola esta vacia y ya no llegaran mas clientes termina la ejecución
            if (Bank.status_queue()):
                break
        # Aumentando el tiempo
        Time = Time + 1

    """
    En este punto los clientes ya han sido atendidos o han desertado,
    de los no desertados se cuentan la siguiente informacion

    - arrival_time (Tiempo de llegada)
    - service_time (Tiempo de servicio)
    - Time that begins service (Tiempo de inicio del servicio)

    Por ende se deben calcular los 3 datos restantes que son

    - Delay in queue (Tiempo en cola)
    - Wait in the nodde (Tiempo de espera)
    - Departure time (Tiempo total en el sistema)
    - Interarrival time (Intervalo de tiempo)

    Nota: el calculo de los datos restantes se debe realizar en el orden mostrado. 
    """

    count = 0
    for i in range(0, len(Clients)):
        # Calulando tiempo intermedio de llegada
        temp = abs(Clients[i].arrival_time - Clients[i - 1].arrival_time)
        Clients[i].setInterarrival_time(temp)
        # Si el cliente no deserto se calculan los datos
        if (Clients[i].desert == False):
            # Calculando tiempos restantes
            Clients[i].setQueue_time()
            Clients[i].setWait_time()
            Clients[i].setDeparture_time()
        else:
            # Contando cantidad de clientes que han desertados
            count = count + 1
    TOTAL = len(Clients)
    DESERT = count
    ATTEND = len(Clients) - count

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

    data = promwork(Clients,TOTAL,ATTEND,DESERT)
    return data

def Priority():
    Priotity_t, Arrival_t, Service_t, Tolerance_t = FIFO(priority_t=T_service(b=6),
                                                         arrival_t=T_arrival(),
                                                         service_t=T_service(),
                                                         tolerance_t=T_arrival(media=10, deviation=2)
                                                         )


    # Step 3
    # Generate 50 clients
    Clients = []
    for i in range(0, len(Arrival_t)):
        Clients.append(Client
                       (ID=i,
                        arrival_time=Arrival_t[i],
                        service_time=Service_t[i],
                        tolerance_time=Tolerance_t[i],
                        priority_time=Priotity_t[i]
                        )
                       )

    # Creating object bank
    Bank = Bancopriority()

    # Cicle that simule the time
    Time = 0
    i = 0

    while (True):
        # Verificando la caja
        Bank.attend(Time)

        # Calculando si un cliente en la cola se va
        desert_client(Time, Clients, Bank)
        # Si i se encuentra en el rango 0 - 49, aun hay clientes por llegar
        if (i < 50):
            # Bucamos la cantidad de clientes que ingresen en el tiempo Time
            C = search(Time, Clients)
            # Verificamos si la cantidad es diferente de 0 pero si la cantidad es 0 y hay clientes en la cola se procede a realizar las acciones
            if (C > 0 or (C == 0 and not Bank.status_queue())):
                # Inicializando contador en 0
                count = 0
                # Verificando si el cajero del banco esta ocupado y si la cola se encuentra ocupada o si es el primer cliente
                if ((Bank.status() and Bank.status_queue()) or Time == Clients[0].arrival_time):
                    """
                    Si la condicion anterior se cumple el cliente se atendera,
                    se calcula el tiempo en el que estara en el caljero,
                    se cambia el estado a atendido,
                    y se envia a atencion,
                    ademas se aumenta i y el contador se establece en 1
                    """
                    Bank.Max = Time + Clients[i].service_time
                    Clients[i].attend = True
                    Clients[i].Time_attend = Time
                    Bank.attend(Time)
                    i = i + 1
                    count = 1
                elif (not Bank.status_queue() and Bank.status()):
                    """
                    La condicion anterior verifica si el cajero se encuentra ocupado,
                    y el estado de la cola si se encuentra llena o no, 
                    la cual prepara la accion de si no llega nadie se atienda al cliente de la cola, realizando lo siguiente
                    Se extrae el cliente de la cola,
                    Se elimina este de la cola,
                    Se establece el estado en cola a False, y su estado de atencion a True,
                    se establece el tiempo en que se atendio,
                    se calcula su tiempo maximo en el servicio, se envia a atencion
                    """
                    clien = Bank.Queue[0]
                    Bank.Queue.popleft()
                    Clients[clien.ID].state_queue = False
                    Clients[clien.ID].attend = True
                    Clients[clien.ID].Time_attend = Time
                    Bank.Max = Time + Clients[clien.ID].service_time
                    Bank.attend(Time)
                while (count < C):
                    """
                    Este ciclo se encarga de ingresar a los clientes a la cola por si llegaron 2 se atiende al 1ro y el otro ingresa
                    a la cola, para ingresar un cliente a la cola se realiza lo siguiente
                    Se cambia su estado en cola a True, se agrega a la cola
                    se aumenta el contador
                    y se aumenta la variable i que indica el id del cliente,
                    ademas se reorganiza la cola por la prioridad de los clientes en esta
                    """
                    Clients[i].state_queue = True
                    Bank.add_Queue(Clients[i])
                    Bank.order_queue()
                    count = count + 1
                    i = i + 1
        else:
            """
            Aqui se maneja el caso de que i este en el rango 50 en adelante, eso quiere decir que no habra mas clientes,
            por ende simplemente se debe atender a los que se encuentren en la cola, para ello se reealiza lo siguiente
            se inicializa en contador en 0
            se verifica el estado de la cola si no esta vacia y el estado del cajero si no encuentra ocupado,
            se extrae 1er cliente de la cola,
            se elimina este de la cola
            se cambia su estado de cola a False, se cambia el estado de atencion a True,
            se establece el tiempo en que se atendio,
            se calcula su tiempo en el servicio, se envia al cajero
            """
            if (not Bank.status_queue() and Bank.status()):
                clien = Bank.Queue[0]
                Bank.Queue.popleft()
                Clients[clien.ID].state_queue = False
                Clients[clien.ID].attend = True
                Clients[clien.ID].Time_attend = Time
                Bank.Max = Time + Clients[clien.ID].service_time
                Bank.attend(Time)
            # Si la cola esta vacia y ya no llegaran mas clientes termina la ejecución
            if (Bank.status_queue()):
                break
        # Aumentando el tiempo
        Time = Time + 1

    """
    En este punto los clientes ya han sido atendidos o han desertado,
    los no desertados cuentan con la siguiente informacion

    - arrival_time (Tiempo de llegada)
    - service_time (Tiempo de servicio)
    - Time that begins service (Tiempo de inicio del servicio)

    Por ende se deben calcular los 3 datos restantes que son

    - Delay in queue (Tiempo en cola)
    - Wait in the nodde (Tiempo de espera)
    - Departure time (Tiempo total en el sistema)
    - Interarrival time (Intervalo de tiempo)

    Nota: el calculo de los datos restantes se debe realizar en el orden mostrado. 
    """

    count = 0
    for i in range(0, len(Clients)):
        # Calulando tiempo intermedio de llegada
        temp = abs(Clients[i].arrival_time - Clients[i - 1].arrival_time)
        Clients[i].setInterarrival_time(temp)
        # Si el cliente no deserto se calculan los datos
        if (Clients[i].desert == False):
            # Calculando tiempos restantes
            Clients[i].setQueue_time()
            Clients[i].setWait_time()
            Clients[i].setDeparture_time()
        else:
            # Contando cantidad de clientes que han desertados
            count = count + 1
    TOTAL = len(Clients)
    DESERT = count
    ATTEND = len(Clients) - count

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

    # Calculando promedios de trabajo
    data = promwork(Clients, TOTAL, ATTEND, DESERT)
    return data
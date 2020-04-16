class Client:
    """
    Para 1 trrabajo i (cliente) se debe tener lo siguiente
    1. Tiempo de llegada (Arrival time) -- ai (listo)
    2. Tiempo en cola (Delay in the queue) -- di (calcular)
    3. Tiempo de inicio del servicio (Time that begins service) -- bi = ai + di (listo)
    4. Tiempo de servicio (Service Time) -- si (listo)
    5. Tiempo de espera (Wait in the node) -- wi = di + si (calcular)
    6. Tiempo en el sistema (Depature time) -- ci = ai + wi (calcular)
    7. Tiempo de intervalo -- ri = ai - ai-1
    """
    queue_time = -1
    departure_time = 0
    wait_time = -1
    interA_time = 0

    def __init__(self, ID, arrival_time=0,service_time=0, desert=False, tolerance_time=0, priority_time=0, attend=False, T_attend=0):
        self.ID = ID
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.tolerance_time  = tolerance_time
        self.priority_time = priority_time
        self.desert = desert
        self.attend = attend
        self.Time_attend = T_attend
        self.state_queue = False

    def setQueue_time(self):
        """
        El tiempo en cola sera igual al valor absoluto tiempo de llegada - el tiempo de inicio del servicio,
        por ejemplo si un cliente llego en el tiempo 3 y lo atendieron en el tiempo 6, el tiempo que duro en cola
        serà queue_time 3 - 6  = -3 -> 3, y si llego en el tiempo 3 y lo atendieron en el tiempo 3, su tiempo en cola
        sera de 0.
        """
        if (self.arrival_time==self.Time_attend):
            self.queue_time = 0
        elif (self.Time_attend == 0):
            print("El cliente no tiene establecido un tiempo de atenciòn")
        else:
            self.queue_time = abs(self.arrival_time-self.Time_attend)

    def setWait_time(self):
        """
        El tiempo de espera serà igual al tiempo en cola + el tiempo en servicio
        """
        if (self.queue_time!=-1):
            self.wait_time = self.service_time + self.queue_time

    def setDeparture_time(self):
        """
        El tiempo en el sistema sera igual al tiempo de espera + el tiempo de llegada
        """
        if (self.wait_time!=-1):
            self.departure_time = self.arrival_time + self.wait_time

    def setInterarrival_time(self, inter):
        """
        El tiempo intermedio de llegada sera el tiempo de llegada menos el tiempo de llegada del cliente anterior
        """
        self.interA_time = inter
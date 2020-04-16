class Client:
    ID = None
    arrival_time = 0
    service_time = 0
    Time_attend = -1

    #Calculados
    queue_time = 0
    wait_time = 0
    departure_time = 0
    interA_time = 0

    desert = False
    def __init__(self, ID=None, arrival_time=0,service_time=0):
        self.ID = ID
        self.arrival_time = arrival_time
        self.service_time = service_time

    def setQueue_time(self):
        """
        El tiempo en cola sera igual al valor absoluto tiempo de llegada - el tiempo de inicio del servicio,
        por ejemplo si un cliente llego en el tiempo 3 y lo atendieron en el tiempo 6, el tiempo que duro en cola
        serà queue_time 3 - 6  = -3 -> 3, y si llego en el tiempo 3 y lo atendieron en el tiempo 3, su tiempo en cola
        sera de 0.
        """
        if (self.arrival_time==self.Time_attend):
            self.queue_time = 0
        elif (self.Time_attend == -1):
            pass#print("El cliente no tiene establecido un tiempo de atenciòn")
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

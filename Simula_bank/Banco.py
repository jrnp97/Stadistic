from collections import deque
from Taller_calse.FIFO import organize

class Banco:
    Max = 0

    def __init__(self):
        self.Queue = deque()

    def status(self):
        if self.Max != 0:
            return False
        else:
            return True

    def attend(self, time):
        if (self.Max == time):
            self.Max = 0

    def add_Queue(self, object):
        self.Queue.append(object)

    def get_Queue(self):
        return self.Queue

    def status_queue(self):
        if len(self.Queue) == 0:
            return True
        else:
            return False

class Bancolifo (Banco):

    def __init__(self):
        super(Banco, self).__init__()
        self.Queue = []

class Bancopriority (Banco):

    def order_queue(self):
        #ordenamos los datos de menor (mayor prioridad) a mayor (menor prioridad)
        for i in range(0, len(self.Queue)):
            for j in range(0, len(self.Queue)):
                if (self.Queue[i].priority_time < self.Queue[j].priority_time):
                    #Cambiando orden de los clientes
                    aux = self.Queue[i]
                    self.Queue[i] = self.Queue[j]
                    self.Queue[j] = aux



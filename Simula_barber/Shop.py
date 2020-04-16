from collections import deque

class Shop:
    Max = 0
    def __init__(self):
        self.Queue = deque()

    def add_Queue(self, object):
        if (len(self.Queue) == 10):
            return False
        else:
            self.Queue.append(object)
            return True

    def get_Queue(self):
        return self.Queue

    def attend(self, time):
        if (self.Max == time):
            self.Max = 0

    def status_queue(self):
        if len(self.Queue) == 0:
            return True
        else:
            return False

    def status(self):
        if self.Max != 0:
            return False
        else:
            return True
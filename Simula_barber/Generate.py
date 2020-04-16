import numpy
import math


def arrival():
    list_float = numpy.random.poisson(5,9)

    # Estableciendo todos los datos positivos
    for i in range(0, len(list_float)):
        if (list_float[i] < 0):
            list_float[i] = ((-1) * list_float[i])

    list_int = []
    # Round UP data in list
    for i in range(0, len(list_float)):
        list_int.append(math.ceil(list_float[i]))

    # Return data
    return list_int

def service():
    data_float = numpy.random.exponential(15)
    # Estableciendo el datos positivos
    if(data_float<0):
        data_float = (-1)*data_float
    # Round UP data in list
    data_int = math.ceil(data_float)
    # Return data
    return  data_int
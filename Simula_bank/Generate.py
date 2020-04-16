import numpy
import math

#Function that generate 50 arrival times
def T_arrival(media=53.3,deviation=21.0306918573783):
    list_float = numpy.random.normal(media,deviation,50)
    #Estableciendo todos los datos positivos
    for i in range(0,len(list_float)):
        if (list_float[i]<0):
            list_float[i] = ((-1)*list_float[i])

    list_int = []
    #Round UP data in list
    for i in range(0, len(list_float)):
        list_int.append(math.ceil(list_float[i]))

    #Return data
    return list_int

#Function that generate 50 service times
def T_service(a=0,b=6.244897959183674):
    list_float = numpy.random.uniform(a,b,50)
    list_int = []
    # Estableciendo todos los datos positivos
    for i in range(0,len(list_float)):
        if (list_float[i]<0):
            list_float[i] = ((-1)*list_float[i])

    # Round UP data in list
    for i in range(0, len(list_float)):
        list_int.append(math.ceil(list_float[i]))

    # Return data
    return list_int
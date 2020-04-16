#Example data
#T_llegada = [49, 66, 87, 33, 60, 67, 64, 52, 47, 44, 87, 63, 68, 80, 8, 30, 14, 71, 33, 46, 110, 31, 34, 51, 19, 77, 51, 54, 93, 37, 76, 76, 87, 46, 52, 51, 71, 47, 57, 58, 48, 37, 35, 46, 16, 54, 50, 54, 56, 32]
#T_servicio = [3, 5, 5, 1, 4, 1, 5, 5, 6, 1, 3, 6, 1, 3, 5, 2, 4, 4, 1, 5, 4, 1, 3, 3, 5, 5, 3, 1, 3, 3, 4, 2, 3, 5, 6, 1, 5, 2, 2, 2, 2, 6, 4, 2, 4, 3, 5, 3, 2, 4]

def organize(priority_t=None, arrival_t=None, service_t=None, tolerance_t=None):
    if (priority_t==None):
        #ordenamos los datos de menor a mayor respecto al tiempo de llegada
        for i in range(0, len(arrival_t)):
            for j in range (0, len(arrival_t)):
                if (arrival_t[i]<arrival_t[j]):
                    aux = arrival_t[i]
                    arrival_t[i] = arrival_t[j]
                    arrival_t[j] = aux
                    #Change in the same way the service time
                    aux = service_t[i]
                    service_t[i] = service_t[j]
                    service_t[j] = aux
                    #Change in the same way the tolerance time
                    aux = tolerance_t[i]
                    tolerance_t[i] = tolerance_t[j]
                    tolerance_t[j] = aux
    else:
        # ordenamos los datos de menor a mayor respecto a la prioridad
        for i in range(0, len(priority_t)):
            for j in range(0, len(priority_t)):
                if (priority_t[i] < priority_t[j]):
                    aux = priority_t[i]
                    priority_t[i] = priority_t[j]
                    priority_t[j] = aux
                    # Change in the same way the arrival time
                    aux = arrival_t[i]
                    arrival_t[i] = arrival_t[j]
                    arrival_t[j] = aux
                    # Change in the same way the service time
                    aux = service_t[i]
                    service_t[i] = service_t[j]
                    service_t[j] = aux
                    # Change in the same way the tolerance time
                    aux = tolerance_t[i]
                    tolerance_t[i] = tolerance_t[j]
                    tolerance_t[j] = aux

    #Retornando datos
    return priority_t, arrival_t, service_t, tolerance_t



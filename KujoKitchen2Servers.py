import numpy as np
import math

from numpy.core.fromnumeric import mean

def expRandomNumber(lambdavalue): #Return random X with exponential distribution 
    U = np.random.uniform(0,1)
    return int((-1/lambdavalue)*np.log(U))

def numberToTimeKujo(numberValue): #Turn minutes to Time value <Hour:Mins>.
    hour = int(numberValue/60)+10 #Hora a partir de 10am
    min = int(numberValue%60)
    if(min < 10):
        output = f"{hour}:0{min}"
    else:
        output = f"{hour}:{min}"
    return output

def waitedTime(Arrive,Departure,Preparation):
    outputList = []
    for key in Departure.keys():
        outputList.append(abs((Departure[key]-Arrive[key])-Preparation[key]))
    return outputList

def percentWaiting(waitList):
    n = len(waitList)
    countBiger5 = 0
    for value in waitList:
        if(value > 5):
            countBiger5 = countBiger5 + 1
    return countBiger5/n



#lambdaVal = lambda para la variable aleatoria exponencial en horario normal
#lmbdaValPico = lambda para la variable aleatoria exponencial en horario Pico
def Server2KujoSimulation(lambdaValueNormal = 8,lambdaValuePico = 3):
    lambdaVal = lambdaValueNormal
    #Variables Estaticas de Tiempo
    T = 660 #Tiempo total 11h = 660min
    TPStartDia = 90 #Empieza hora pico 90min despues de abrir
    TPEndDia = 210 #Termina hora pico 120min despues de empezar
    TPStartTarde = 420 
    TPEndTarde = 540
    eventList = [TPStartDia,TPEndDia,TPStartTarde,TPEndTarde,T]

    #Variables de tiempo
    t = 0 #tiempo actual
    tA = 0 #tiempo de arribo del proximo cliente
    tD1 = math.inf # tiempo de salida de S1
    tD2 = math.inf # tiempo de salida de S2
    clientType = 0 # 0 si sandwitch, 1 si sushi
    nextEvent = eventList[0] #Para alternar valores de horario pico y horario normal

    #Variables contadoras
    Na = 0 #Cantidad de arribos
    cS1 = {} #cantidad Partidas desde S1
    cS1Time = {}
    cS2 = {} #cantidad Partidas desde S2
    cS2Time = {}

    #Variables de estado
    clientQueue = [] #Cola con los clientes
    SE = 0 #Proximo Evento
    
    #Variables de salida
    Arrive = {} #Tiempos de arribo
    departure = {} #Tiempo de ida
    preparationTime = {} #Tiempo que demora hacer el sandwich o el sushi de un cliente
    #Inicializar
    tA = expRandomNumber(lambdaVal)
    SS = 0 #Estados
    #Horario Normal
    #SS = 0 <-> S1 = 0, S2 = 0, n = 0

    #SS = 1 <-> S1 = 1, S2 = 0, n = 1
    #SS = 2 <-> S1 = 0, S2 = 1, n = 1

    #SS = 3 <-> S1 = 1, S2 = 1, n = 2
    #SS = 4 <-> S1 = 1, S2 = 1, n > 2

    #Horario Pico con 3 Server
    #SS = 5 <-> S1 = 0, S2 = 0, S3 = 0, n = 0

    #SS = 6 <-> S1 = 1, S2 = 0, S3 = 0, n = 1
    #SS = 7 <-> S1 = 0, S2 = 1, S3 = 0, n = 1
    #SS = 8 <-> S1 = 0, S2 = 0, S3 = 1, n = 1

    #SS = 9 <-> S1 = 0, S2 = 1, S3 = 1, n = 2
    #SS = 10 <-> S1 = 1, S2 = 0, S3 = 1, n = 2

    #SS = 11 <-> S1 = 1, S2 = 1, S3 = 1, n = 3

    #SS = 13 <-> S1 = 1, S2 = 1, S3 = 1, n > 3

    while(t < T):
        #Arribo Horario
        clientType = int(np.random.uniform(1,3))
        if(clientType == 1):
            A = 3
            B = 6
        if(clientType == 2):
            A = 5
            B = 9

        if tA >= T:
            break
        if(min(tA,tD1,tD2,nextEvent) == tA and tA <= T):
            #Time pass
            #else:
            #Horario Normal
            t = tA 
            Na = Na + 1
            new_At = int(np.random.exponential(lambdaVal)) #Segun el horario
            tA = t + new_At
            Arrive[Na] = t

            if(SS == 0):
                SS = 1
                tD1_t = int(np.random.uniform(A,B))
                preparationTime[Na] = tD1_t
                tD1 = t + tD1_t
            elif(SS == 1):
                SS = 3
                tD2_t = int(np.random.uniform(A,B))
                preparationTime[Na] = tD2_t
                tD2 = t + tD2_t
            elif(SS == 2):
                SS = 3
                tD1_t = int(np.random.uniform(A,B))
                preparationTime[Na] = tD1_t
                tD1 = t + tD1_t
            elif(SS == 3):
                SS = 4

            clientQueue.append(Na)

        #Partida S1 
        elif(min(tA,tD1,tD2,nextEvent) == tD1 and tD1 <= T):
            #if(tD1>=TPStartDia or tD1>= TPStartTarde):
            #Horario Pico Cambios
            #    pass
            #else:
            t = tD1
            clientId = clientQueue.pop(0)
            cS1[clientId] = t
            departure[clientId] = t
            cS1Time[clientId] = numberToTimeKujo(t)
            if(SS == 1):
                SS = 0
                tD1 = math.inf
            elif(SS == 3):
                SS = 2
                tD1 = math.inf
            
            elif(SS == 4):
                if(len(clientQueue) < 3):
                    SS = 3
                new_tD1 = int(np.random.uniform(A,B))
                newClient = clientQueue[1]
                preparationTime[newClient] = new_tD1 
                tD1 = t + new_tD1
         
        #Partida S2
        elif(min(tA,tD1,tD2,nextEvent) == tD2 and tD2 <= T):
            t = tD2
            clientId = clientQueue.pop(0)
            cS2[clientId] = t
            departure[clientId] = t
            cS2Time[clientId] = numberToTimeKujo(t)
            if(SS == 2):
                SS = 0
                tD2 = math.inf
            elif(SS == 3):
                SS = 1
                tD2 = math.inf
            elif(SS == 4):
                if(len(clientQueue) < 3):
                    SS = 3
                new_tD2 = int(np.random.uniform(A,B))
                newClient = clientQueue[1]
                preparationTime[newClient] = new_tD2
                tD2 = t + new_tD2

        #Partida Empezar Evento
        elif(min(tA,tD1,tD2,nextEvent) == nextEvent):
            #if(tD2>=TPStartDia or tD2>= TPStartTarde):
            #Horario Pico Cambios
            #    pass
            #else:
            if(SE == 0 or SE == 2):
                lambdaVal = lambdaValuePico
            elif(SE== 1 or SE == 4):
                lambdaVal = lambdaValueNormal
            SE = SE + 1
            t = nextEvent
            tA = nextEvent
            nextEvent = eventList[SE]
    #EndWhile
    if(tD1 < math.inf):
        t = tD1
        cS1[clientId] = t
        cS1Time[clientId] = numberToTimeKujo(t)

    if(tD2 < math.inf):
        t = tD2
        cS2[clientId] = t
        cS2Time[clientId] = numberToTimeKujo(t)

    return Arrive,departure,preparationTime


if __name__ == '__main__':
    Arrive,Departure,PreparationTime = Server2KujoSimulation(7,4)
    finalWaitList = waitedTime(Arrive,Departure,PreparationTime)
    print(f"El porciento de espera de más de 5 minutos con 2 servidores para este caso es: {percentWaiting(finalWaitList)}%")

    listCases = []
    for i in range(100):
        Arrive,Departure,PreparationTime = Server2KujoSimulation(7,4)
        finalWaitList = waitedTime(Arrive,Departure,PreparationTime)
        listCases.append(percentWaiting(finalWaitList))
    print(f"Media del porciento de espera para 100 casos es: {mean(listCases)}")




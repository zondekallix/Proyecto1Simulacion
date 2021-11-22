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
        if key not in Preparation.keys():
            Preparation[key] = 5
        outputList.append(abs((Departure[key]-Arrive[key])-Preparation[key]))
    return outputList

def percentWaiting(waitList):
    n = len(waitList)
    countBiger5 = 0
    for value in waitList:
        if(value > 5):
            countBiger5 = countBiger5 + 1
    return countBiger5/n
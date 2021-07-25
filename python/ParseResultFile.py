
def GetResultsFromFile(fileName):
    x=[]
    y=[]
    z=[]

    with open(fileName,'r') as f:
        dateTime = f.readline()
        print(dateTime.replace('#',''))
        config_Limits = f.readline()
        print(config_Limits)

        for linie in f:       
            data = linie.rstrip().split('\t')
            x.append(float(data[0]))
            y.append(float(data[1]))
            z.append(float(data[2]))
        
        return x,y,z,dateTime,config_Limits
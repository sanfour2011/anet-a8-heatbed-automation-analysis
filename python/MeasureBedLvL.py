import time
import Gauge 
import Printer 
from datetime import datetime
from tqdm import trange, tqdm

xStep = 10
xLim_min = -10
xLim_max = 264
yStep = 10
yLim_min = 0
yLim_max = 213

p = Printer.anetA8Plus("COM7")
g = Gauge.Gauge(comPort="COM4")

date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
date_time = datetime.now().strftime("%Y.%m.%d - %H.%M.%S")

try:
    p.Connect2Printer() 
    p.MoveZ(10)
    p.ReturnHome(True, True, True)
    p.MoveZ(3) #to travel over paper clips, that increases measurement surface
    nextMoveUp = True
    xCoordList = trange(xLim_min,xLim_max,xStep)
    yCoordList = range(yLim_min,yLim_max,yStep)
   
    yTargets = yCoordList

    with open(f".\\reuslts\\{date_time}.txt",'w') as fout:        
        fout.write('#'*15+date_time+'#'*15+"\n")
        fout.write("step size(xStep:{},yStep:{}) xlim:({},{}), ylim:({},{})\n".format(xStep,yStep,xLim_min,xLim_max,yLim_min,yLim_max))
        for x in xCoordList:
            p.MoveX(x)
            if nextMoveUp == True:
                yTargets = yCoordList
            else:
                yTargets = reversed(yCoordList)
        
            for y in yTargets:
                p.MoveY(y)                            
                bedLvl_mm = g.Measure()
                fout.write(f"{x}\t{y}\t{bedLvl_mm}\n")
               

            nextMoveUp = ~nextMoveUp
    
    p.MoveZ(10)
    p.ReturnHome(True, True, True)

finally:
    p.Close()
    g.Close()

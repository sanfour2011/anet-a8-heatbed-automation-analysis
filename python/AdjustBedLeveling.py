import Gauge 
import Printer 

p = Printer.anetA8Plus("COM7")
g = Gauge.Gauge(comPort="COM4")

p.Connect2Printer() 
p.MoveZ(10)
p.ReturnHome(True, True, True)
p.MoveZ(3)
p.MoveXY(240, 0)
p.MoveY(200)
try:
    while True:
        print(g.Measure())

except KeyboardInterrupt:
        pass

finally:
    p.Close()
    g.Close()
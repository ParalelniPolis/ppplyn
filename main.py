#!/usr/bin/python2

from GasMeter import GasMeter

for i in [1,3,4,5,6,7]:
    gas = GasMeter("./images/input/board" + str(i) + ".png")
    value = gas.get_meter_value()

    print(value)

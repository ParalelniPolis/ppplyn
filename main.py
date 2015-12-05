#!/usr/bin/python2

from SimpleCV import Image, ImageSet

from GasMeter import GasMeter


test_frames = ImageSet("./images/input")

for frame in test_frames:

    gas = GasMeter(frame)
    value = gas.get_meter_value()

    print(value)

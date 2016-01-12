#!/usr/bin/env python

import logging
logging.getLogger().setLevel(logging.INFO)

from SimpleCV import ImageSet

from GasMeter import GasMeter


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

test_frames = ImageSet("./images/input")

for frame in test_frames:

    gas = GasMeter(frame)
    value = gas.get_meter_value()
    if is_number(value):
        print(frame.filename + "\t" + "{0:.3f}".format(float(value)))
    else:
        print(frame.filename + "\t" + value + " UNRELIABLE")

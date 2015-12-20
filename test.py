#!/usr/bin/env python

import logging
logging.getLogger().setLevel(logging.INFO)

from SimpleCV import ImageSet

from GasMeter import GasMeter


test_frames = ImageSet("./images/input")

for frame in test_frames:

    gas = GasMeter(frame)
    value = gas.get_meter_value()

    print(frame.filename + "\t" + str(value))

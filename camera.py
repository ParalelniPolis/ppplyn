#!/usr/bin/python2

from SimpleCV import Camera

import time

from GasMeter import GasMeter

cam = Camera(0, {"width": 1280, "height": 720})

first_image = True

while True:

    if first_image:
        first_image = False
        print("Skiping first image")
        time.sleep(5)
        continue

    filename = "./images/camera/camera_" + str(int(time.time())) + ".png"

    print("Saving image " + filename)

    camera_image = cam.getImage()
    camera_image.save(filename)

    gas = GasMeter(camera_image)
    value = gas.get_meter_value()

    print(camera_image.filename + "\t" + value)

    time.sleep(5)

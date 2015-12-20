#!/usr/bin/python2

from SimpleCV import Camera

import time

from GasMeter import GasMeter

import sys

cam = Camera(0, {"width": 1280, "height": 720})

first_image = True

prev_run = 0

while True:

    if first_image:
        first_image = False
        print("Skiping first image")
        time.sleep(5)
        continue

    filename = "./images/camera/camera_" + str(int(time.time())) + ".png"

    # print("Saving image " + filename)

    camera_image = cam.getImage()
    camera_image.save(filename)

    gas = GasMeter(camera_image)
    value = gas.get_meter_value()

    stamp = time.strftime("%d/%m/%Y %I:%M:%S")

    print(camera_image.filename + "\t" + stamp + "\t" + str(value) + "\t" + str(value - prev_run))

    prev_run = value

    sys.stdout.flush()

    time.sleep(5)

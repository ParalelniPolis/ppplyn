#!/usr/bin/python2

from SimpleCV import Camera

import time

from GasMeter import GasMeter

import sys

cam = Camera(0, {"width": 1280, "height": 720})
# v4l2-ctl --set-ctrl brightness=100
# v4l2-ctl --list-ctrls
# v4l2-ctl --info

first_image = True

prev_run = 0

while True:

    if first_image:
        # Skip first image
        first_image = False
        time.sleep(5)
        continue

    image_filename = "camera_" + str(int(time.time())) + ".png"
    filename = "./images/camera/" + image_filename

    # print("Saving image " + filename)

    camera_image = cam.getImage()
    camera_image.save(filename)

    gas = GasMeter(camera_image)
    value = gas.get_meter_value()

    stamp = time.strftime("%d/%m/%Y %H:%M:%S")

    print(image_filename + "\t" + stamp + "\t" + str(value) + "\t" + str(value - prev_run))

    prev_run = value

    sys.stdout.flush()

    time.sleep(5)

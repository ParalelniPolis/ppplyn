#!/usr/bin/python2

from SimpleCV import Camera

import time

cam = Camera(0, {"width": 1280, "height": 720})

while True:

    filename = "./images/camera/camera_" + str(int(time.time())) + ".png"

    print("Saving image " + filename)

    cam.getImage().save(filename)

    time.sleep(5)

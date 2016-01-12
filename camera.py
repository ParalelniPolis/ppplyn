#!/usr/bin/python2

from SimpleCV import Camera

import time

from GasMeter import GasMeter

import sys

cam = Camera(0, {"width": 1280, "height": 720})

first_image = True

prev_run = ""

while True:

    if first_image:
        first_image = False
        print("Skiping first image")
        time.sleep(5)
        continue

    # External 16G USB drive is mounted here
    image_filename = "camera_" + str(int(time.time())) + ".png"
    filename = "./images/camera/" + image_filename

    # print("Saving image " + filename)

    camera_image = cam.getImage()
    camera_image.save(filename)

    gas = GasMeter(camera_image)

    stamp = time.strftime("%d/%m/%Y %H:%M:%S")

    # value is returned as a string. It can have X in the place of unrecognized character
    value = gas.get_meter_value()

    if value.find('X') == -1 and prev_run.find('X') == -1:
        output_line = image_filename + "\t" + stamp + "\t" + str(value) + "\t"
    else:
        output_line = image_filename + "\t" + stamp + "\t" + str(value) + "\t" + "UNKNOWN"

    print(output_line)

    with open('./camera_output.tsv', 'a+') as tsv_file:
        tsv_file.write(output_line + "\n")

    prev_run = value

    sys.stdout.flush()

    time.sleep(5)

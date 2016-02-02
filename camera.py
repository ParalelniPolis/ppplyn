#!/usr/bin/python2

from SimpleCV import Camera

import time

from GasMeter import GasMeter

from secret_key import SECRET_KEY

import requests

import sys

from CHMUWeather import CHMUWeather

cam = Camera(0, {"width": 1280, "height": 720})

first_image = True

prev_run = ""


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


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

    csv_line = []

    csv_line.append(image_filename)
    csv_line.append(stamp)
    csv_line.append(str(value))
    csv_line.append(str(int(time.time())))

    weather = CHMUWeather()

    csv_line.append(str(weather.temperature_air))
    csv_line.append(str(weather.air_pressure))
    csv_line.append(str(weather.air_wind))

    # if value.find('X') == -1:
    #     prev_run = value
    # else:
    #     csv_line.append("UNKNOWN")

    csv_line_str = ";".join(csv_line)

    print(csv_line_str)

    api_data = {
        "data": csv_line_str,
        "key": SECRET_KEY
    }

    api_call = requests.post('http://gas.pavelkral.eu/api.php', data=api_data)

    print("API : " + str(api_call.status_code) + " " + str(api_call.content))

    if value.find('X') == -1:
        # Write only valid values
        with open('./camera_output.tsv', 'a+') as tsv_file:
            tsv_file.write(csv_line_str + "\n")

    sys.stdout.flush()

    time.sleep(5)

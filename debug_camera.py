#!/usr/bin/env python

import csv

from shutil import copy

from os.path import isfile

from datetime import datetime

from collections import OrderedDict

# Text output from camera.py
camera_output_file = "/Users/me/Downloads/camera.txt"

# Where camera.py stored its images
camera_output_directory = "/Users/me/Downloads/camera/"

# Directory where we copy images where detection failed
camera_bug_directory = "/Users/me/Downloads/camera_bug/"

# Reading higher than this are invalid
max_limit = 0.1

valid_data = OrderedDict()


def invalid_row(row):
    """
    Process image with invalid reading
    """

    image_filename, date, reading, reading_diff = row_details(row)

    if isfile(camera_output_directory + image_filename):

        copy(camera_output_directory + image_filename, camera_bug_directory + image_filename)


def valid_row(row):
    """
    Process image with correct reading
    """

    image_filename, date, reading, reading_diff = row_details(row)

    date_stamp = date.strftime("%d/%m/%Y %H:%M")

    if date_stamp not in valid_data:
        valid_data[date_stamp] = []

    valid_data[date_stamp].append(reading)


def row_details(row):

    if "/" in row[0]:
        # Image has full path, not just filename
        image_filename = row[0].split("/")[-1]
    else:
        # Just filename
        image_filename = row[0]

    date = datetime.strptime(row[1], "%d/%m/%Y %H:%M:%S")
    reading = float(row[2])
    reading_diff = float(row[3])

    return (image_filename, date, reading, reading_diff)

with open(camera_output_file, "rb") as csvfile:
    csv_reader = csv.reader(csvfile, delimiter="\t")
    for row in csv_reader:

        image_filename, date, reading, reading_diff = row_details(row)

        if reading_diff < 0 or reading_diff > max_limit:
            invalid_row(row)
        else:
            valid_row(row)


for valid_data_row in valid_data:
    valid_data[valid_data_row] = max(valid_data[valid_data_row])

for valid_data_row in valid_data:
    print(valid_data_row + "\t" + str(valid_data[valid_data_row]))


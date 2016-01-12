#!/usr/bin/env python

import logging
logging.getLogger().setLevel(logging.INFO)

from SimpleCV import ImageSet

import numpy

from TemplateDigitDetector import TemplateDigitDetector
from SVCDigitDetector import SVCDigitDetector

# Simple script for evaluating Digit detectors

svc_detector = SVCDigitDetector()
template_detector = TemplateDigitDetector()

svc_detector_success = []
template_detector_success = []

for test_digit in range(10):

    test_samples = ImageSet("./images/dataset-test/" + str(test_digit))

    for test_sample in test_samples:

        svc_digit = svc_detector.detect_digit(test_sample)
        template_digit = template_detector.detect_digit(test_sample)

        print("svc_digit:" + str(svc_digit) + " template_digit:" + str(template_digit))

        if svc_digit != test_digit:
            svc_detector_success.append(0)
        else:
            svc_detector_success.append(100)

        if template_digit != test_digit:
            template_detector_success.append(0)
        else:
            template_detector_success.append(100)

svc_detector_success_rate = numpy.mean(svc_detector_success)
template_detector_success = numpy.mean(template_detector_success)

print("SVCDigitDetector\t" + str(svc_detector_success_rate) + "%")
print("TemplateDigitDetector\t" + str(template_detector_success) + "%")

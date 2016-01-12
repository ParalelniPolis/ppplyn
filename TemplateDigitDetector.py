

from SimpleCV import Image

from operator import itemgetter

import logging


class TemplateDigitDetector(object):
    """
    Compares digit from the camera with known digits
    """

    def __init__(self):
        pass

    def detect_digit(self, digit_image):
        """
        Which digit is on the image ?
        """

        detected_digits = []

        for digit in range(10):
            template_image = Image("./images/digits/" + str(digit) + ".png").resize(w=digit_image.width, h=digit_image.height)

            diff_image = digit_image - template_image

            diff_index = diff_image.getNumpy().mean()

            detected_digits.append((digit, diff_index))

        sorted_array = sorted(detected_digits, key=itemgetter(1))

        detected_digit = sorted_array[0][0]

        logging.debug("Detected digit " + str(detected_digit))

        return detected_digit

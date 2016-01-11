from SimpleCV import Color

from operator import itemgetter, methodcaller

import cv

# from TemplateDigitDetector import TemplateDigitDetector
from SVCDigitDetector import SVCDigitDetector

from BlobStorage import BlobStorage

import logging


class GasMeter(object):
    """
    Class monitoring gas consumption in Paralelni Polis

    """

    MARKERS_COLOR = (255, 228, 110)
    # Color stickers on the meter
    MARKERS_THRESHOLD = 60
    MARKERS_MINSIZE = 600

    # Once we have fixed perspective, resize to this size
    RESIZE_TO_HEIGHT = 1529
    RESIZE_TO_WIDTH = 2048

    DIGITS_TOP_LEFT = (153, 18)
    DIGITS_BOTTOM_RIGHT = (1458, 270)
    DIGITS_THRESHOLD = 110
    DIGITS_MINSIZE = 1500

    # Our gasmeter measure up to 8 digits and has a decimal point after 5th digit.
    # DIGIT_X_CORDS - x coordinates of each digit on the normalized image
    DIGIT_X_CORDS = [(36, 112),     # 1st
                     (196, 268),    # 2nd
                     (355, 428),    # 3rd
                     (512, 588),    # 4th
                     (669, 743),    # 5th
                     (830, 900),    # 6th
                     (984, 1055),   # 7th
                     (1168, 1236)]  # 8th digit
    DIGITS_WHOLE_CUBIC_METERS = 5
    DIGITS_TOTAL_NUMBER = len(DIGIT_X_CORDS)

    DEBUG = False

    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)

    def __init__(self, image):
        self.image = image

        # self.digit_detector = TemplateDigitDetector()
        self.digit_detector = SVCDigitDetector()

        self.blob_storage = BlobStorage("./images/debug/blobs/")

    def get_meter_value(self):
        """
        Lets read gas meter !
        """

        meter_corners = self.find_meter_corners()

        image_fixed_perspective = self.fix_perspective(meter_corners)

        digits_area = image_fixed_perspective.crop(self.DIGITS_TOP_LEFT, self.DIGITS_BOTTOM_RIGHT).smooth()

        self._save_debug_image(digits_area, "digits_area")

        digits = self.find_digits_in_area_by_cutting(digits_area)

        detected_digits_whole = []
        detected_digits_fraction = []

        for idx, blob in enumerate(digits):

            img_blob = blob.blobImage().binarize(self.DIGITS_THRESHOLD).invert()

            # save image if debugging
            self._save_debug_image(img_blob, "blob" + str(idx))

            # to which list should I save this digit?
            if idx + 1 <= self.DIGITS_WHOLE_CUBIC_METERS:
                save_list = detected_digits_whole
            else:
                save_list = detected_digits_fraction

            # simple check if the blob can be a number
            img_blob_ratio = img_blob.height / float(img_blob.width)

            if img_blob_ratio > 2:

                detected_digit = self.digit_detector.detect_digit(img_blob)

                if detected_digit is not None:
                    save_list.append(str(detected_digit))
                else:
                    save_list.append("X")

            else:
                # if we didn't recognized the last digit we suppose it is 5
                if idx + 1 == self.DIGITS_TOTAL_NUMBER:
                    detected_digits_fraction.append('5')
                else:
                    save_list.append("X")

            # This stores detected blobs (digits) into ./images/debug/blobs/
            # Great for creating datasets. See BlobStorage.py for details
            self.blob_storage.store_blob(img_blob)

        detected_digits_whole_string = "".join(detected_digits_whole)
        detected_digits_fraction_string = "".join(detected_digits_fraction)

        return detected_digits_whole_string + "." + detected_digits_fraction_string

    def find_digits_in_area_by_cutting(self, digits_area):
        """
        Find white digits in given area by cutting the image of the gasmeter to 8 pieces
        and returning the biggest blobs in each of that area
        """

        digits = []

        for digit_i, (x1, x2) in enumerate(self.DIGIT_X_CORDS):
            digit_area = digits_area[x1:x2, :]

            # return only the largest blob which should hopefully be our number
            self._save_debug_image(digit_area, "blobs_my_way" + str(digit_i))
            digit_blob = digit_area.findBlobs(minsize=self.DIGITS_MINSIZE * 2, appx_level=1)
            if digit_blob:
                digits.append(digit_blob[-1])

            logging.debug("Blobbing digit: " + str(digit_i))

        return digits

    def fix_perspective(self, meter_corners):
        """
        Resize gas meter to the whole image with right perspective
        """

        image_top_left = (0, 0)
        image_top_right = (self.image.width, 0)
        image_bottom_left = (0, self.image.height)
        image_bottom_right = (self.image.width, self.image.height)

        image_corners = (image_top_left, image_top_right, image_bottom_right, image_bottom_left)

        # Make transformation matrix
        transform_matrix = cv.CreateMat(3, 3, cv.CV_32FC1)
        cv.GetPerspectiveTransform(meter_corners, image_corners, transform_matrix)

        # Fix gas meter perspective
        fixed_perspective = self.image.transformPerspective(transform_matrix).resize(w=self.RESIZE_TO_WIDTH, h=self.RESIZE_TO_HEIGHT).smooth()

        self._save_debug_image(fixed_perspective, "fixed_perspective")

        return fixed_perspective

    def find_meter_corners(self):
        """
        Find gas meter corners in the image
        """

        # Find color markers on the image
        image_with_markers = self.image.colorDistance(color=self.MARKERS_COLOR).binarize(thresh=self.MARKERS_THRESHOLD)

        markers = image_with_markers.findBlobs(minsize=self.MARKERS_MINSIZE)

        markers.sort(key=methodcaller("area"), reverse=True)

        if len(markers) != 4:
            logging.error("There are not exactly 4 corners !")

        corners = []

        for marker in markers[:4]:

            corners.append(marker.centroid())

            logging.debug("Meter corner " + str(marker.centroid()))

            marker.draw(color=Color.GREEN, width=10)

        self._save_debug_image(image_with_markers, "image_with_markers")

        return self.corners_from_array(corners)

    def corners_from_array(self, array):
        """
        Returns square corners in clockwise order
        TODO : There must be a better way how to do this
        """

        sorted_by_xy = sorted(list(array), key=itemgetter(0, 1))

        # print(sorted_by_xy)

        top_left = sorted_by_xy[0]
        top_right = sorted_by_xy[3]

        bottom_left = sorted_by_xy[1]
        bottom_right = sorted_by_xy[2]

        logging.debug(str([top_left, top_right, bottom_right, bottom_left]))

        return [top_left, top_right, bottom_right, bottom_left]

    def _save_debug_image(self, image, image_name, force_store=False):
        """
        Just stores an image for debugging
        """

        if force_store or self.DEBUG:
            filename = image_name + ".png"
            logging.debug("Storing debug image " + filename)
            image.save("./images/debug/" + filename)

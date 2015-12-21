
from SimpleCV import Color

from operator import itemgetter, attrgetter, methodcaller

import cv

# from TemplateDigitDetector import TemplateDigitDetector
from SVCDigitDetector import SVCDigitDetector

from BlobStorage import BlobStorage

import logging


class GasMeter(object):
    """
    Class monitoring gas consumption in Paralelni Polis

    """

    MARKERS_COLOR = (244, 221, 124)
    # Color stickers on the meter
    MARKERS_THRESHOLD = 50
    MARKERS_MINSIZE = 500

    # Once we have fixed perspective, resize to this size
    RESIZE_TO_HEIGHT = 1529
    RESIZE_TO_WIDTH = 2048

    DIGITS_TOP_LEFT = (153, 18)
    DIGITS_BOTTOM_RIGHT = (1458, 270)
    DIGITS_THRESHOLD = 110
    DIGITS_MINSIZE = 1500

    DEBUG = True

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

        digits = self.find_digits_in_area(digits_area)

        detected_digits = []

        for idx, blob in enumerate(digits):

            # print("blob " + str(blob.area()) + " " + str(blob.meanColor()))

            img_blob = blob.blobImage()

            img_blob_ratio = img_blob.height / float(img_blob.width)

            if img_blob_ratio > 2:
                # Digits is rectangle

                detected_digit = self.digit_detector.detect_digit(img_blob)

                if detected_digit is not None:
                    detected_digits.append(str(detected_digit))

                self.blob_storage.store_blob(img_blob)

        digits_string = "".join(detected_digits).lstrip("0")

        return float(digits_string[0:4] + "." + digits_string[4:6])

    def find_digits_in_area(self, digits_area):
        """
        Find white digits in given area
        """

        white_digits = digits_area.colorDistance(color=Color.WHITE).binarize(self.DIGITS_THRESHOLD)

        self._save_debug_image(white_digits, "white_digits")

        # Fidn digits the area
        digits = white_digits.findBlobs(minsize=self.DIGITS_MINSIZE)

        # Sort digits by X coordinate
        return sorted(digits, key=attrgetter("x"))

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

    def _save_debug_image(self, image, image_name):
        """
        Just stores an image for debugging
        """

        if self.DEBUG:
            filename = image_name + ".png"
            logging.debug("Storing debug image " + filename)
            image.save("./images/debug/" + filename)

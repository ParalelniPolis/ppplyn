
import logging

from SimpleCV import ImageSet

from sklearn.svm import LinearSVC

from os.path import isfile

import pickle


class SVCDigitDetector(object):

    TEMPLATE_SIZE = (10, 40)

    dataset_array = []
    dataset_digit = []

    neural_network = LinearSVC()

    neural_network_cache = "./neural_network.pickle"

    def __init__(self):

        if isfile(self.neural_network_cache):
            logging.debug("Loading neural netowrk from cache")
            cache_file = open(self.neural_network_cache, "rb")
            self.neural_network = pickle.load(cache_file)
        else:
            self.train("./images/dataset/")
            cache_file = open(self.neural_network_cache, "wb+")
            pickle.dump(self.neural_network, cache_file)

        cache_file.close()

    def train(self, digits_path):

        for digit_to_train in range(-1, 10):

            logging.info("Training digit " + str(digit_to_train))

            digit_images = ImageSet(digits_path + str(digit_to_train))

            logging.debug("Loaded " + str(len(digit_images)) + " digits")

            for digit_image in digit_images:

                self.train_image(digit_image, digit_to_train)

            logging.info("Digit " + str(digit_to_train) + " trained")

        self.train_network()

    def train_network(self):

        logging.info("Training the model")

        self.neural_network.fit(self.dataset_array, self.dataset_digit)

    def image_to_array(self, image):

        resiezed_image = image.resize(self.TEMPLATE_SIZE[0], self.TEMPLATE_SIZE[1])

        resiezed_image_numpy = resiezed_image.getNumpy().ravel()

        return resiezed_image_numpy

    def train_image(self, image, digit):

        self.dataset_array.append(self.image_to_array(image))
        self.dataset_digit.append(digit)

    def detect_digit(self, image):

        image_array = self.image_to_array(image).reshape(1, -1)

        name = self.neural_network.predict(image_array)

        if name[0] > 0:
            return name[0]
        else:
            # -1 are invalid blobs
            return None

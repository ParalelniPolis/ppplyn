
import logging

import numpy


class BlobStorage(object):
    """
    Class storing digits for training purposes
    """

    def __init__(self, storage_dir):
        self.storage_dir = storage_dir

    def blob_filename(self, blob):

        image_sum = numpy.sum(blob.getNumpy())

        return image_sum

    def store_blob(self, blob):
        """
        This method is called by GasMeter with a single image to be stored
        """

        store_path = self.storage_dir + "/blobstorage_" + str(self.blob_filename(blob)) + ".png"

        logging.debug("Storing blob " + store_path)

        blob.save(store_path)

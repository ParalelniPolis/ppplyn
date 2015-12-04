
import hashlib

import logging

import numpy

from random import randint


class BlobStorage(object):
    """
    Class storing digits for training purposes
    """

    def __init__(self, storage_dir):
        self.storage_dir = storage_dir

    def blob_filename(self, blob):

        # blob_hash = hashlib.md5(blob.getNumpy())

        # return blob_hash.hexdigest()

        image_sum = numpy.sum(blob.getNumpy())
        
        return image_sum

    def store_blob(self, blob):
        """
        This method is called by GasMeter with a single image to be stored
        """

        blob.save(self.storage_dir + "/blobstorage_" + str(self.blob_filename(blob)) + ".png")

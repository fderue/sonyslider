import os
import logging

LOGGER = logging.getLogger(__name__)

class Camera(object):
    def __init__(self):
        self.camera_name = 'SonyA6000'

    def snap(self):
        cmd = 'irsend SEND_ONCE {} S'.format(self.camera_name)
        try:
            res = os.system(cmd)
        except Exception as e:
            LOGGER.exception(e.__repr__())

        return res

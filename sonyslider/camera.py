import os
import logging
LOGGER = logging.getLogger(__name__)


class Camera(object):
    def __init__(self):
        self.camera_name = 'DSLR1'

    def snap(self):
        LOGGER.info("Sending command irsend")
        cmd = 'irsend SEND_ONCE {} S'.format(self.camera_name)

        res = os.system(cmd)
        if res != 0:
            #raise Exception("Error cmd response:{}".format(res))
            LOGGER.error("Error cmd response:{}".format(res))

        return res

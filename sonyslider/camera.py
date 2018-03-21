import os


class Camera(object):
    def __init__(self):
        self.camera_name = 'SonyA6000'

    def snap(self):
        cmd = 'irsend SEND_ONCE {} S'.format(self.camera_name)
        res = os.system(cmd)
        return res

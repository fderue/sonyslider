from flask import jsonify, Blueprint
from flask_api import status
import time
from sonyslider.slidercontroller import SliderController
from sonyslider.camera import Camera
import logging

LOGGER = logging.getLogger(__name__)

class HyperlapseEngine(object):

    def __init__(self):
        # Space between two shots on the slider [mm]
        self.spatial_step = 0

        # Delay between two shots [s]
        self.time_step = 1

        # Number of shots to take
        self.nb_picture_total = 1
        self.curr_picture_idx = 0

        self.camera = Camera()
        self.slider = SliderController()

    def start(self):
        """
        Start hyperlapse
        shoot - wait (timestep/2) - move - wait(timestep/2)
        :return:
        """
        LOGGER.info("Starting hyperlapse \n "
                    "time step = {0} [s] \n"
                    "spatial step = {1} [mm] \n"
                    "#pictures total = {2}".format(self.time_step, self.spatial_step, self.nb_picture_total))

        delay = self.time_step/2.0
        for image_idx in range(self.nb_picture_total):
            LOGGER.info("Capturing image #{0}/{1}".format(image_idx+1, self.nb_picture_total))
            self.curr_picture_idx = image_idx
            self.camera.snap()
            time.sleep(delay)
            self.slider.translate_forward()
            time.sleep(delay)


    def stop(self):
        LOGGER.info("Stopping hyperlapse")
        self.curr_picture_idx = 0


hyperlapse_engine = HyperlapseEngine()
hyperlapse_blueprint = Blueprint('hyperlapse', __name__)


@hyperlapse_blueprint.route('/hyperlapse/settings/spatialstep', methods=['GET'])
def get_spatialstep_view():
    return jsonify(
        spatialstep=hyperlapse_engine.spatial_step,
    )


@hyperlapse_blueprint.route('/hyperlapse/settings/spatialstep/<value>', methods=['PUT'])
def set_spatialstep_view(value):
    spatial_step = int(value)
    hyperlapse_engine.spatial_step = spatial_step
    return jsonify(
        spatialstep=hyperlapse_engine.spatial_step,
    )


@hyperlapse_blueprint.route('/hyperlapse/settings/timestep', methods=['GET'])
def get_timestep_view():
    return jsonify(
        timestep=hyperlapse_engine.time_step,
    )


@hyperlapse_blueprint.route('/hyperlapse/settings/timestep/<value>', methods=['PUT'])
def set_timestep_view(value):
    time_step = int(value)
    hyperlapse_engine.time_step = time_step
    return jsonify(
        timestep=hyperlapse_engine.time_step,
    )


@hyperlapse_blueprint.route('/hyperlapse/settings/pictures/total', methods=['GET'])
def get_totalpictures_view():
    return jsonify(
        nb_picture_total=hyperlapse_engine.nb_picture_total,
    )


@hyperlapse_blueprint.route('/hyperlapse/settings/pictures/total/<value>', methods=['PUT'])
def set_totalpictures_view(value):
    nb_picture_total = int(value)
    hyperlapse_engine.nb_picture_total = nb_picture_total
    return jsonify(
        nb_picture_total=hyperlapse_engine.nb_picture_total,
    )


@hyperlapse_blueprint.route('/hyperlapse/settings/pictures/current', methods=['GET'])
def get_curr_picture_view():
    return jsonify(
        curr_picture_idx=hyperlapse_engine.curr_picture_idx,
    )


@hyperlapse_blueprint.route('/hyperlapse/command/<cmd>', methods=['PUT'])
def set_command_view(cmd=None):
    if cmd == 'start':
        try:
            hyperlapse_engine.start()
            return status.HTTP_202_ACCEPTED
        except Exception as e:
            content = {'message': e.__repr__()}
            return content
    elif cmd == 'stop':
        hyperlapse_engine.stop()
        return status.HTTP_202_ACCEPTED
    else:
        content = {'message': 'command not found, choose either start or stop'}
        return content, status.HTTP_404_NOT_FOUND


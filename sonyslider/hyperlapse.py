from flask import request, jsonify, Blueprint

class HyperlapseEngine(object):

    def __init__(self):
        # Space between two shots on the slider [mm]
        self.spatial_step = 0

        # Delay between two shots [s]
        self.time_step = 1

        # Number of shots to take
        self.nb_picture_total = 1


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
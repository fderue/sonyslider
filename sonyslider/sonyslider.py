from flask_api import FlaskAPI
from flask import jsonify
from hyperlapse import hyperlapse_blueprint

app = FlaskAPI(__name__)  # create the application instance :)
app.register_blueprint(hyperlapse_blueprint)


@app.route('/')
def home():
    return jsonify(message='Welcome to Sony Slider')


if __name__=='__main__':
    app.run(host='0.0.0.0', port=5003)
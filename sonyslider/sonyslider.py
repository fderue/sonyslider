from flask import Flask
from sonyslider.hyperlapse import hyperlapse_blueprint
app = Flask(__name__) # create the application instance :)
app.register_blueprint(hyperlapse_blueprint)


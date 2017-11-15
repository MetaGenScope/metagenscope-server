"""MetaGenScope server application."""


import os


from flask import Flask, jsonify


from instance.config import app_config


# instantiate the app
app = Flask(__name__)

# set config
config_name = os.getenv('APP_SETTINGS', 'development')
app.config.from_object(app_config[config_name])

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

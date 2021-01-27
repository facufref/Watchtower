from argparse import ArgumentParser
from flask import Flask, jsonify, request, render_template
from ControlTower import ControlTower
import numpy as np

# Instantiate our Node
app = Flask(__name__)

# Instantiate the Miner
controlTower = ControlTower()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check', methods=['POST'])
def check_recording():
    values = request.get_json()
    recording = np.array(values.get('recording'))
    position_lat = values.get('position_lat')
    position_lon = values.get('position_lon')
    controlTower.check_recording(position_lat, position_lon, recording)
    response = {
        'message': 'Received recording'
    }
    return jsonify(response), 200


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5001, type=int, help='port to listen on')
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.port)

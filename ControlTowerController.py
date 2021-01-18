from argparse import ArgumentParser
from flask import Flask, jsonify
from ControlTower import ControlTower

# Instantiate our Node
app = Flask(__name__)

# Instantiate the Miner
controlTower = ControlTower()


@app.route('/hi', methods=['GET'])
def say_hi():
    response = {
        'message': "hi " + controlTower.uuid
    }
    return jsonify(response), 200


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5001, type=int, help='port to listen on')
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.port)

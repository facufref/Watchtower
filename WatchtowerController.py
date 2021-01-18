from argparse import ArgumentParser
from flask import Flask, jsonify
from Watchtower import Watchtower

# Instantiate our Node
app = Flask(__name__)

# Instantiate the Miner
watchtower = Watchtower()


@app.route('/position', methods=['GET'])
def get_position():
    response = {
        'position_lat': watchtower.position_lat,
        'position_lon': watchtower.position_lon,
        'range': watchtower.range
    }
    return jsonify(response), 200


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5001, type=int, help='port to listen on')
    parser.add_argument('-lat', '--lat', default=0, type=float, help='latitude parameter of position')
    parser.add_argument('-lon', '--lon', default=0, type=float, help='longitude parameter of position')
    parser.add_argument('-r', '--range', default=0, type=float, help='range of the mic')
    args = parser.parse_args()
    watchtower.position_lat = args.lat
    watchtower.position_lon = args.lon
    watchtower.range = args.range
    app.run(host='0.0.0.0', port=args.port)

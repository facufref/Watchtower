from argparse import ArgumentParser

from flask import Flask, jsonify

from Watchtower import Watchtower

# Instantiate our Node
app = Flask(__name__)

# Instantiate the Watchtower
watchtower = None


@app.route('/position', methods=['GET'])
def get_position():
    response = {
        'uuid' : watchtower.tower_id,
        'position_lat': watchtower.position_lat,
        'position_lon': watchtower.position_lon,
        'range': watchtower.range
    }
    return jsonify(response), 200


@app.route('/record', methods=['GET'])
def record():
    result = watchtower.record()
    response = {
        'data': result.tolist()
    }
    return jsonify(response), 200


@app.route('/start', methods=['GET'])
def start():
    # TODO: Find a better way, the return never happens
    watchtower.record_forever()
    response = {
        'message': 'Starting to record'
    }
    return jsonify(response), 200


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-id', '--id', default=5002, type=str, help='Tower id')
    parser.add_argument('-p', '--port', default=5002, type=int, help='port to listen on')
    parser.add_argument('-lat', '--lat', default=0, type=float, help='latitude parameter of position')
    parser.add_argument('-lon', '--lon', default=0, type=float, help='longitude parameter of position')
    parser.add_argument('-r', '--range', default=50, type=int, help='range of the tower')
    parser.add_argument('-s', '--save', default=0, type=bool, help='if the recording should be saved or not')
    args = parser.parse_args()
    watchtower = Watchtower(args.id, args.lat, args.lon, args.port, args.range, args.save)
    app.run(host='0.0.0.0', port=args.port)

from argparse import ArgumentParser
from flask import Flask, jsonify, request, render_template, Response
from pykafka import KafkaClient

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
    tower_id = values.get('uuid')
    position_lat = values.get('position_lat')
    position_lon = values.get('position_lon')

    controlTower.check_recording(tower_id, position_lat, position_lon, recording)
    controlTower.produce_checkpoint()

    response = {
        'message': 'Received recording'
    }
    return jsonify(response), 200


@app.route('/topic/<topicname>')
def get_messages(topicname):
    client = KafkaClient(hosts='127.0.0.1:9092')

    def events():
        for i in client.topics[topicname].get_simple_consumer():
            yield 'data:{0}\n\n'.format(i.value.decode())

    return Response(events(), mimetype="text/event-stream")


@app.route('/clean', methods=['GET'])
def delete_old_towers():
    controlTower.delete_old_towers()

    response = {
        'message': 'Old towers deleted'
    }
    return jsonify(response), 200


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5001, type=int, help='port to listen on')
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.port)

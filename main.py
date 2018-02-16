#!/usr/bin/env python

import os
import optparse
import nest
import nest_apps.simple_network as simple

from flask import Flask, request, jsonify
app = Flask(__name__)


# --------------------------
# General request
# --------------------------

@app.route('/', methods=['GET'])
def index():
    response = {
        'name': 'NEST server simulation',
        'version': nest.version().split(' ')[1],
        'ref': 'http://www.github.com/babsey/nest-server-simulation',
        'env': dict(filter(lambda item: 'NEST' in item[0], os.environ.items()))
    }
    return jsonify(response)


# --------------------------
# NEST simulation request
# --------------------------

def simulate(simulation, data):
    # print(data)
    try:
        response = {'data': simulation(data)}
    except Exception as e:
        response = {'error': str(e)}
    return jsonify(response)


@app.route('/network/simple/simulate', methods=['POST'])
def simple_network_simulate():
    return simulate(simple.simulate, request.get_json())


@app.route('/network/simple/resume', methods=['POST'])
def simple_network_resume():
    return simulate(simple.resume, request.get_json())


if __name__ == "__main__":
    parser = optparse.OptionParser("usage: python main.py [options]")
    parser.add_option("-H", "--host", dest="hostname",
                      default="127.0.0.1", type="string",
                      help="specify hostname to run on")
    parser.add_option("-p", "--port", dest="port", default=5000,
                      type="int", help="port to run on")
    (options, args) = parser.parse_args()
    app.run(host=options.hostname, port=options.port)

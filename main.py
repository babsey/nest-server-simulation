#!/usr/bin/env python

import nest_apps.simple_network as simple

from flask import Flask, request, jsonify
app = Flask(__name__)


def run(simulation, data):
    local_num_threads = 4
    try:
        response = {'data': simulation(data, local_num_threads)}
    except Exception as e:
        response = {'error': str(e)}
    return jsonify(response)


# --------------------------
# General requests
# --------------------------


@app.route('/', methods=['GET'])
def index():
    return 'Hello World!'


@app.route('/versions', methods=['GET'])
def versions():
    req = {}
    try:
        import nest
        nest = nest.version()
    except:
        pass
        nest = 'failed'

    return jsonify(nest=nest)


# --------------------------
# NEST applications
# --------------------------


@app.route('/network/simple/simulate', methods=['POST'])
def simple_network_simulate():
    return run(simple.simulate, request.get_json())


@app.route('/network/simple/resume', methods=['POST'])
def simple_network_resume():
    return run(simple.resume, request.get_json())


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        app.run(sys.argv[1])
    else:
        app.run()

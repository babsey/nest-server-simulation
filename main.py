#!/usr/bin/env python

from flask import Flask, request, jsonify
app = Flask(__name__)

def run(simulation, data):
    local_num_threads = 4
    try:
        response = {'data': simulation(data, local_num_threads)}
    except Exception, e:
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

import nest_apps.simple_network as simple
@app.route('/network/simple/simulate', methods=['POST'])
def simple_network_simulate():
    return run(simple.simulate, request.get_json())

@app.route('/network/simple/resume', methods=['POST'])
def simple_network_resume():
    return run(simple.resume, request.get_json())

import nest_apps.gamma_network as gamma
@app.route('/network/gamma/simulate', methods=['POST'])
def gamma_network_simulate():
    return run(gamma.simulate, request.get_json())

@app.route('/network/gamma/resume', methods=['POST'])
def gamma_network_resume():
    return run(gamma.resume, request.get_json())

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        app.run(sys.argv[1])
    else:
        app.run()

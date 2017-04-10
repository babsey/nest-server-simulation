#!/usr/bin/env python

from flask import Flask, request, jsonify
app = Flask(__name__)

local_num_threads = 4

# --------------------------
# General requests
# --------------------------

@app.route('/', methods=['GET'])
def index():
    return 'Hello World!'

@app.route('/versions', methods=['GET'])
def ersions():
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
    data = request.get_json()
    return jsonify(simple.simulate(data, local_num_threads))

@app.route('/network/simple/resume', methods=['POST'])
def simple_network_resume():
    data = request.get_json()
    return jsonify(simple.resume(data))


import nest_apps.gamma_network as gamma
@app.route('/network/gamma/simulate', methods=['POST'])
def gamma_network_simulate():
    data = request.get_json()
    return jsonify(gamma.simulate(data, local_num_threads))

@app.route('/network/gamma/resume', methods=['POST'])
def gamma_network_resume():
    data = request.get_json()
    return jsonify(gamma.resume(data))

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        app.run(sys.argv[1])
    else:
        app.run()

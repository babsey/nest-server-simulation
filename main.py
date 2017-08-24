#!/usr/bin/env python

import re
import sys
import nest_apps.simple_network as simple

from flask import Flask, request, jsonify
app = Flask(__name__)


def is_valid_ip(ip):
    # https://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python
    m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
    # m = re.match(r"^(\d{1,3}\.){3}\d{1,3}$", ip)
    return bool(m) and all(map(lambda n: 0 <= int(n) <= 255, m.groups()))

# --------------------------
# General request
# --------------------------

@app.route('/', methods=['GET'])
def index():
    return 'Hello World!'


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


if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 5000
    if len(sys.argv) > 1:
        host = sys.argv[1]
        if ':' in host:
            ip, port = host.split(':')
        else:
            ip = host
    # print('%s:%s' %(ip,port))
    assert is_valid_ip(ip)
    app.run(host=ip, port=int(port))

#!/usr/bin/env python

from flask import Flask, jsonify, request
import nest

app = Flask(__name__)

@app.route('/simulate/', methods=['POST'])
def simulate():
    nest.ResetKernel()

    nest.SetKernelStatus({'local_num_threads':4})

    data = request.get_json()
    nodes = data['nodes']
    nodes['neuron']['params'] = dict(zip(nodes['neuron']['params'].keys(), map(float, nodes['neuron']['params'].values())))
    nodes['input']['params'] = dict(zip(nodes['input']['params'].keys(), map(float, nodes['input']['params'].values())))

    npop = 500
    pop = nest.Create(nodes['neuron']['model'], npop, params=nodes['neuron']['params'])
    popE,popI = pop[:int(npop*.8)],pop[int(npop*.8):]
    noise = nest.Create('noise_generator')
    input = nest.Create(nodes['input']['model'], params=nodes['input']['params'])

    sd = nest.Create('spike_detector')

    nest.Connect(input,pop)
    # nest.Connect(pop[::5],sd)
    nest.Connect(pop,sd)

    nest.SetStatus(noise, {'std':1000.})
    nest.Simulate(100.)
    nest.SetStatus(noise, {'std':0.})
    events = nest.GetStatus(sd,'events')[0]

    p = .1
    nest.Connect(popE,pop,
        # conn_spec={'rule': 'fixed_outdegree', 'outdegree': int(p*npop), 'autapses': False, 'multapses': True},
        conn_spec={'rule': 'fixed_indegree', 'indegree': int(p*npop), 'autapses': False, 'multapses': True},
        syn_spec={'weight':10.})
    nest.Connect(popI,pop,
        # conn_spec={'rule': 'fixed_outdegree', 'outdegree': int(p*npop), 'autapses': False, 'multapses': True},
        conn_spec={'rule': 'fixed_indegree', 'indegree': int(p*npop), 'autapses': False, 'multapses': True},
        syn_spec={'weight':-40.})

    nest.Simulate(data['sim_time'])
    time = nest.GetKernelStatus('time')

    events = nest.GetStatus(sd,'events')[0]
    nest.SetStatus(sd, {'n_events': 0})

    events = dict(map(lambda (x,y): (x,y.tolist()), events.items()))
    return jsonify(events=events, time=time, pop=pop)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        app.run(sys.argv[1])
    else:
        app.run()

#!/usr/bin/env python
import numpy as np
import nest

import lib.paramify as paramify
import lib.lcrn_network as lcrn

def simulate(data, local_num_threads=1):
    # print data
    np.random.seed(int(data['kernel'].get('grng_seed', 0)))

    nest.ResetKernel()
    nest.SetKernelStatus({
        'local_num_threads': local_num_threads,
        'grng_seed': int(data['kernel'].get('grng_seed', 0)),
        'rng_seeds': np.random.randint(0,1000,local_num_threads).tolist(),
    })

    nodes = data['nodes']
    input = nest.Create(nodes[0]['model'], params=paramify.simulate(nodes[0]))
    data['nodes'][0]['ids'] = input

    nrow = int(nodes[1]['nrow'])
    ncol = int(nodes[1]['ncol'])
    n = nrow*ncol
    neuron = nest.Create(nodes[1]['model'], int(n), params=paramify.simulate(nodes[1]))
    data['nodes'][1]['ids'] = neuron

    sd = nest.Create('spike_detector')
    data['nodes'][2]['ids'] = sd

    source, target, conn_spec, syn_spec = paramify.link(data['links'][0])
    nest.Connect(input, neuron, conn_spec = conn_spec, syn_spec = syn_spec)

    source, target, conn_spec, syn_spec = paramify.link(data['links'][1])
    outdegree = conn_spec['outdegree']
    offset = neuron[0]
    for ii in range(n):
        targets, delay = lcrn.lcrn_gamma_targets(ii, nrow, ncol, nrow, ncol, int(outdegree), 4, 3)
        nest.Connect([neuron[ii]], (targets+offset).tolist(), conn_spec = conn_spec, syn_spec = syn_spec)

    nest.Connect(neuron,sd)

    nest.Simulate(float(data['sim_time']))
    data['kernel']['time'] = nest.GetKernelStatus('time')

    events = nest.GetStatus(sd,'events')[0]
    data['nodes'][2]['events'] = dict(map(lambda (x,y): (x,y.tolist()), events.items()))
    nest.SetStatus(sd, {'n_events': 0})

    return data

def resume(data, local_num_threads=1):

    nodes = data['nodes']
    nest.SetStatus(nodes[0]['ids'], paramify.resume(nodes[0]))

    nest.Simulate(float(data['sim_time']))
    data['kernel']['time'] = nest.GetKernelStatus('time')

    events = nest.GetStatus(nodes[2]['ids'],'events')[0]
    nodes[2]['events'] = dict(map(lambda (x,y): (x,y.tolist()), events.items()))
    nest.SetStatus(nodes[2]['ids'], {'n_events': 0})

    return data

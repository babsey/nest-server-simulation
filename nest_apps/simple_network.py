#!/usr/bin/env python
import numpy as np
import nest

import lib.paramify as paramify

def simulate(data):
    # print data
    nest.ResetKernel()

    np.random.seed(int(data['kernel'].get('grng_seed', 0)))
    nest.SetKernelStatus({
        'local_num_threads': 4,
        'grng_seed': np.random.randint(0,1000),
        'rng_seeds': np.random.randint(0,1000,4).tolist(),
    })

    outputs = []
    for idx, node in enumerate(data['nodes']):
        if node.get('disabled', False): continue
        if not node.get('model', False): continue
        if len(node['model']) == 0: continue

        if node['model'] == 'multimeter':
            links = filter(lambda link: link['target'] == idx, data['links'])
            recordables = []
            for link in links:
                recorded_neuron = data['nodes'][link['source']]
                recordables.extend(map(lambda rec: rec.name, nest.GetStatus(recorded_neuron['ids'],'recordables')[0]))
            node['params'].update({'record_from': recordables})
        params = paramify.simulate(node)
        data['nodes'][idx]['ids'] = nest.Create(node['model'], int(node.get('n',1)), params=params)
        if node['type'] == 'output':
            outputs.append((idx, data['nodes'][idx]['ids']))

    for link in data['links']:
        if link.get('disabled', False): continue
        if data['nodes'][link['source']].get('disabled', False): continue
        if data['nodes'][link['target']].get('disabled', False): continue
        if not data['nodes'][link['source']].get('ids', False): continue
        if not data['nodes'][link['target']].get('ids', False): continue

        source = data['nodes'][link['source']]['ids']
        target = data['nodes'][link['target']]['ids']
        syn_spec = link.get('syn_spec',{'weight': 1.})
        syn_spec = paramify.syn(syn_spec)
        if data['nodes'][link['target']]['model'] in ['voltmeter','multimeter']:
            nest.Connect(target, source, conn_spec=link.get('conn_spec','all_to_all'), syn_spec=syn_spec)
        else:
            nest.Connect(source, target, conn_spec=link.get('conn_spec','all_to_all'), syn_spec=syn_spec)

    nest.Simulate(float(data['sim_time']))
    data['kernel']['time'] = nest.GetKernelStatus('time')

    for idx, output in outputs:
        events = nest.GetStatus(output,'events')[0]
        data['nodes'][idx]['events'] = dict(map(lambda (x,y): (x,y.tolist()), events.items()))
        nest.SetStatus(output, {'n_events': 0})

    return data


def resume(data):
    # print data
    outputs = []
    for idx, node in enumerate(data['nodes']):
        if not 'ids' in node: continue
        if len(node['ids']) == 0: continue
        nest.SetStatus(node['ids'], params=paramify.resume(node))
        if node['type'] == 'output':
            outputs.append((idx, data['nodes'][idx]['ids']))

    # for link in data['links']:
    #     syn_spec = link.get('syn_spec',{'weight': 1.})
    #     syn_spec = dict(zip(syn_spec.keys(), map(float, syn_spec.values())))
    #     source = data['nodes'][link['source']]['ids']
    #     target = data['nodes'][link['target']]['ids']
    #     nest.SetStatus(nest.GetConnections(source,target))

    nest.Simulate(float(data['sim_time']))
    data['kernel']['time'] = nest.GetKernelStatus('time')

    for idx, output in outputs:
        events = nest.GetStatus(output,'events')[0]
        data['nodes'][idx]['events'] = dict(map(lambda (x,y): (x,y.tolist()), events.items()))
        nest.SetStatus(output, {'n_events': 0})

    return data

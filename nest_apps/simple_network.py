#!/usr/bin/env python
import numpy as np
import nest

from .lib import paramify


def simulate(data):
    print('Simulate %s' %data.get('id', None))

    # print('Set kernel')
    nest.ResetKernel()
    np.random.seed(int(data.get('random_seed', 0)))
    local_num_threads = int(data['kernel'].get('local_num_threads', 1))
    nest.SetKernelStatus({
        'local_num_threads': local_num_threads,
        'rng_seeds': np.random.randint(0, 1000, local_num_threads).tolist(),
        'resolution': float(data['kernel'].get('resolution', 1.0)),
    })

    nodes = data['nodes']
    links = data['links']

    recorders = []
    # print('Create nodes')
    for idx, node in enumerate(nodes):
        if node.get('disabled', False):
            continue
        if not node.get('model', False):
            continue
        nodes[idx]['ids'] = nest.Create(node['model'], int(node.get('n', 1)))
        if node['element_type'] == 'recorder':
            recorders.append((idx, nodes[idx]['ids']))

    # print('Set parameters for nodes')
    for idx, node in enumerate(nodes):
        if len(node.get('ids', [])) == 0:
            continue
        if node['model'] == 'multimeter':
            rec_links = filter(lambda link: link['target'] == idx, links)
            recordables = []
            for link in rec_links:
                recorded_neuron = nodes[link['source']]
                recordables.extend(map(
                    lambda rec: rec.name,
                    nest.GetStatus(recorded_neuron['ids'], 'recordables')[0]))
            recordables = sorted(list(set(recordables)))
            node['params'].update({'record_from': recordables})

        if len(node.get('params', {})) == 0:
            continue
        nest.SetStatus(node['ids'], params=paramify.simulate(node))

    # print('Connect nodes')
    for link in data['links']:
        if link.get('disabled', False):
            continue
        if nodes[link['source']].get('disabled', False):
            continue
        if nodes[link['target']].get('disabled', False):
            continue
        if not nodes[link['source']].get('ids', False):
            continue
        if not nodes[link['target']].get('ids', False):
            continue
        source, target, conn_spec, syn_spec = paramify.link(link)
        if nodes[link['target']]['model'] in ['voltmeter', 'multimeter']:
            source, target = target, source
            if type(conn_spec) == dict:
                if conn_spec['rule'] == 'fixed_indegree':
                    conn_spec['rule'] = 'fixed_outdegree'
                    conn_spec['outdegree'] = conn_spec['indegree']
                    del conn_spec['indegree']
        nest.Connect(
            nodes[source]['ids'], nodes[target]['ids'], conn_spec=conn_spec,
            syn_spec=syn_spec)

    # print('Simulate')
    nest.Simulate(float(data['sim_time']))
    data['kernel']['time'] = nest.GetKernelStatus('time')

    # print('Get record data')
    for idx, recorder in recorders:
        events = nest.GetStatus(recorder, 'events')[0]
        nodes[idx]['events'] = dict(
            map(lambda X: (X[0], X[1].tolist()), events.items()))
        nest.SetStatus(recorder, {'n_events': 0})

    return data


def resume(data):
    print('Resume %s' %data.get('id', None))

    recorders = []
    for idx, node in enumerate(data['nodes']):
        if len(node.get('ids', [])) == 0:
            continue
        if node['element_type'] != 'recorder':
            nest.SetStatus(node['ids'], params=paramify.resume(node))
        else:
            recorders.append((idx, node['ids']))

    # for link in data['links']:
    #     if link.get('disabled', False): continue
    #     if data['nodes'][link['source']].get('disabled', False): continue
    #     if data['nodes'][link['target']].get('disabled', False): continue
    #     if data['nodes'][link['target']]['model'] == 'recorder': continue
    #     if not data['nodes'][link['source']].get('ids', False): continue
    #     if not data['nodes'][link['target']].get('ids', False): continue
    #     source = data['nodes'][link['source']]['ids']
    #     target = data['nodes'][link['target']]['ids']
    #     syn_spec = link.get('syn_spec',{'weight': 1.})
    #     nest.SetStatus(nest.GetConnections(source,target),syn_spec)

    nest.Simulate(float(data['sim_time']))
    data['kernel']['time'] = nest.GetKernelStatus('time')

    for idx, recorder in recorders:
        events = nest.GetStatus(recorder, 'events')[0]
        data['nodes'][idx]['events'] = dict(
            map(lambda X: (X[0], X[1].tolist()), events.items()))
        nest.SetStatus(recorder, {'n_events': 0})

    return data

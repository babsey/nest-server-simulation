import numpy as np
import nest

def simulate(node):
    params = {}
    if len(node['params']) > 0:
        param_defaults = nest.GetDefaults(node['model'])
        for pkey,pval in node['params'].items():
            if pkey in param_defaults:
                ptype = type(param_defaults[pkey])
                if ptype == np.ndarray:
                    params[pkey] = np.array(pval, dtype=param_defaults[pkey].dtype)
                else:
                    params[pkey] = ptype(pval)
    return params


def resume(node):
    params = simulate(node)
    if node['type'] == 'neuron':
        param_defaults = nest.GetDefaults(node['model'])
        recordables = param_defaults['recordables']
        for recordable in recordables:
            if recordable.name in params:
                del params[recordable.name]
    if ((node['model'] == 'multimeter') and ('record_from' in params)):
        del params['record_from']
    return params

def syn(syn_spec):
    if len(syn_spec) > 0:
        param_defaults = nest.GetDefaults(syn_spec.get('model', 'static_synapse'))
        for pkey,pval in syn_spec.items():
            if pkey in param_defaults:
                syn_spec[pkey] = type(param_defaults[pkey])(pval)
    return syn_spec

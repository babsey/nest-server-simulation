import nest

def simulate(node):
    param_defaults = nest.GetDefaults(node['model'])
    params = {}
    if len(node['params']) > 0:
        for pkey,pval in node['params'].items():
            if pkey in param_defaults:
                params[pkey] = type(param_defaults[pkey])(pval)
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

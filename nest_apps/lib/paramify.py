import numpy as np
import nest


def _paramify(params, param_defaults):
    _params = {}
    for pkey, pval in params.items():
        if pkey == 'model':
            _params[pkey] = pval
        elif isinstance(pval, dict):
            _params[pkey] = _paramify(pval, param_defaults[pkey])
        elif pkey in param_defaults:
            ptype = type(param_defaults[pkey])
            if ptype == np.ndarray:
                _params[pkey] = np.array(
                pval, dtype=param_defaults[pkey].dtype)
            else:
                _params[pkey] = ptype(pval)
    return _params


def simulate(node):
    params = node.get('params', {})
    param_defaults = nest.GetDefaults(node['model'])
    params = _paramify(params, param_defaults)
    return params


def resume(node):
    params = simulate(node)
    if node['element_type'] == 'neuron':
        param_defaults = nest.GetDefaults(node['model'])
        recordables = param_defaults['recordables']
        for recordable in recordables:
            if recordable.name in params:
                del params[recordable.name]
    if ((node['model'] == 'multimeter') and ('record_from' in params)):
        del params['record_from']
    return params


def link(link):
    source, target = link['source'], link['target']
    conn_spec = link.get('conn_spec', 'all_to_all')
    if len(conn_spec) == 0:
        conn_spec = 'all_to_all'
    syn_spec = link.get('syn_spec', {'weight': 1.})
    if len(syn_spec) > 0:
        param_defaults = nest.GetDefaults(
            syn_spec.get('model', 'static_synapse'))
        syn_spec = _paramify(syn_spec, param_defaults)
        # for pkey,pval in syn_spec.items():
        #     if pkey in param_defaults:
        #         syn_spec[pkey] = type(param_defaults[pkey])(pval)
    return source, target, conn_spec, syn_spec

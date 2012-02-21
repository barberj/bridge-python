import random
import string

import reference

class AuxError(Exception):
    pass

def serialize(bridge, obj):
    if hasattr(obj, '__call__'):
        return serialize_func(bridge, obj)
    elif isinstance(obj, reference.Ref):
        return obj._to_dict()
    elif is_service(obj):
        # XXX: Duplicate code.
        name = gen_guid()
        chain = ['client', bridge.get_client_id(), name]
        ref = reference.LocalRef(bridge, chain, obj)
        obj._ref = ref
        bridge._children[name] = obj
        return ref._to_dict()
    else:
        for container, key, val in deep_scan(obj, atomic_matcher):
            container[key] = serialize(bridge, val)
        return obj

def is_service(obj):
    return isinstance(obj, reference.Service) or \
           issubclass(obj, reference.Service)

def atomic_matcher(key, val):
    return isinstance(val, reference.Ref) or \
           is_service(val) or hasattr(val, '__call__')

def serialize_func(bridge, func):
    # XXX: Duplicate code.
    name = gen_guid()
    chain = ['client', bridge.get_client_id(), name, 'callback']
    ref = reference.LocalRef(bridge, chain, reference.Service())
    service = ref._service
    service._ref = ref
    service.callback = func
    bridge._children[name] = service
    return ref._to_dict()

def gen_guid():
    return ''.join([
        random.choice(string.ascii_letters) for k in range(32)
    ])

def parse_server_cmd(bridge, obj):
    chain = obj['destination']['ref']
    args = deserialize(bridge, obj['args'])
    service = reference.get_service(bridge, chain)
    print(bridge._children)
    return service._ref, args

def deserialize(bridge, obj):
    for container, key, ref in deep_scan(obj, ref_matcher):
        chain = ref['ref']
        print('deserialize: chain =', chain)
        service = reference.get_service(chain)
        if not service:
            ops = ref.get('operations', [])
            service = reference.RemoteService(ops)
            service._ref = reference.RemoteRef(bridge, chain, service)
            name = chain[reference.SERVICE]
            bridge._children[name] = service
        container[key] = service._ref
    return obj

def ref_matcher(key, val):
    return type(val) == dict and 'ref' in val

def deep_scan(obj, matcher):
    iterator = []
    if type(obj) is dict:
        iterator = obj
    elif type(obj) is list:
        iterator = enumerate(obj)
    for key, val in iterator:
        if matcher(key, val):
            yield obj, key, val
        else:
            for result in deep_scan(val, matcher):
                yield result

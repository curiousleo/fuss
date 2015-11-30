_WIRE_FILE = 'wire.txt'
_SERVICES = open(_WIRE_FILE).read().strip().lower().split('\n')

def iswire(name):
    if not isinstance(name, str):
        return false
    name = name.strip().lower()
    return len(name) > 2 and any(s.startswith(name) for s in _SERVICES)

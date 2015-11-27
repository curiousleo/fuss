def memoize(attr):
    def _memoize(f):
        def wrapper(self, *args):
            try:
                return getattr(self, attr)
            except AttributeError:
                setattr(self, attr, f(self, *args))
                return getattr(self, attr)
        return wrapper
    return _memoize

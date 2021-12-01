import typing


_services = {}


def register(name: str, service: typing.Any):
    if name in _services:
        raise ValueError("Service '{}' is already registered".format(name))
    _services[name] = service


def get(name: str):
    if name not in _services:
        raise ValueError("Service '{}' is not registered".format(name))
    return _services[name]


def unregister(name: str):
    _services.pop(name)

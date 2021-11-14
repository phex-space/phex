class Access(object):
    def __init__(self, scope: str, resource: str):
        self.__scope = scope
        self.__resource = resource
        self.__repr = f"{self.resource}#{self.scope}"

    def __repr__(self):
        return self.__repr

    @property
    def scope(self):
        return self.__scope

    @property
    def resource(self):
        return self.__resource

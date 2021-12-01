from io import StringIO


class Access(object):
    def __init__(self, scope: str, resource: str):
        self.__scope = scope
        self.__resource = resource
        self.__str = f"{self.resource}#{self.scope}"

    @property
    def scope(self):
        return self.__scope

    @property
    def resource(self):
        return self.__resource

    def __str__(self):
        return self.__str

    def __repr__(self):
        buffer = StringIO()
        buffer.write("Access(scope=\"")
        buffer.write(self.scope)
        buffer.write("\", resource=\"")
        buffer.write(self.resource)
        buffer.write("\")")
        return buffer.getvalue()

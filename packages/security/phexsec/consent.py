from io import StringIO


class Consent(object):
    def __init__(self, requests_access=None, permissions=None):
        if requests_access is None:
            requests_access = []
        if permissions is None:
            permissions = []

        for access in requests_access:
            setattr(self, f"can_{access.scope}_{access.resource}", False)
        for permission in permissions:
            resource_name = permission["rsname"]
            scopes = permission["scopes"]
            for scope in scopes:
                setattr(self, f"can_{scope}_{resource_name}", True)

    def __repr__(self):
        buffer = StringIO()
        buffer.write("Consent(")
        first = False
        for attr, value in self.__dict__.items():
            if attr.startswith("can_"):
                if first:
                    buffer.write(", ")
                buffer.write(attr)
                buffer.write("=")
                buffer.write(str(value))
                first = True
        buffer.write(")")
        return buffer.getvalue()

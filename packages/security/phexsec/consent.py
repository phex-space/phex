from io import StringIO


class Consent(object):
    def __init__(self, requests_access=None, permissions=None):
        for access in requests_access:
            setattr(self, f"can_{access.scope}_{access.resource}", False)
        for permission in permissions:
            resource_name = permission["rsname"]
            scopes = permission["scopes"]
            for scope in scopes:
                setattr(self, f"can_{scope}_{resource_name}", True)

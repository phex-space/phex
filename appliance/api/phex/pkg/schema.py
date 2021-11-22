from typing import Optional

from phex.mongodb import PhexBaseModel


class Package(PhexBaseModel):
    name: str
    version: Optional[str]
    status: str = "created"

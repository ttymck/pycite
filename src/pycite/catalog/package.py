"""The package class defining a python module, application or library
"""
from enum import Enum
from dataclasses import dataclass

PackageType = Enum("PackageType", ["GIT", "PYPI"])


@dataclass
class Package:
    type: PackageType
    name: str
    uri: str

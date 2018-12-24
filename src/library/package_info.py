"""The package class defining a python module, application or library
"""
from dataclasses import dataclass 

@dataclass
class PackageInfo:
    name: str
    repo_url: str

from typing import List
from abc import ABC, abstractmethod

from .package_info import PackageInfo

class Library(ABC):
    """A library of python packages/modules for analysis
    """
    def __init__(self):
        self._projects = self._load_library()
        
    @abstractmethod
    def _load_library(self) -> List[PackageInfo]:
        pass
    
    def __iter__(self):
        for project in self._projects:
            yield project
            
    def __getitem__(self,  index):
        return self._projects[index]
    
    def __len__(self):
        return len(self._projects)
        
    def items(self):
        for project in self._projects:
            yield (project.name,  project.repo_url)
    
    def keys(self):
        for project in self._projects:
            yield project.name
    
    def urls(self):
        for project in self._projects:
            yield project.repo_url


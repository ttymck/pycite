from typing import List
from abc import ABC, abstractmethod
from ruamel.yaml import YAML
import requests

import requests_cache

requests_cache.install_cache('web_cache',  backend='sqlite',  expire_after=60*20)
yaml = YAML()

class PackageInfo:
    def __init__(self,  name: str,  repo: str):
        self.name = name
        self.repo = repo

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
        return list(self)[index]
    
    def __len__(self):
        return len(self._projects)
        
    def items(self):
        for project in self._projects:
            yield (project.name,  project.url)
    
    def keys(self):
        for project in self._projects:
            yield project.name

@Library.register        
class APA(Library):
    """Awesome Python Applications list, curated by 
    @mahmoud (Mahmoud Hashemi): https://github.com/mahmoud/awesome-python-applications
    """
    library_url = "https://raw.githubusercontent.com/mahmoud/awesome-python-applications/master/projects.yaml" # yaml file of package list
    def __init__(self):
        super().__init__()
    
    def __repr__(self):
        return "apa library"
    
    def _load_library(self) -> List[PackageInfo]:
        projects = self._read_projects_list()
        project_info = []
        for project in projects:
            info = PackageInfo(project.get("name"),  project.get("repo_url"))
            project_info.append(info)
        return project_info
        
    def _read_projects_list(self):
        projects_file_request = requests.get(self.library_url)
        projects_file = projects_file_request.text 
        projects = yaml.load(projects_file).get("projects")
        return projects
        
        

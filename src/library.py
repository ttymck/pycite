from typing import List
from abc import ABC, abstractmethod
from ruamel.yaml import YAML
import requests

from .config import Config

logger = Config.getLogger("library")

import requests_cache

requests_cache.install_cache('web_cache',  backend='sqlite',  expire_after=60*20)
yaml = YAML()

class PackageInfo:
    def __init__(self,  name: str,  repo_url: str):
        self.name = name
        self.repo_url = repo_url

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
        projects = self._read_projects_list(self.library_url)
        project_info = []
        for project in projects:
            info = PackageInfo(project.get("name"),  project.get("repo_url"))
            project_info.append(info)
        return project_info
        
    def _read_projects_list(self,  projects_list_url):
        logger.debug("downloading APA yaml from: %s",  projects_list_url)
        projects_file_request = requests.get(projects_list_url)
        projects_file = projects_file_request.text 
        projects = yaml.load(projects_file).get("projects")
        return projects
        
        

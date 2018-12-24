from typing import List
from ruamel.yaml import YAML
import requests
import requests_cache

from src.config import Config
from .package_info import PackageInfo
from .library import Library

logger = Config.getLogger("library")

requests_cache.install_cache('web_cache',  backend='sqlite',  expire_after=60*20)
yaml = YAML()

@Library.register        
class APA(Library):
    """Awesome Python Applications list, curated by 
    @mahmoud (Mahmoud Hashemi): https://github.com/mahmoud/awesome-python-applications
    """
    # yaml API
    library_url = "https://raw.githubusercontent.com/mahmoud/awesome-python-applications/master/projects.yaml" 
    
    def __init__(self):
        super().__init__()
    
    def __repr__(self):
        return "<APA Library>"
    
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

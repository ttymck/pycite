from pathlib import Path
import glob
from typing import List
import git
from .config import Config

class GitProject:
    """A project made available via git
    """
    cache_dir = Path.home() / ".cache" / Config.app_name
    def __init__(self, name: str,  url: str):
        self.name = name
        self.url = url
        self.dest_path = self.cache_dir / name
        self._fetch()
        
    def _fetch(self):
        self.cache_dir.mkdir(exist_ok=True)
        # if it exists in the cache, pull changes
        if self.dest_path.exists():
            git.Repo(self.dest_path).pull()
        # otherwise, need to clone into cache
        else:
            git.Repo.clone_from(self.url,  self.dest_path,  branch="master")
        
class GitLibrary():
    """A collection of GitProjects
    """
    def __init__(self,  library):
        self.projects = self._load_git_projects_from_library(library)
        
    def _load_git_projects_from_library(self,  library) -> List[GitProject]:
        return [GitProject(*args) for args in library.items()]
    
    def py_file_count(self) -> int:
        count = 0
        for project in self.projects:
            py_files = project.glob('**/*.py')
            count += len(py_files)
        return count

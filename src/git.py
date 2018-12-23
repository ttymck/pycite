from pathlib import Path
import git
from config import Config

class GitProject:
    """A project made available via git
    """
    cache_dir = Path.home() / ".cache" / Config.app_name
    def __init__(self, name: str,  url: str):
        self.name = name
        self.url = url
        self.dest_path = self.cache_dir / name
        
    def _clone(self):
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
    
    

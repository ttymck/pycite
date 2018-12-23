import sys
from pathlib import Path
from typing import List
import git
from .config import Config

logger = Config.getLogger("git")

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
            logger.debug("pulling repo at %s",  self.dest_path)
            git.Repo(self.dest_path).remotes.origin.pull()
        # otherwise, need to clone into cache
        else:
            logger.debug("cloning repo at %s to %s",  self.url,  self.dest_path)
            try:
                git.Repo.clone_from(self.url,  self.dest_path,  branch="master")
            except git.exc.GitCommandError:
                raise ValueError(f"Invalid repo url: {self.url}")
                
class GitLibrary():
    """A collection of GitProjects
    """
    def __init__(self,  library):
        self.projects = self._load_git_projects_from_library(library)
        
    def __iter__(self):
        for project in self.projects:
            yield project
        
    def _load_git_projects_from_library(self,  library) -> List[GitProject]:
        logger.debug("loading git projects from library: %s",  library)
        git_projects = []
        for (name,  url) in library.items():
            try:
                project = GitProject(name,  url)
                git_projects.append(project)
            except ValueError:
                logger.debug("Ignoring project '%s' with invalid url: %s", name, url)
        return git_projects
        
    @property
    def pyglob(self):
        return self._pyglob()
        
    def _pyglob(self) -> List:
        py_files = []
        for project in self:
            py_files += project.dest_path.glob("**/*.py")
        return py_files

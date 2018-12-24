import sys
from datetime import datetime, timedelta
from collections import namedtuple
import json
from pathlib import Path
from typing import List
import git

from src.config import Config

logger = Config.getLogger("git")


GitProjectGlob = namedtuple("GitProjectGlob", ["name", "glob"])

class GitProject:
    """A project made available via git
    """
    cache_dir = Path.home() / ".cache" / Config.app_name
    def __init__(self, name: str,  url: str, no_fetch=False):
        self.name = name
        self.url = url
        self.dest_path = self.cache_dir / name
        if not no_fetch:
            self._fetch()

    def _fetch(self):
        self.cache_dir.mkdir(exist_ok=True)
        # if it exists in the cache, pull changes
        if self.dest_path.exists():
            logger.debug("Pulling repo at %s",  self.dest_path)
            git.Repo(self.dest_path).remotes.origin.pull()
        # otherwise, need to clone into cache
        else:
            logger.debug("Cloning repo at %s to %s",  self.url,  self.dest_path)
            try:
                git.Repo.clone_from(self.url,  self.dest_path,  branch="master")
            except git.exc.GitCommandError as e:
                raise RuntimeError(f"Failed cloning repo from: {self.url}. Failed with error: {e}")
                
class GitLibrary():
    """A collection of GitProjects
    """
    git_pull_cache_file = Path.home() / ".cache" / Config.app_name / "git-cache.json"
    cache_ttl = timedelta(hours=1)
    def __init__(self,  library):
        self.cached_projects = self._read_git_pull_cache()
        self.projects = self._load_git_projects_from_library(library)
        self.globbed = False # flag to see if glob has already been run
        
    def __iter__(self):
        for project in self.projects:
            yield project
        
    def _load_git_projects_from_library(self,  library) -> List[GitProject]:
        logger.debug("Loading git projects from library: %s",  library)
        git_projects = []
        for (name,  url) in library.items():
            cached = (name in self.cached_projects)
            try:
                project = GitProject(name,  url, cached)
                git_projects.append(project)
            except RuntimeError as e:
                logger.error("Ignoring project '%s' with git error: %s", name, e)
        self._set_git_pull_cache(git_projects)
        return git_projects
        
    def _set_git_pull_cache(self, git_projects):
        current_timestamp = datetime.now()
        output = {"timestamp": current_timestamp.isoformat(timespec="seconds"), "project_names": [p.name for p in git_projects]}
        print(output)
        try:
            with open(self.git_pull_cache_file, "w") as f:
                json.dump(output, f)
        except Exception as e:
            logger.error("Error writing git pull cache: %s", e)
            self.git_pull_cache_file.unlink()
            
    def _read_git_pull_cache(self):
        if self.git_pull_cache_file.exists():
            try:
                with open(self.git_pull_cache_file, "r") as f:
                    cache = json.load(f)
                cached_timestamp = datetime.strptime(cache.get("timestamp"), "%Y-%m-%dT%H:%M:%S")
                if cached_timestamp + self.cache_ttl >= datetime.now():
                    return cache.get("project_names")
            except json.decoder.JSONDecodeError:
                logger.error("Invalid git-cache json, ignoring cache!")
                self.git_pull_cache_file.unlink()
        return []
            
    @property
    def pyglob(self):
        # generate globs
        self._pyglob()
        return [GitProjectGlob(project.name, project.pyglob) for project in self.projects]
        
        
    def _pyglob(self) -> List:
        if not self.globbed:
            for project in self:
                logger.debug("Globbing repo: %s", project.dest_path)
                project.pyglob = project.dest_path.glob("**/*.py")
            self.globbed = True

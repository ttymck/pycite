import sys
from datetime import datetime, timedelta
from dataclasses import dataclass
import json
import re
from pathlib import Path
import typing
import git
import requests

from pycite.catalog import PackageType
from pycite.config import Config

logger = Config.getLogger("git")

@dataclass
class GitProjectGlob:
    name: str
    glob: typing.List[str]

class GitProject:
    """A project made available via git
    """
    cache_dir = Config.cache_path / Config.app_name
    git_link_pattern = re.compile(r"git://.+?\.git")
    def __init__(self, name: str,  url: str, no_fetch=False):
        self.name = name
        self.url = url
        self.dest_path = self.cache_dir / name
        self.pyglob = None # set after fetch
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
            cloned = False
            logger.debug("Cloning repo at %s to %s",  self.url,  self.dest_path)
            try:
                # try cloning from the given repo_url
                self._clone_repo(self.url, self.dest_path)
                cloned = True
            except git.exc.GitCommandError as e:
                # if repo_url failed, find git:// URIs in the page
                git_uris = self._find_git_uri(self.url)
                # there may be multiple URIs, only need 1 to work        
                while cloned == False:
                    for uri in git_uris:
                        try:
                            self._clone_repo(uri, self.dest_path)
                            # if cloned succesfully, exit the while block
                            cloned = True
                        except git.exc.GitCommandError as e:
                            continue
            if cloned == False:
                # if none of the URIs worked, raise runtime error
                raise RuntimeError(f"Failed cloning repo from: {self.url}. Failed with error: {e}")
                
    @staticmethod
    def _clone_repo(url, dest, branch='master', depth=1):
        git.Repo.clone_from(url, dest)
                
                    
    def _find_git_uri(self, repo_url):
        """If failed using repo_url, search that page for a git link(s)
        
        TODO: there may be unrelated git URIs on the page; need to order them
        by likelihood (i.e. it contains the project name or similar substring)
        """
        repo_page = requests.get(repo_url).text
        git_uri_matches = self.git_link_pattern.findall(repo_page)
        if git_uri_matches:
            git_uri_matches = list(set(git_uri_matches))
        for uri in git_uri_matches:
            yield uri
        
                
class GitLibrary():
    """A collection of GitProjects
    """
    git_pull_cache_file = Config.cache_path / "git-cache.json"
    cache_ttl = timedelta(hours=1)
    def __init__(self,  library):
        self._cached_projects = self._read_git_pull_cache()
        self.projects = self._load_git_projects_from_library(library)
        self.globbed = False # flag to see if glob has already been run
        
    def __iter__(self):
        for project in self.projects:
            yield project
        
    def _load_git_projects_from_library(self,  library) -> typing.List[GitProject]:
        logger.debug("Loading git projects from library: %s",  library)
        git_projects = []
        for (name,  url) in library.items(PackageType.GIT):
            cached = name in self._cached_projects
            try:
                project = GitProject(name,  url, cached)
                git_projects.append(project)
            # capture failures to clone with an error log.
            # TODO: add parameter to fail, or add this project to a list for
            # manual analysis
            except RuntimeError as e:
                logger.error("Ignoring project '%s' with git error: %s", name, e)
        self._set_git_pull_cache(git_projects)
        return git_projects
        
    def _set_git_pull_cache(self, git_projects) -> None:
        current_timestamp = datetime.now().isoformat(timespec="seconds")
        output = {"timestamp": current_timestamp, "project_names": [p.name for p in git_projects]}
        logger.debug("Setting git cache at: %s", current_timestamp)
        try:
            with open(self.git_pull_cache_file, "w") as f:
                json.dump(output, f)
        except Exception as e:
            logger.error("Error writing git pull cache: %s", e)
            self.git_pull_cache_file.unlink()
            
    def _read_git_pull_cache(self) -> typing.List[str]:
        if self.git_pull_cache_file.exists():
            try:
                with open(self.git_pull_cache_file, "r") as f:
                    cache = json.load(f)
                cached_timestamp = datetime.strptime(cache.get("timestamp"), "%Y-%m-%dT%H:%M:%S")
                if cached_timestamp + self.cache_ttl >= datetime.now():
                    logger.debug("Using cached git projects from %s", cache.get("timestamp"))
                    return cache.get("project_names")
            except json.decoder.JSONDecodeError:
                logger.error("Invalid git-cache json, ignoring cache!")
                self.git_pull_cache_file.unlink()
        return []
            
    @property
    def pyglob(self) -> typing.List[GitProject]:
        # generate globs
        self._pyglob()
        return [GitProjectGlob(project.name, project.pyglob) for project in self.projects]
        
        
    def _pyglob(self) -> None:
        if not self.globbed:
            for project in self:
                logger.debug("Globbing repo: %s", project.dest_path)
                project.pyglob = list(project.dest_path.glob("**/*.py"))
            self.globbed = True
            

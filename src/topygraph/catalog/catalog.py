from typing import List
from abc import ABC, abstractmethod

from .package import Package


class Catalog(ABC):
    """A library of python packages/modules for analysis
    """

    def __init__(self):
        self._projects = self._load_package_list()

    @abstractmethod
    def _load_package_list(self) -> List[Package]:
        pass

    def __iter__(self):
        for project in self._projects:
            yield project

    def __getitem__(self, index):
        return self._projects[index]

    def __len__(self):
        return len(self._projects)

    def items(self, type_filter=None):
        projects_list = self._projects
        if type_filter:
            projects_list = filter(lambda p: p.type == type_filter, projects_list)
        for project in projects_list:
            yield (project.name, project.uri)

    def keys(self):
        for project in self._projects:
            yield project.name

    def urls(self):
        for project in self._projects:
            yield project.repo_url

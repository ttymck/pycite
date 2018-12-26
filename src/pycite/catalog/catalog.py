import typing
from abc import ABC, abstractmethod

from .package import Package

CatalogFilter = typing.Callable[[typing.List[Package]], bool]


class Catalog(ABC):
    """A library of python packages/modules for analysis
    """

    def __init__(self):
        self._projects = self._load_package_list()
        """Catalogs can implement filters (lambdas) to select package subsets 
        when the .items() method is used (or its downstream methods)
        """
        self._filter: CatalogFilter = None

    @abstractmethod
    def _load_package_list(self) -> typing.List[Package]:
        pass

    def __iter__(self):
        for project in self._projects:
            yield project

    def __getitem__(self, index):
        return self._projects[index]

    def __len__(self):
        return len(self._projects)

    def items(self, type_filter=None):
        """"""
        projects_list = self._projects
        # user defined filter
        if self._filter:
            projects_list = filter(self._filter, projects_list)
        # libraries select only what they can handle
        if type_filter:
            projects_list = filter(lambda p: p.type == type_filter, projects_list)
        for project in projects_list:
            yield project

    def keys(self):
        for project in self.items():
            yield project.name

    def urls(self):
        for project in self.items():
            yield project.repo_url

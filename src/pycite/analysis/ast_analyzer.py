import ast
import itertools
import typing
from dataclasses import dataclass
from collections import Counter
from pycite.config import Config

logger = Config.getLogger("ast_analyzer")


@dataclass(frozen=True, eq=True)
class Import:
    module: str


def get_imports(name: str, glob: list):
    logger.info(f"Getting imports in {name}")
    glob_list = list(glob)
    import_list = itertools.chain.from_iterable(_get_imports_from_glob(glob_list))
    logger.warning(import_list)
    import_counter = Counter(import_list)
    ignore_names = _names_to_ignore(name, glob_list)
    if ignore_names:
        ignored = _drop_ignore_names_from_imports(import_counter, ignore_names)
    logger.info("Ignoring: %s", ignored)
    logger.debug(
        "%s import statements in project %s", len(list(import_counter.elements())), name
    )
    return import_counter


def _drop_ignore_names_from_imports(import_counter: Counter, ignore_names: list):
    ignore_names = set(ignore_names)
    logger.info("Ignoring imports for names: %s", ignore_names)
    counter_names = list(import_counter.elements())
    ignored = []
    for i in counter_names:
        try:
            should_ignore = any([ignore in i.module for ignore in ignore_names])
        except TypeError as e:
            logger.error("Invalid ignore check for '%s': %s", i, e)
        if should_ignore:
            ignored.append(i)
            del import_counter[i]
    return set(ignored)


def _names_to_ignore(name, glob):
    # a simplified name that we would expect to see in code
    project_name_in_code = name.lower().replace(" ", "").replace("-", "_")
    # list of python file names that we can exclude from our search, we don't care about modules defined within the project
    exclude_names = [f.name.rstrip(".py") for f in glob]
    exclude_names.append(project_name_in_code)
    logger.info("exclude names for %s: %s", name, exclude_names)
    return exclude_names


def _get_imports_from_glob(glob: list) -> list:
    for path in glob:
        root = _load_file(path)
        if root:
            imports = _filter_none_import(_parse_root(root))
            yield list(imports)


def _load_file(path):
    with open(path) as fh:
        try:
            return ast.parse(fh.read(), path)
        except SyntaxError:
            logger.error("File %s using invalid syntax could not be parsed", path)
            return None
        except UnicodeDecodeError as e:
            logger.error("File %s contains invalid Unicode: %s", path, e)
            return None


def _filter_none_import(imports: typing.List[Import]):
    return filter(lambda x: x.module is not None, imports)


def _parse_root(root):
    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Import):
            for n in node.names:
                yield Import(n.name)
        elif isinstance(node, ast.ImportFrom):
            try:
                yield Import(node.module)
            except AttributeError:
                yield None
        else:
            continue

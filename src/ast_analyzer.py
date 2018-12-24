import ast
import itertools
import copy
from collections import namedtuple, Counter
from src.config import Config

logger = Config.getLogger("ast_analyzer")

Import = namedtuple("Import", ["module"])

def get_imports(name: str, glob: list):
    logger.info(f"Getting imports in {name}")
    glob_list = list(glob)
    import_list = itertools.chain.from_iterable(_get_imports_from_glob(glob_list))
    logger.warning(import_list)
    import_counter = Counter(import_list)
    ignore_names = _names_to_ignore(name, glob_list)
    if ignore_names:
        ignore_names = set(ignore_names)
        logger.info("Ignoring imports for names: %s", ignore_names)
        counter_names = list(import_counter.elements())
        for i in counter_names:
            try:
                if any([ignore in i.module for ignore in ignore_names]):
                    logger.info("Ignoring import: %s", i)
                    del import_counter[i]
            except TypeError:
                logger.error("Invalid ignore check for '%s'", i)
                del import_counter[i]
    logger.debug("%s import statements in project %s", len(list(import_counter.elements())), name)
    return import_counter   
        
def _names_to_ignore(name, glob):
    # a simplified name that we would expect to see in code
    project_name_in_code = name.lower().replace(" ","").replace("-","_")
    # list of python file names that we can exclude from our search, we don't care about modules defined within the project
    exclude_names = [f.name.rstrip(".py") for f in glob] 
    exclude_names.append(project_name_in_code)
    logger.info("exclude names for %s: %s", name, exclude_names)
    return exclude_names
    
def _get_imports_from_glob(glob: list) -> list:
    for path in glob:
        root = _load_file(path)
        if root:
            imports = list(_parse_root(root))
            yield imports

def _load_file(path):
    with open(path) as fh:
        try:
            return ast.parse(fh.read(), path)
        except SyntaxError:
            logger.error(f"File {path} using invalid syntax could not be parsed")
            return None
    
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

        

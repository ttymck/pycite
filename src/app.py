from collections import Counter
from src.library.apa import APA
from .git import GitLibrary
from src.ast_analyzer import get_imports
from .config import Config

#logger = Config.getLogger("app")

def main():
    apa = APA()
    apa._projects = apa._projects[:10]
    print(f"{len(apa)} modules to parse.")
    project_globs = GitLibrary(apa).pyglob
    py_file_count = sum(len(list(p.glob)) for p in project_globs) 
    print("Python File Count:", py_file_count)
    import_counter = Counter()
    for project in project_globs:
        print("Project %s has %s python files." % (project.name, len(list(project.glob))))
        import_counter.update(get_imports(project.name, project.glob))
    total = sum(import_counter.values())
    print(f"{total} total import statements found.")
    print(f"5 Most Common Imports:\n{import_counter.most_common(5)}")
    
main()

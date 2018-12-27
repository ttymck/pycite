from collections import Counter
from topygraph.catalog import APA
from topygraph.library import GitLibrary
from topygraph.analysis.ast_analyzer import get_imports
from .config import Config

# logger = Config.getLogger("app")


def main():
    apa = APA()
    apa.filter = lambda p: 'science' in (p.tags or [])
    print(f"{len(apa)} modules satisfy filter.")
    project_globs = GitLibrary(apa).pyglob[:10]
    py_file_count = sum(len(list(p.glob)) for p in project_globs)
    print("Python File Count:", py_file_count)
    import_counter = Counter()
    for project in project_globs:
        print(
            "Project %s has %s python files." % (project.name, len(list(project.glob)))
        )
        import_counter.update(get_imports(project.name, project.glob))
    total = sum(import_counter.values())
    print(f"{total} total import statements found.")
    print(f"5 Most Common Imports:\n{import_counter.most_common(5)}")


if __name__ == "__main__":
    main()

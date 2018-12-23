from .library import APA
from .git import GitLibrary

def main():
    apa = APA()
    apa._projects = apa._projects[:7]
    print(len(apa))
    glob = GitLibrary(apa).pyglob
    print("Python File Count:", len(glob))

main()

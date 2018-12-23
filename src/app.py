from .library import APA
from .git import GitLibrary

def main():
    apa = APA()
    print(GitLibrary(apa).py_file_count())

main()

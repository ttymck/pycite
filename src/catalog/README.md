# pycite

A python library for retrieving python packages and conducting network analysis of dependencies. Seeking to provide a semi-quantitative index or scoring of python libraries.

## Domain Model

1. Package
  * defines its type, its name, and its URI
  * can be a git repo, a pypi package, a tar file, etc.
2. Catalog
  * a curated or served collection of packages
  * Awesome Python Applications (a yaml file); PyPI; Conda(?)
3. Library
  * The implementation for retrieving a certain type of package
  * Clones a git repo; pip install a PyPI package; download a tarball...  
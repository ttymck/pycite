import pytest
import tempfile
from pathlib import Path
from pycite.library import git

@pytest.fixture()
def git_project():
    name = "solfege"
    url = "http://git.savannah.gnu.org/cgit/solfege.git"
    tmpdir = tempfile.TemporaryDirectory()
    dest_dir = Path(tmpdir.name) / name 
    project = git.GitProject(name, url, no_fetch=True)
    project.dest_path = dest_dir
    yield project
    
def test_find_git_uri(git_project):
    """Tests the regex functionality in finding git uris from an invalid 
    git repo link. 
    
    TODO: convert to sample data/mocked url, currently making live request to git.savannah.gnu.org
    """
    uris = git_project._find_git_uri(git_project.url)
    uri_list = list(uris)
    assert len(uri_list) == 1

import pytest
from src import library

@pytest.fixture(scope="module")
def apa():
    yield library.APA()

def test_init(apa):
    assert isinstance(apa,  library.Library)
    
def test_iter(apa):
    assert isinstance(apa[0],  library.PackageInfo)

def test_keys(apa):
    assert 'Reddit' in apa.keys()
    
def test_len(apa):
    assert isinstance(len(apa),  int)
        

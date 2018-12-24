import pytest
from src.library.apa import APA
from src.library.library import Library
from src.library.package_info import PackageInfo

@pytest.fixture(scope="module")
def apa():
    yield APA()

def test_init(apa):
    assert isinstance(apa, Library)
    
def test_iter(apa):
    assert isinstance(apa[0],  PackageInfo)

def test_keys(apa):
    assert 'Reddit' in apa.keys()
    
def test_len(apa):
    assert isinstance(len(apa),  int)
        

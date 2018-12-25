import pytest
from src.catalog import APA, Library, Package

@pytest.fixture(scope="module")
def apa():
    yield APA()

def test_init(apa):
    assert isinstance(apa, Library)
    
def test_iter(apa):
    assert isinstance(apa[0],  Package)

def test_keys(apa):
    assert 'Reddit' in apa.keys()
    
def test_len(apa):
    assert isinstance(len(apa),  int)
        

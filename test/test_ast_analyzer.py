import pytest
import ast
from src import ast_analyzer


@pytest.fixture()
def sample_code():
    src = """
from coco import bunny
from coco.bungy import carrot
from meta import teta
from rocket import spaceship as sp
import bingo
import com.stackoverflow
import motorbike as car
import module1, module2
"""
    yield src 
    
def test_import_parser(sample_code):
    root = ast.parse(sample_code)
    imports = ast_analyzer._parse_root(root)
    import_list = list(imports)
    assert import_list[5] == ast_analyzer.Import("com.stackoverflow")
    

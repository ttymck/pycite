import pytest

from topygraph.get_std_lib import get_std_lib

def test_get_std_lib():
    std_lib_names = get_std_lib()
    # gets most of standard library, cuts out test submodules
    assert all(['.test' not in n for n in std_lib_names])

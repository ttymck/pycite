import distutils.sysconfig as sysconfig
import os
import sys

std_lib = sysconfig.get_python_lib(standard_lib=True)


def get_std_lib():
    full_std_lib = _walk_std_lib()
    filtered_libs = filter(lambda x: _filter_std_lib_names(x), full_std_lib)
    return filtered_libs


def _filter_std_lib_names(name: str):
    checks = [lambda x: not ".test" in x]
    for check in checks:
        if not check(name):
            return False
    return True


def _walk_std_lib():
    for top, dirs, files in os.walk(std_lib):
        for name in files:
            prefix = top[len(std_lib) + 1 :]
            if prefix[:13] == "site-packages":
                continue
            if name == "__init__.py":
                yield top[len(std_lib) + 1 :].replace(os.path.sep, ".")
            elif name[-3:] == ".py":
                yield os.path.join(prefix, name)[:-3].replace(os.path.sep, ".")
            elif name[-3:] == ".so" and top[-11:] == "lib-dynload":
                yield name[0:-3]

import sys
import re
import ast

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('yobit_api/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

if sys.version_info < (3, 2):
    raise NotImplementedError("Sorry, you need at least Python 3.x")

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='yobit_api',
    version=version,
    packages=['yobit_api'],
    url='',
    license='',
    author='yobit_api',
    author_email='',
    description=''
)

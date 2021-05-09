"""
Allows package to be installed in "editable" mode by running `pip install -e`
Can change source code and rerun tests at will
"""
from setuptools import setup, find_packages
import impression_web

# get the dependencies and installs
with open('requirements.txt', 'r') as f:
    requires = [x.strip() for x in f if x.strip()]

setup(
    name='impression_web',
    packages=find_packages(),
    version=impression_web.__version__,
    author=impression_web.__author__,
    author_email=impression_web.__author_email__,
    license=impression_web.__licence__,
    install_requires=requires)

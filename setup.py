"""
Allows package to be installed in "editable" mode by running `pip install -e`
Can change source code and rerun tests at will
"""
from setuptools import setup, find_packages
import impression_job

# get the dependencies and installs
with open('requirements.txt', 'r') as f:
    requires = [x.strip() for x in f if x.strip()]

setup(
    name='impression_job',
    packages=find_packages(),
    version=impression_job.__version__,
    author=impression_job.__author__,
    author_email=impression_job.__author_email__,
    license=impression_job.__licence__,
    install_requires=requires)

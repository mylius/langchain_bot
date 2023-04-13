import os
import runpy

from setuptools import find_packages
from setuptools import setup

_this_dir = os.path.dirname(os.path.abspath(__file__))
_version_file = os.path.join(_this_dir, "langchain_bot/version.py")
__version__ = runpy.run_path(_version_file)["version"]

requirements = [
    "pydantic~=1.10.7",
    "fastapi~=0.95.0",
    "uvicorn~=0.21.1",
    "slack_sdk~=3.20.2",
    "langchain~=0.0.123",
    "chromadb~=0.3.11",
]

setup(
    author="Jan-Gabriel Mylius",
    name="langchain_bot",
    install_requires=requirements,
    packages=find_packages(),
    version=__version__,
)
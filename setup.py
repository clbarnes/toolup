import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md')) as f:
    readme = f.read()

with open(os.path.join(here, 'toolup', 'version.py')) as f:
    exec(f.read())

setup(
    name="toolup",
    version=__version__,
    packages=find_packages(include=('toolup', )),
    url="https://github.com/clbarnes/toolup",
    license="MIT",
    install_requires=["toml"],
    author="Chris L. Barnes",
    author_email="barnesc@janelia.hhmi.org",
    description="Convenience package for installing python-based development tools",
    long_description=readme,
    long_description_content_type='text/markdown',
    entry_points={"console_scripts": "toolup = toolup.__main__:main"},
    python_requires=">=3.6.1",
)

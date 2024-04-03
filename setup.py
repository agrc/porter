#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
setup.py
A module that installs conductor as a module
"""
from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup

setup(
    name="conductor",
    version="2.5.2",
    license="MIT",
    description="A bot to check on the status of porter issues.",
    author="UGRC",
    author_email="ugrc-developers@utah.gov",
    url="https://github.com/agrc/porter",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
    ],
    project_urls={
        "Issue Tracker": "https://github.com/agrc/porter/issues",
    },
    keywords=["gis"],
    install_requires=[
        "colorama==0.*",
        "flask==3.*",
        "psycopg2-binary==2.*",
        "PyGithub==2.*",
        "pygsheets==2.*",
        "pyodbc>=4,<6",
        "requests==2.*",
    ],
    extras_require={
        "cloud-run": [
            "flask==3.*",
            "gunicorn==21.*",
        ],
        "tests": [
            "pytest-cov>=4,<6",
            "pytest-instafail==0.5.*",
            "pytest-mock==3.*",
            "pytest-ruff==0.*",
            "pytest-watch==4.*",
            "pytest>=7,<9",
            "black>=23,<25",
            "ruff==0.0.*",
        ],
    },
    setup_requires=[
        "pytest-runner",
    ],
    entry_points={
        "console_scripts": [
            "conductor = conductor.conductor:startup",
            "test_conductor = conductor.conductor:startup_local",
        ]
    },
)

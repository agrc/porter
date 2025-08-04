#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
setup.py
A module that installs conductor as a module
"""

from pathlib import Path

from setuptools import find_packages, setup

setup(
    name="conductor",
    version="2.5.13",
    description="A bot to check on the status of porter issues.",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    author="UGRC",
    author_email="ugrc-developers@utah.gov",
    url="https://github.com/agrc/porter",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=True,
    license_files=["LICENSE"],
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
    ],
    project_urls={
        "Issue Tracker": "https://github.com/agrc/porter/issues",
    },
    keywords=["gis", "issue-ops", "github", "automation", "workflow"],
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
            "gunicorn==23.*",
        ],
        "tests": [
            "pytest-cov==6.*",
            "pytest-instafail==0.5.*",
            "pytest-mock==3.*",
            "pytest-ruff==0.*",
            "pytest-watch==4.*",
            "pytest>=7,<9",
            "ruff==0.*",
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

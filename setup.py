#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
setup.py
A module that installs projectname as a module
"""
from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup

setup(
    name='conductor',
    version='1.0.0',
    license='MIT',
    description='A bot to check on the status of a porter issue.',
    author='AGRC',
    author_email='agrc@utah.gov',
    url='https://github.com/agrc/porter',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
    ],
    project_urls={
        'Issue Tracker': 'https://github.com/agrc/porter/issues',
    },
    keywords=['gis'],
    install_requires=[
        'PyGithub==1.*',
        'pyodbc==4.*',
        'psycopg2-binary==2.*',
    ],
    extras_require={
        'tests': [
            'pylint-quotes==0.2.*',
            'pylint==2.5.*',
            'pytest-cov==2.9.*',
            'pytest-instafail==0.4.*',
            'pytest-isort==1.0.*',
            'pytest-mock==3.1.*',
            'pytest-pylint==0.17.*',
            'pytest-watch==4.2.*',
            'pytest==5.4.*',
            'yapf==0.30.*',
        ]
    },
    setup_requires=[
        'pytest-runner',
    ],
    entry_points={'console_scripts': [
        'conductor = conductor.conductor:startup',
    ]},
)

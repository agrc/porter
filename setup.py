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
    name='conductor',
    version='2.1.1',
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
        'colorama==0.*',
        'docopt==0.*',
        'flask==1.*',
        'psycopg2-binary==2.*',
        'PyGithub==1.*',
        'pygsheets==2.*',
        'pyodbc==4.*',
        'requests==2.*',
    ],
    extras_require={
        'cloud-run': [
            'flask==1.*',
            'google-cloud-secret-manager==2.5.*',
            'gunicorn==20.*',
        ],
        'tests': [
            'pylint-quotes==0.2.*',
            'pylint==2.*',
            'pytest-cov==2.*',
            'pytest-instafail==0.4.*',
            'pytest-isort==2.*',
            'pytest-mock==3.*',
            'pytest-pylint==0.17.*',
            'pytest-watch==4.*',
            'pytest==6.*',
            'yapf==0.*',
        ]
    },
    setup_requires=[
        'pytest-runner',
    ],
    entry_points={
        'console_scripts': [
            'conductor = conductor.conductor:startup',
            'test_conductor = conductor.conductor:startup_local',
        ]
    },
)

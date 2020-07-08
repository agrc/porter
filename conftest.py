#!/usr/bin/env python
# * coding: utf8 *
"""
conftest.py
a module to modify the pytest cli
"""
import pytest


def pytest_addoption(parser):
    """adds a cli option to pytest
    """
    parser.addoption('--vpn', action='store_true', default=False, help='run tests that require vpn')


def pytest_configure(config):
    """setup configuration on pytest
    """
    config.addinivalue_line('markers', 'vpn: mark test as vpn required to run')


def pytest_collection_modifyitems(config, items):
    """modify test collection to handle marked tests
    """
    if config.getoption('--vpn'):
        # --vpn given in cli: do not skip slow tests
        return

    skip_vpn = pytest.mark.skip(reason='need --vpn option to run')

    for item in items:
        if 'vpn' in item.keywords:
            item.add_marker(skip_vpn)

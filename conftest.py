#!/usr/bin/env python
# * coding: utf8 *
"""
conftest.py
a module to modify the pytest cli
"""
import pytest


def pytest_addoption(parser):
    """adds a cli option to pytest"""
    parser.addoption("--vpn", action="store_true", default=False, help="run tests that require vpn")
    parser.addoption(
        "--google",
        action="store_true",
        default=False,
        help="run tests that require google sheets access",
    )


def pytest_configure(config):
    """setup configuration on pytest"""
    config.addinivalue_line("markers", "vpn: mark test as vpn required to run")
    config.addinivalue_line("markers", "google: mark test as google required to run")


def pytest_collection_modifyitems(config, items):
    """modify test collection to handle marked tests"""
    if not config.getoption("--vpn"):
        skip_vpn = pytest.mark.skip(reason="need --vpn option to run on state network")

        for item in items:
            if "vpn" in item.keywords:
                item.add_marker(skip_vpn)

    if not config.getoption("--google"):
        skip_google = pytest.mark.skip(reason="need --google option and client-secrets.json to access")

        for item in items:
            if "google" in item.keywords:
                item.add_marker(skip_google)

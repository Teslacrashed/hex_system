#!/usr/bin/env python
# vim: ft=python
"""tests/confest.py."""
# Standard Library
import logging

# Third Party Library
import pytest

# First Party Library
from geometry import Point


LOG = logging.getLogger()


@pytest.fixture
def point_0_0() -> Point:
    return Point(0, 0)

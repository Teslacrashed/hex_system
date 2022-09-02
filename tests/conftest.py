#!/usr/bin/env python
# vim: ft=python
"""tests/confest.py."""
import logging
import pytest

from geometry import Point

LOG = logging.getLogger()


@pytest.fixture
def point_0_0() -> Point:
    return Point(0, 0)

#!/usr/bin/env python
# vim: ft=python
"""tests/geometry/test_line.py."""
import pytest

from geometry import Line
from geometry import Point


def test_line():
	origin = Point(0, 0)
	end = Point(1, 2)
	line = Line(origin, end)

	assert origin == line.origin
	assert end == line.end

	# check repr string
	# line_repr = eval(str(line))
	# assert line == line_repr


def test_line_eq():
	origin = Point(0, 0)
	end = Point(1, 1)

	line1 = Line(origin, end)
	line2 = Line(origin, end)

	assert line1 == line2

	# Line == anything: error
	# with pytest.raises(GeometryArithmeticError):
		# line0 == v

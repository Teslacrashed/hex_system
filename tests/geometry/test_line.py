#!/usr/bin/env python
# vim: ft=python
"""tests/geometry/test_line.py."""
# Standard Library
import math

# Third Party Library
import pytest

# First Party Library
from geometry import (
	Line,
	Point,
)


def test_line_init() -> None:
	x0y0 = Point(0, 0)
	x1y2 = Point(1, 2)
	line = Line(x0y0, x1y2)

	assert x0y0 == line.origin
	assert x1y2 == line.end
	return


def test_line_length() -> None:
	x1y1 = Point(1, 1)
	x2y2 = Point(2, 2)
	line = Line(x1y1, x2y2)

	assert line.x1 == 1
	assert line.x2 == 2

	assert line.y1 == 1
	assert line.y2 == 2

	assert line.length == math.sqrt(2)
	return


def test_line_no_same_points() -> None:

	with pytest.raises(ValueError):
		line = Line(Point(1, 1), Point(1, 1))

	return


@pytest.mark.parametrize(
	('line', 'length'), [
		(Line(Point(0, 0), Point(1, 0)), 1),
		(Line(Point(0, 0), Point(1, 0)), 1),
	]
)
def test_distance(line: Line, length: float):
	assert line.length == length


def test_line_origin_is_read_only() -> None:
	p1 = Point(1, 1)
	p2 = Point(2, 2)
	line = Line(p1, p2)

	with pytest.raises(AttributeError):
		line.origin = Point(3, 3)
	return


def test_line_end_point_is_read_only():
	p1 = Point(1, 1)
	p2 = Point(2, 2)
	line = Line(p1, p2)

	new_end_point = Point(3, 3)
	with pytest.raises(AttributeError):
		line.end = new_end_point

	assert line.end != new_end_point
	return


def test_line_eq():
	origin = Point(0, 0)
	end = Point(1, 1)

	line1 = Line(origin, end)
	line2 = Line(origin, end)

	assert line1 == line2

	# Line == anything: error
	# with pytest.raises(GeometryArithmeticError):
		# line0 == v

#!/usr/bin/env python
# vim: ft=python
"""tests/geometry/test_point.py."""
import pytest

from config import Number
from geometry import Point


def test_point_init() -> None:
	"""Test the initialization of Vector2D objects and basic properties."""
	point = Point(0, 2)
	# str(vec)  # test the string representation of the vector

	assert point.x == 0
	assert point.y == 2
	assert point[0] == 0
	assert point[1] == 2
	# assert point.magnitude == 2
	# assert point.magnitude_squared == 4
	# assert not vec.is_zero(0.0000001)

	assert len(point) == 2
	point_tuple = tuple(i for i in point)
	assert point_tuple == (0, 2)

	# norm_vec = vec.normalize()
	# assert norm_vec.x == 0
	# assert norm_vec.y == 1
	# assert norm_vec.magnitude == 1

	return


def test_point_iterate() -> None:
	point = Point(1, 2)
	x, y = point
	assert (x, y) == (1, 2)
	return



left: int = -1
right: int = 1


@pytest.mark.parametrize('x0', [x for x in range(left, right)])
@pytest.mark.parametrize('y0', [y for y in range(left, right)])
@pytest.mark.parametrize('x1', [x for x in range(left, right)])
@pytest.mark.parametrize('y1', [y for y in range(left, right)])
def test_point_compare(x0: Number, y0: Number, x1: Number, y1: Number) -> None:

	if x0 == x1 and y0 == y1:
		assert (Point(x0, y0) == Point(x1, y1)) is True
		assert (Point(x0, y0) != Point(x1, y1)) is False

		assert (Point(x0, y0) < Point(x1, y1)) is False
		assert (Point(x0, y0) <= Point(x1, y1)) is True
		assert (Point(x0, y0) > Point(x1, y1)) is False
		assert (Point(x0, y0) >= Point(x1, y1)) is True

	else:
		assert (Point(x0, y0) == Point(x1, y1)) is False
		assert (Point(x0, y0) != Point(x1, y1)) is True

	if x0 < x1 or x0 == x1 and y0 < y1:
		assert (Point(x0, y0) < Point(x1, y1)) is True
		assert (Point(x0, y0) <= Point(x1, y1)) is True
		assert (Point(x0, y0) > Point(x1, y1)) is False
		assert (Point(x0, y0) >= Point(x1, y1)) is False

	if x0 > x1 or x0 == x1 and y0 > y1:
		assert (Point(x0, y0) < Point(x1, y1)) is False
		assert (Point(x0, y0) <= Point(x1, y1)) is False
		assert (Point(x0, y0) > Point(x1, y1)) is True
		assert (Point(x0, y0) >= Point(x1, y1)) is True

	return



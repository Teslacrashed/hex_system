#!/usr/bin/env python
# vim: ft=python
"""tests/geometry/test_point.py."""
# Third Party Library
import pytest

# First Party Library
from geometry import Point

# App
from config import Number


def test_point_init() -> None:
	"""Test the initialization of Vector2D objects and basic properties."""
	point = Point(0, 2)

	assert point.x == 0
	assert point.y == 2
	assert point[0] == 0
	assert point[1] == 2

	assert len(point) == 2
	generated_tuple = tuple(i for i in point)
	assert generated_tuple == (0, 2)

	return


def test_point_x_is_readonly() -> None:
	point = Point(2, 4)
	with pytest.raises(AttributeError):
		point.x = 3
	return

def test_point_y_is_readonly() -> None:
	point = Point(2, 4)
	with pytest.raises(AttributeError):
		point.y = 3
	return

def test_point_equality() -> None:
	p = Point(1, 1)
	r = Point(1, 1)
	assert p == r and p is not r
	return

def test_point_inequality() -> None:
	p = Point(2, 2)
	r = Point(1, 1)
	assert p != r and p is not r


def test_point_eq() -> None:
	point = Point(0, 0)
	assert None != point


def test_point_iterate() -> None:
	point = Point(1, 2)
	x, y = point
	assert (x, y) == (1, 2)
	return


def test_points_are_sortable() -> None:
	starting_list = [Point(2, 2), Point(1, 2), Point(2, 1), Point(1, 1)]
	sorted_list = sorted(starting_list)
	assert sorted_list == [Point(1, 1), Point(1, 2), Point(2, 1), Point(2, 2)]
	return

def test_points_distance() -> None:
	# Check distance between two points.
	# assert(cc.Point(0.0, 0.0).distance(cc.Point(1.0, 1.0)) == pytest.approx(math.sqrt(2.0)))
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

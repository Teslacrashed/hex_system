#!/usr/bin/env python
# vim: ft=python
"""geometry/hexagon.py.

horizontal grain / pointy top
vertical grain / flat top

qrs instead of xyz
# Hex
# Side (a)
# The length of a side / edge of a hexagon.
HEX_SIDE: float = 32.0

# Circumradius (R) Distance from center of hexagon to a corner.
HEX_CIRCUMRADIUS: float = HEX_SIDE

# Long Diagonal (d) Distance of a line from corner to corner that crosses the center of the hexagon.
# Easily calculated as the length of two sides.
HEX_HEIGHT: float = HEX_SIDE * 2.0

# Short Diagonal (s) Distance of a line that crosses from corner to corner that does not cross the center of the hexagon.
HEX_WIDTH: float = HEX_SIDE * SQRT_3

# Apothem (r) / inradius
# Distance between the midpoint of any side / edge and the center of the hexagon.
HEX_APOTHEM: float = HEX_SIDE * SQRT_3 / 2.0
"""
# Standard Library
import math
from typing import (
	Any,
	Dict,
	List,
	Tuple,
)

# First Party Library
from geometry.point import Point

# App
from config import (
	PI,
	SQRT_3,
	SQRT_3_OVER_2,
	Number,
)
from utils import round_to_int


__all__ = ['Hexagon']


class Hexagon:
	"""A hex position in cube coordinates.

	:const:`SIDE`

	:py:const:`SIDE`

	:const:`geometry.Hexagon.SIDE`

	:py:const:`geometry.Hexagon.SIDE`

	:py:const:`geometry.Hexagon.SIDE`

	q, r, and s must always total to zero.
	See https://www.redblobgames.com/grids/hexagons/ for details.
	"""

	_side: float = 32.0
	_height: float = _side * 2.0
	_width: float = _side * SQRT_3
	_apothem: float = _side * SQRT_3_OVER_2
	_orientation: str = 'pointy-top'

	def __new__(cls, point: Point):
		if isinstance(point.x, float):
			LOG.warning(f'<x: {x} is float>.')
		if isinstance(point.y, float):
			LOG.warning(f'<y: {y} is float>.')
		return super(Hexagon, cls).__new__(cls)

	def __init__(self, point: Point) -> None:
		self._center: Point = point
		self._x = self._center.x
		self._y = self._center.y

		# To coerce drawing vertices clockwise starting North.
		self._angle_degrees: List[int] = [270, -30, 30, 90, 150, 210]

		# List comprehension to dynamically create Hex's radians based on the `ANGLE_DEGREES` list.
		self._angle_radians: List[float] = [math.radians(degree) for degree in self.angle_degrees]
		return

	def __str__(self) -> str:
		return f"{self.__class__.__name__}({self.x}, {self.y})"

	def __repr__(self) -> str:
		return f"<{self.__class__.__name__}(x: {self.x}, y: {self.y})>"

	@property
	def angle_degrees(self) -> List[int]:
		return self._angle_degrees

	@property
	def angle_radians(self) -> List[float]:
		return self._angle_radians

	@property
	def width(self) -> int:
		return round_to_int(self._width)

	@property
	def height(self) -> int:
		return round_to_int(self._height)

	@property
	def side(self) -> int:
		return round_to_int(self._side)

	@property
	def size(self) -> Tuple[int, int]:
		return self.width, self.height

	@property
	def center(self) -> Point:
		return self._center

	@property
	def corners(self) -> List[Point]:
		return self._get_corners()

	@property
	def x(self) -> Number:
		return self._x

	@property
	def y(self) -> Number:
		return self._y

	@property
	def xy(self) -> Tuple[Number, Number]:
		return self.x, self.y

	@property
	def to_dict(self) -> Dict[str, Any]:
		stats = {
			'center': self.center,
			'corners': self.corners,
			'side': self.side,
			'size': self.size
		}
		return stats

	def _get_corner_offset(self, angle_radian: float) -> Point:

		corner_x: Number = self.side * math.cos(angle_radian)
		corner_y: Number = self.side * math.sin(angle_radian)

		return Point(round_to_int(corner_x), round_to_int(corner_y))

	def _get_corners(self) -> List[Point]:

		corners: List[Point] = []

		for angle_radian in self.angle_radians:
			corner_offset: Point = self._get_corner_offset(angle_radian)
			corner: Point = self.center + corner_offset
			corners.append(corner)

		return corners

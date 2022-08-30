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
import math
from typing import (
	List,
	Tuple
)

from config import Number
from geometry.point import Point

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

	SIDE: float = 32.0
	HEIGHT: float = SIDE * 2.0
	WIDTH: float = SIDE * math.sqrt(3.0)
	APOTHEM: float = SIDE * math.sqrt(3.0) / 2.0
	# To coerce drawing vertices clockwise starting North.
	ANGLE_DEGREES: List[int] = [270, -30, 30, 90, 150, 210]
	# List comprehension to dynamically create Hex's radians based on the `ANGLE_DEGREES` list.
	ANGLE_RADIANS: List[float] = [math.radians(degree) for degree in ANGLE_DEGREES]

	def __init__(self, point: Point) -> None:
		self._center: Point = point
		self._x = self._center.x
		self._y = self._center.y
		return

	def __str__(self) -> str:
		return f"{self.__class__.__name__}({self.x}, {self.y})"

	def __repr__(self) -> str:
		return f"<{self.__class__.__name__}(x: {self.x}, y: {self.y})>"

	@property
	def width(self) -> Number:
		return self.WIDTH

	@property
	def height(self) -> Number:
		return self.HEIGHT

	@property
	def size(self) -> Tuple[Number, Number]:
		return self.width, self.height

	@property
	def center(self) -> Point:
		return self._center

	@property
	def x(self) -> Number:
		return self._x

	@property
	def y(self) -> Number:
		return self._y

	@property
	def xy(self) -> Tuple[Number, Number]:
		return self.x, self.y

	def _get_corner_offset(self, angle_radian: float) -> Point:

		corner_x: Number = self.SIDE * math.cos(angle_radian)
		corner_y: Number = self.SIDE * math.sin(angle_radian)

		return Point(int(round(corner_x)), int(round(corner_y)))

	def get_corners(self) -> List[Point]:

		corners: List[Point] = []

		for angle_radian in self.ANGLE_RADIANS:
			corner_offset: Point = self._get_corner_offset(angle_radian)
			corner: Point = self.center + corner_offset
			corners.append(corner)

		return corners

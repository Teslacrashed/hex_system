#!/usr/bin/env python
# vim: ft=python
"""geometry/rectangle.py."""
# Standard Library
from dataclasses import dataclass
from typing import (
	Any,
	Dict,
	Tuple,
)

# First Party Library
from geometry.point import Point

# App
from config import Number
from loggers import get_logger
from utils import round_to_int


__all__ = ['Rectangle']


@dataclass
class Rectangle:
	"""A rectangle identified by two points.

	The rectangle stores left, top, right, and bottom values.

	Coordinates are based on screen coordinates.

	origin                               top
	+-----> x increases                |
	|                           left  -+-  right
	v                                  |
	y increases                         bottom

	set_points  -- reset rectangle coordinates
	contains  -- is a point inside?
	overlaps  -- does a rectangle overlap?
	top_left  -- get top-left corner
	bottom_right  -- get bottom-right corner
	expanded_by  -- grow (or shrink)
	"""

	def __init__(self, origin: Point, end: Point) -> None:
		"""Create a rectangle.

		:param origin: The pixel x, y coordinates of the top left corner of the Rectangle.
		:type origin: Point
		:param end: The pixel x, y coordinate of the bottom right corner of the Rectangle.
		:type end: Point
		:rtype: None
		"""
		self._log = get_logger(self.__class__.__name__)
		self._origin = origin
		self._end = end
		return

	def __repr__(self) -> str:
		return f'<{self.__class__.__name__}(origin: {self.origin}, end: {self.end})>'

	def __str__(self) -> str:
		return f'{self.__class__.__name__}({self.origin}, {self.end})'

	@property
	def width(self) -> int:
		return self.end.x - self.origin.x

	@property
	def height(self) -> int:
		return self.end.y - self.origin.y

	@property
	def size(self) -> Tuple[int, int]:
		return self.width, self.height

	@property
	def origin(self) -> Point:
		return self._origin

	@property
	def end(self) -> Point:
		return self._end

	@property
	def left(self) -> int:
		return self.origin.x

	@property
	def top(self) -> int:
		return self.origin.y

	@property
	def right(self) -> int:
		return self.end.x

	@property
	def top(self) -> int:
		return self.end.y

	@property
	def midleft(self):
		return self.left, self.height / 2

	@property
	def midtop(self):
		return self.width / 2, self.top

	@property
	def midright(self):
		return self.right, self.height / 2

	@property
	def midbottom(self):
		return self.width / 2, self.bottom

	@property
	def perimeter(self) -> int:
		return (self.height + self.width) * 2

	@property
	def midpoint(self) -> Point:
		return Point(self.width / 2, self.height / 2)

	@property
	def to_dict(self) -> Dict[str, Any]:
		stats= {
			'origin': self.origin,
			'end': self.end,
			'size': self.size
		}
		return stats

	def contains(self, point: Point) -> bool:
		"""Return true if a point is inside the rectangle."""
		return (self.left <= point.x <= self.right and self.top <= point.y <= self.bottom)

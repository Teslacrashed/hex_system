#!/usr/bin/env python
# vim: ft=python
"""geometry/line.py."""
from dataclasses import dataclass
import math
from typing import (
	Tuple
)

from config import Number
from geometry.point import Point

__all__ = ['Line']


@dataclass
class Line:
	""""""

	# __slots__ = 'origin', 'end'
	# origin: Point
	# end: Point

	def __init__(self, origin: Point, end: Point) -> None:
		self._origin = origin
		self._end = end
		return None

	def __str__(self) -> str:
		return f"{self.__class__.__name__}({self.origin}, {self.end})"

	def __repr__(self) -> str:
		return f"<{self.__class__.__name__}(origin: {self.origin}, end: {self.end})>"

	def __eq__(self, other) -> bool:
		if self.__class__ == other.__class__:
			return self.origin == other.origin and self.end == other.end

	@property
	def origin(self) -> Point:
		return self._origin

	@property
	def end(self) -> Point:
		return self._end

	@property
	def p1(self) -> Point:
		"""Get the point with smaller x value

		.. note:: Convenience method to make some other code cleaner/easier to read."""
		return self.end if self.origin.x > self.end.x else self.origin

	@property
	def p2(self) -> Point:
		"""Get the point with larger x value.

		.. note:: Convenience method to make some other code cleaner/easier to read.
		"""
		return self.origin if self.origin.x > self.end.x else self.end

	@property
	def x1(self) -> Number:
		return self.origin.x

	@property
	def y1(self) -> Number:
		return self.origin.y

	@property
	def x1y1(self) -> Tuple[Number, Number]:
		return self.x1, self.y1

	@property
	def x2(self) -> Number:
		return self.end.x

	@property
	def y2(self) -> Number:
		return self.end.y

	@property
	def x2y2(self) -> Tuple[Number, Number]:
		return self.x2, self.y2

	@property
	def dx(self) -> Number:
		return self.end.x - self.origin.x

	@property
	def dy(self) -> Number:
		return self.end.y - self.origin.y

	@property
	def slope(self):
		return self.dy / self.dx

	@property
	def normal(self):
		return -self.dx / self.dy

	@property
	def is_horizontal_line(self) -> bool:
		if self.p1.y == self.p2.y:
			return True
		return False

	@property
	def is_vertical_line(self) -> bool:
		if self.p1.x == self.p2.x:
			return True
		return False

	@property
	def width(self):
		"""Arbitrarily make the width the length, and set height to 0"""
		return abs(self.end - self.origin)

	@property
	def height(self) -> int:
		return 0

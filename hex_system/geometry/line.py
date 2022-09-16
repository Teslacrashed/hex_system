#!/usr/bin/env python
# vim: ft=python
"""geometry/line.py."""
# Standard Library
import math
from dataclasses import dataclass
from typing import Tuple

# First Party Library
from geometry.point import Point

# App
from config import Number
from loggers import get_logger


__all__ = ['Line']

LOG = get_logger('Line')


@dataclass(frozen=True)
class Line:
	"""A Line."""

	__slots__ = 'origin', 'end'
	origin: Point
	end: Point

	def __new__(cls, origin: Point, end: Point):
		#p1 = Point(p1)
		#p2 = Point(p2)

		if origin == end:
			# sometimes we return a single point if we are not given two unique
			# points. This is done in the specific subclass
			raise ValueError(f"{cls.__name__}.__new__ requires two unique Points.")

		if len(origin) != len(end):
			raise ValueError(f"{cls.__name__}.__new__ requires two Points of equal dimension.")

		return super().__new__(cls)

	def __str__(self) -> str:
		return f"{self.__class__.__name__}({self.origin}, {self.end})"

	def __repr__(self) -> str:
		return f"<{self.__class__.__name__}(origin: {self.origin}, end: {self.end})>"

	def __eq__(self, other) -> bool:
		if self.__class__ == other.__class__:
			return self.origin == other.origin and self.end == other.end
		else:
			raise TypeError()

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
		return self.x2 - self.x1

	@property
	def dy(self) -> Number:
		return self.y2 - self.y1

	@property
	def inclination(self) -> float:
		"""calculating the inclination of the LineSegment instance.

		:return: The inclination of the LineSegment instance as an angle in radians.
		"""
		return math.atan(self.slope)


	def midpoint(self, ratio: float = 0.5) -> Point:
		"""finds a point on the LineSegment object located at the given
		ratio, taken the 'end1' attribute of the object as the starting
		point
		Args:
			ratio (float): the ratio of the target point on the
			LineSegment instance
		Returns:
			a point preserving that ratio, taking the 'end1' attribute
			of the LineSegment instance as the starting point and the
			'end2' attribute as the end point
		"""
		LOG.debug(f"<ratio: {ratio}>.")
		# if 0.0 < ratio < 1.0:
			# raise RuntimeError("the given ratio should have a value between zero and one")

		# point = Point(self.end1.x, self.end1.y)
		delta_x = (math.cos(self.inclination)) * (self.length) * (ratio)
		delta_y = (math.sin(self.inclination)) * (self.length) * (ratio)
		point = Point(delta_x, delta_y)
		return point

	@property
	def slope(self):
		"""Get the slope of the Line.

		:return: the slope of the LineSegment instance as the tangent of its inclination angle
		"""

		try:
			result = self.dy / self.dx
		except ZeroDivisionError:
			result = math.tan(math.pi / 2)
		finally:
			return result

	@property
	def length(self) -> float:
		"""Calculate the length of the Line.

		:return: The length of the Line instance.
		"""
		x1, y1 = self.x1y1
		x2, y2 = self.x2y2
		return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))

	@property
	def normal(self):
		return -self.dx / self.dy

	@property
	def is_horizontal_line(self) -> bool:
		if self.y1 == self.y2:
			return True
		return False

	@property
	def is_vertical_line(self) -> bool:
		if self.x1 == self.x2:
			return True
		return False

	@property
	def width(self):
		"""Arbitrarily make the width the length, and set height to 0"""
		return abs(self.end - self.origin)

	@property
	def height(self) -> int:
		return 0

	def dot(self, other) -> float: # assumes Line is a vector from p1 to p2
		if self.__class == other.__class__:
			v1 = (self.end - self.end)
			v2 = (other.origin - other.origin)
			return v1.dot(v2)

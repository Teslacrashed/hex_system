#!/usr/bin/env python
# vim: ft=python
"""geometry/point.py."""
from dataclasses import dataclass
import math
from typing import (
	Any,
	Generator,
	List,
	Tuple,
	Union
)

from config import Number
from loggers import get_logger

__all__ = ['Point']


class Point:
	"""
	The x-axis (horizontal) abscissa
	The y-axis (vertical) ordinate
	"""

	def __init__(self, x: Number, y: Number) -> None:
		self._x = x
		self._y = y
		return None

	def __str__(self) -> str:
		return f"({self.x}, {self.y})"

	def __repr__(self) -> str:
		return f"<{self.__class__.__name__}(x: {self.x}, y: {self.y})>"

	def __iter__(self) -> Generator[Number, Any, None]:
		yield from (self.x, self.y)

	def __abs__(self) -> Number:
		return abs(self.x) + abs(self.y)

	def __eq__(self, other) -> bool:
		if self.__class__ == other.__class__:
			return (self.x == other.x) and (self.y == other.y)
		else:
			raise TypeError()

	def __ne__(self, other) -> bool:
		if self.__class__ == other.__class__:
			return not self.__eq__(other)
		else:
			raise TypeError()

	def __lt__(self, other) -> bool:
		if self.__class__ == other.__class__:
			return self.y < other.y if self.x == other.x else self.x < other.x
			# return (self.x < other.x) and (self.y < other.y)
		if isinstance(other, Number):
			return (self.x < other) and (self.y < other)
		else:
			raise TypeError()

	def __le__(self, other) -> bool:
		if self.__class__ == other.__class__:
			# return (self.x <= other.x) and (self.y <= other.y)
			return self.y <= other.y if self.x == other.x else self.x < other.x
		if isinstance(other, Number):
			return (self.x <= other) and (self.y <= other)
		else:
			raise TypeError()

	def __gt__(self, other) -> bool:
		if self.__class__ == other.__class__:
			# return (self.x > other.x) and (self.y > other.y)
			return self.y > other.y if self.x == other.x else self.x > other.x
		if isinstance(other, Number):
			return (self.x > other) and (self.y > other)
		else:
			raise TypeError()

	def __ge__(self, other) -> bool:
		if self.__class__ == other.__class__:
			# return (self.x >= other.x) and (self.y >= other.y)
			return self.y >= other.y if self.x == other.x else self.x > other.x
		if isinstance(other, Number):
			return (self.x >= other) and (self.y >= other)
		else:
			raise TypeError()

	def __hash__(self) -> int:
		return hash((self.x + self.y))

	def __neg__(self):
		return self.__class__(-self.x, -self.y)

	def __add__(self, other):
		if self.__class__ == other.__class__:
			return self.__class__(self.x + other.x, self.y + other.y)
		elif isinstance(other, Number):
			return self.__class__(self.x + other, self.y + other)
		else:
			raise TypeError()

	def __sub__(self, other):
		if self.__class__ == other.__class__:
			return self.__class__(self.x - other.x, self.y - other.y)
		elif isinstance(other, Number):
			return self.__class__(self.x - other, self.y - other)
		else:
			raise TypeError()

	def __mul__(self, other):
		"""Handle multiplier operator.

		`self` * `other`

		:param other:
		:return:
		"""
		if self.__class__ == other.__class__:
			return self.__class__(self.x * other.x, self.y * other.y)
		elif isinstance(other, Number):
			return self.__class__(self.x * other, self.y * other)
		else:
			# ValueError?
			raise TypeError('`other` must be a Point or scalar value')

	def __pow__(self, other):
		if self.__class__ == other.__class__:
			return self.cross(other)
		else:
			return NotImplemented

	def __floordiv__(self, scalar):
		""" PointA / scalar integer division operator. """
		return self.__class__(self.x // scalar, self.y // scalar)

	def __truediv__(self, scalar):
		""" PointA / scalar true (float) division operator. """
		return self.__class__(self.x / scalar, self.y / scalar)

	def __len__(self) -> int:
		return 2

	def __getitem__(self, key):
		if key == 0:
			return self.x
		elif key == 1:
			return self.y
		else:
			raise IndexError("Invalid subscript " + str(key) + " to Vec2d")

	def __getslice__(self, i, j):
		return [self.x, self.y][i:j]

	def __nonzero__(self) -> bool:
		return bool(self.x or self.y)
		# raise TypeError('Points cannot be used in Boolean contexts.')

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
	def length(self) -> Number:
		"""Get the length / magnitude."""
		return math.sqrt((self.x * self.x) + (self.y * self.y))

	@property
	def radians(self) -> Number:
		return math.atan2(self.x, self.y)

	@property
	def degrees(self) -> Number:
		return math.degrees(self.radians)

	@property
	def normalized(self):
		return Point(self.x / self.length, self.y / self.length)

	@property
	def angle(self) -> Number:
		return (math.atan2(self.x, -self.y) + math.pi * 2) % (math.pi * 2)

	def cross(self, other) -> Number:
		if self.__class__ == other.__class__:
			return (self.x * other.y) - (self.y * other.x)

	def y_mirror(self, h):
		return self.__class__(self.x, h - self.y)

	def rotated(self, total_width):
		return self.__class__(self.y, total_width - self.x)

	def distance_euclid_from(self, other) -> Number:
		x_diff = self.x - other.x
		y_diff = self.y - other.y
		x_squared = x_diff * x_diff
		y_squared = y_diff * y_diff
		return math.sqrt(x_squared + y_squared)

	def distance_manhattan_from(self, other) -> Number:
		return math.fabs(other.x - self.x) + math.fabs(other.y - self.y)

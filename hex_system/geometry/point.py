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


@dataclass
class Point:
	"""
	The x-axis (horizontal) abscissa
	The y-axis (vertical) ordinate
	"""

	def __init__(self, x: Number, y: Number) -> None:
		self._x = x
		self._y = y
		return

	def __repr__(self) -> str:
		return f"<{self.__class__.__name__}(x: {self.x}, y: {self.y})>"

	def __str__(self) -> str:
		return f"{self.__class__.__name__}({self.x}, {self.y})"

	def __lt__(self, other) -> bool:
		"""Handle less than comparator.

		`self` < `other`

		:param other: The Point to be evaluated.
		:type other: Point
		:return: True if self is less than target.
		:rtype: bool
		"""
		if self.__class__ == other.__class__:
			return self.y < other.y if self.x == other.x else self.x < other.x
		else:
			raise TypeError()

	def __le__(self, other) -> bool:
		"""Handle less than or equal comparator.

		`self` <= `other`

		:param other: The Point to be evaluated.
		:type other: Point
		:return: True if self is less than or equal to target.
		:rtype: bool
		"""
		if self.__class__ == other.__class__:
			return self.y <= other.y if self.x == other.x else self.x < other.x
		else:
			raise TypeError()

	def __eq__(self, other) -> bool:
		"""Handle equal to comparator.

		`self` == `other`

		:param other: The Point to be evaluated.
		:type other: Point
		:return: True if self is equal to the target.
		:rtype: bool
		"""
		if self.__class__ == other.__class__:
			return (self.x == other.x) and (self.y == other.y)
		elif other is None:
			return False
		else:
			raise TypeError()

	def __ne__(self, other) -> bool:
		"""Handle not equal to comparator.

		`self` != `other`

		:param other: The Point to be evaluated.
		:type other: Point
		:return: True if self is less than target.
		:rtype: bool
		"""
		if self.__class__ == other.__class__:
			return not self.__eq__(other)
		elif other is None:
			return True
		else:
			raise TypeError()

	def __gt__(self, other) -> bool:
		"""Handle greater than comparator.

		`self` > `other`

		:param other: The Point to be evaluated.
		:type other: Point
		:return: True if self is greater than target.
		:rtype: bool
		"""
		if self.__class__ == other.__class__:
			return self.y > other.y if self.x == other.x else self.x > other.x
		else:
			raise TypeError()

	def __ge__(self, other) -> bool:
		"""Handle greater than or equal to comparator.

		`self` >= `other`

		:param other: The Point to be evaluated.
		:type other: Point
		:return: True if self is greater than or equal to target.
		:rtype: bool
		"""
		if self.__class__ == other.__class__:
			return self.y >= other.y if self.x == other.x else self.x > other.x
		else:
			raise TypeError()

	def __hash__(self) -> int:
		"""Redefine the hash function to meet the consistency requirement.

		In order to put an item into a set, it needs to be hashable.
		To make an object hashable, it must meet the consistency requirement:
			a == b must imply hash(a) == hash(b)

		:return: An integer as a representation of the Point's hash.
		:rtype: int
		"""
		return hash((self.x + self.y))

	def __bool__(self) -> bool:
		"""A boolean indicating if this point is defined.

		:return: True most any case where the Point exists due to validation checks.
		:rtype: bool
		"""
		return self.x is not None and self.y is not None

	def __len__(self) -> int:
		return 2

	def __getitem__(self, key: int) -> Number:
		if key == 0:
			return self.x
		elif key == 1:
			return self.y
		else:
			raise IndexError(f"Invalid subscript: {str(key)} to Point")

	def __iter__(self) -> Generator[Number, Any, None]:
		yield from (self.x, self.y)

	def __reversed__(self) -> Generator[Number, Any, None]:
		yield from (self.y, self.x)

	def __contains__(self, item):
		"""Not appropriate for Point."""
		raise NotImplementedError()

	def __neg__(self):
		return self.__class__(-self.x, -self.y)

	def __pos__(self):
		return self

	def __abs__(self):
		return self.__class__(abs(self.x), abs(self.y))

	def __invert__(self):
		return self.__class__(self.x, -self.y)

	def __round__(self, n=None):
		return self.__class__(round(self.x, n), round(self.y, n))

	def __trunc__(self):
		return self.__class__(math.trunc(self.x), math.trunc(self.y))

	def __floor__(self):
		return self.__class__(math.floor(self.x), math.floor(self.y))

	def __ceil__(self):
		return self.__class__(math.ceil(self.x), math.ceil(self.y))

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

	def __matmul__(self, other):
		if self.__class__ == other.__class__:
			return self.x * other.y - self.y * other.x

	def __truediv__(self, scalar):
		""" PointA / scalar true (float) division operator. """
		return self.__class__(self.x / scalar, self.y / scalar)

	def __floordiv__(self, scalar):
		""" PointA / scalar integer division operator. """
		return self.__class__(self.x // scalar, self.y // scalar)

	def __lshift__(self, other):
		if other % 2:
			return self.__reversed__()
		else:
			return self

	def __rshift__(self, other):
		if other % 2:
			return self.__reversed__()
		else:
			return self


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
	def length_squared(self) -> Number:
		"""Get the length / magnitude."""
		return (self.x * self.x) + (self.y * self.y)

	@property
	def radius(self) -> Number:
		"""The distance from this point to the origin (0, 0)."""
		return math.hypot(self.x, self.y)

	@property
	def radians(self) -> Number:
		"""The angle in radians measured counter-clockwise from 3 o'clock."""
		return math.atan2(self.x, self.y)

	@property
	def degrees(self) -> Number:
		"""The angle in radians measured counter-clockwise from 3 o'clock."""
		return math.degrees(self.radians)

	@property
	def normalized(self):
		return Point(self.x / self.length, self.y / self.length)

	@property
	def angle(self) -> Number:
		return (math.atan2(self.x, -self.y) + math.pi * 2) % (math.pi * 2)

	def polar(self):
		return self.length, self.degrees

	def dot(self, other) -> Number:
		if self.__class__ == other.__class__:
			return (self.x * other.x) + (self.y * other.y)

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

#!/usr/bin/env python
# vim: ft=python
"""grid/cube.py."""
# Standard Library
from typing import (
	Generator,
	Iterator,
	List,
	NamedTuple,
	Tuple,
)

# App
from config import Number
from loggers import get_logger


__all__ = ['Cube']


class Cube:

	def __new__(cls, q: int, r: int, s: int):
		if q + r + s != 0:
			raise ValueError(f"Attributes 'q', 'r', 's' must have a sum of 0, not {q + r + s}")
		return super().__new__(cls, q, r, s)

	def __init__(self, q: int, r: int, s: int) -> None:
		"""Initialize a new Cube coordinate.

		.. note:: To be lenient we accept floats and turn them into ints, but only if they pass the new validation.

		:param q: Rightward axes.
		:param r: Axes two.
		:param s: Axes three.
		"""
		self._q: int = q
		self._r: int = r
		self._s: int = s

		return

	def __str__(self) -> str:
		return f"{self.__class__.__name__}({self.q}, {self.r}, {self.s})"

	def __repr__(self) -> str:
		return f"<{self.__class__.__name__}(x: {self.q}, y: {self.r}, s: {self.s})>"

	def __abs__(self):
		return (abs(self.q) + abs(self.r) + abs(self.s)) // 2

	def __iter__(self):
		yield self.q
		yield self.r
		yield self.s

	def __eq__(self, other) -> bool:
		if self.__class__ == other.__class:
			return self.q == other.q and self.r == other.r and self.s == other.s
		return False

	def __ne__(self, other) -> bool:
		return not self.__eq__(other)

	def __neg__(self):
		return Cube(-self.q, -self.r, -self.s)

	def __lt__(self, other) -> bool:
		if self.q < other.q and self.r < other.r and self.s < other.s:
			return True
		return False

	def __gt__(self, other) -> bool:
		if self.q > other.q and self.r > other.r and self.s > other.s:
			return True
		return False

	def __hash__(self) -> int:
		return hash(self.qrs)

	def __add__(self, other):
		return Cube(self.q + other.q, self.r + other.r, self.s + other.s)

	def __sub__(self, other):
		return Cube(self.q - other.q, self.r - other.r, self.s - other.s)

	def __mul__(self, k):
		if isinstance(k, Cube):
			return Cube(self.r * k.r, self.r * k.r, self.s * k.s)
		elif isinstance(k, int):
			return Cube(self.q * k, self.r * k, self.s * k)
		else:
			raise ValueError("Cube multiplier must be Cube or scalar")

	def __iter__(self):
		yield self.q
		yield self.r
		yield self.s

	def __getitem__(self, idx: int) -> int:
		return self.qrs[idx]

	@property
	def q(self) -> int:
		return self._q

	@property
	def r(self) -> int:
		return self._r

	@property
	def s(self) -> int:
		return self._s

	@property
	def qr(self) -> Tuple[int, int]:
		return self.q, self.r

	@property
	def qrs(self) -> Tuple[int, int, int]:
		return self.q, self.r, self.s

	@staticmethod
	def _validate(q: Number, r: Number, s: Number) -> None:
		if q + r + s != 0:
			raise ValueError(f"attributes 'q', 'r', 's' must have a sum of 0, not {q + r + s}")
		return

	def distance(self, other) -> int:
		return (abs(self.q - other.q) + abs(self.r - other.r) + abs(self.s - other.s)) / 2

	def rotate_clockwise(self):
		return Cube(-self.r, -self.s, -self.q)

	def rotate_counterclockwise(self):
		return Cube(-self.s, -self.q, -self.r)

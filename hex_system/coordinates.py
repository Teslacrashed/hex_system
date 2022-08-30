#!/usr/bin/env python
# vim: ft=python
"""coordinates.py."""
from dataclasses import (
	dataclass
)
from config import Number
from loggers import get_logger
from typing import (
	Iterator,
	Generator,
	NamedTuple,
	List,
	Tuple
)

__all__ = ['Cube', 'Offset']


@dataclass
class Offset:
	"""Create x, y coordinates.

	col = horizontal
	row = vertical
	"""
	__slots__ = ('col', 'row')
	col: int
	row: int

	def __init__(self, col: int, row: int) -> None:
		self.col = col
		self.row = row
		return

	def __repr__(self) -> str:
		return f"<{self.__class__.__name__}(col: {self.col}, row: {self.row})>"

	def __str__(self) -> str:
		return f"{self.__class__}({self.col}, {self.row})"

	def __hash__(self) -> int:
		"""
		.. note:: Maybe 31 * hash(self.col) + hash(self.row)
		:return: a unique hash
		"""
		return hash((self.col, self.row))

	def __eq__(self, other) -> bool:
		if isinstance(other, Offset):
			return self.col == other.col and self.row == other.row
		else:
			raise TypeError('Other object is not an Offset')

	def __ne__(self, other) -> bool:
		if isinstance(other, Offset):
			return not self.__eq__(other)
		else:
			raise TypeError('Other object is not an Offset')

	def __lt__(self, other) -> bool:
		if isinstance(other, Offset):
			return self.col < other.col and self.row < other.row
		else:
			raise TypeError('Other object is not an Offset')

	def __gt__(self, other) -> bool:
		if isinstance(other, Offset):
			return self.col > other.col and self.row > other.row
		else:
			raise TypeError('Other object is not an Offset')

	def __add__(self, other):
		if isinstance(other, Offset):
			return Offset(self.col + other.col, self.row + other.row)
		else:
			raise TypeError(f'Unable to add {other}')

	def __sub__(self, other):
		if isinstance(other, Offset):
			return Offset(self.col - other.col, self.row - other.row)
		else:
			raise TypeError(f'Unable to subtract {other}')

	def __iter__(self) -> Iterator[int]:
		return iter((self.col, self.row))

	def __setattr__(self, key, value) -> None:
		object.__setattr__(self, key, value)
		return

	def __getitem__(self, item) -> int:
		return self.list[item]

	def __setitem__(self, key, value) -> None:
		self.list[key] = value
		return

	def __len__(self) -> int:
		return len(self.list)

	@property
	def list(self) -> List[int]:
		return [self.col, self.row]


class Cube:

	def __new__(cls, q: Number, r: Number, s: Number):
		if q + r + s != 0:
			raise ValueError(f"Attributes 'q', 'r', 's' must have a sum of 0, not {q + r + s}")
		return super().__new__(cls)

	def __init__(self, q: Number, r: Number, s: Number) -> None:
		"""Initialize a new Cube coordinate.

		.. note:: To be lenient we accept floats and turn them into ints, but only if they pass the new validation.

		:param q: Rightward axes.
		:param r: Axes two.
		:param s: Axes three.
		"""
		self.q: int = int(q)
		self.r: int = int(r)
		self.s: int = int(s)
		return

	def __str__(self) -> str:
		return f"({self.q}, {self.r}, {self.s})"

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
		return hash((self.s, self.r, self.s))

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

	def __getitem__(self, idx: int) -> int:
		return self.qrs[idx]

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

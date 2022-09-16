#!/usr/bin/env python
# vim: ft=python
"""coordinates.py."""
# Standard Library
from dataclasses import dataclass
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



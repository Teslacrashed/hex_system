#!/usr/bin/env python
# vim: ft=python
"""grid/hex_cell.py."""
#!/usr/bin/env python
# vim: ft=python
"""hex.py.

horizontal grain / pointy top
vertical grain / flat top

qrs instead of xyz
"""
# Standard Library
import math
from typing import (
	List,
	Optional,
	Tuple,
)

# App
from config import (
	PI,
	SQRT_3,
	SQRT_3_OVER_2,
	Number,
)
from grid.cube import Cube
from grid.offset import Offset
from loggers import get_logger


LOG = get_logger(__name__)


class HexCell:
	"""A hex position in cube coordinates."""

	# NE - Clockwise
	# DIRECTION_VECTORS = {Cube(+1, -1, 0), Cube(+1, 0, -1), Cube(0, +1, -1), Cube(-1, +1, 0), Cube(-1, 0, +1), Cube(0, -1, +1)}

	def __new__(cls, cube: Cube):
		"""Ensure that created hexes have valid cube coordinates.

		:param cube: The horizontal grid coordinate of the Hexagon.
		:type cube: Cube
		"""
		if cube.q + cube.r + cube.s != 0:
			raise ValueError(f"<q: {q} r: {r} s: {s}> coordinate must equal 0.")
		return super().__new__(cls)

	def __init__(self, cube: Cube) -> None:

		self._q: int = int(cube.q)
		self._r: int = int(cube.r)
		self._s: int = int(cube.s)
		self._cube: Cube = cube

		self._col: int = int(self.q + (self.r - (self.r >> 1)) / 2)
		self._row: int = int(self.r)
		self._offset: Offset = Offset(self.col, self.row)

		return

	def __str__(self) -> str:
		return f"{self.__class__.__name__}({self.q}, {self.r}, {self.s})"

	def __repr__(self) -> str:
		return f"<{self.__class__.__name__}(q: {self.q}, r: {self.r}, s: {self.s})>"

	@property
	def offset(self) -> Offset:
		return self._offset

	@property
	def cube(self) -> Cube:
		return self._cube

	@property
	def col(self) -> int:
		return self._col

	@property
	def row(self) -> int:
		return self._row

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
		return (self.q, self.r)

	@property
	def qrs(self) -> Tuple[int, int, int]:
		return (self.q, self.r, self.s)

	#def direction(direction):
		#return self.DIRECTION_VECTORS[direction]

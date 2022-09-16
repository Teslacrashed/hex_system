#!/usr/bin/env python
# vim: ft=python
"""hex_grid.py."""
# Standard Library
from typing import (
	Dict,
	List,
	Optional,
	Tuple,
)

# First Party Library
from geometry import (
	Hexagon,
	Point,
	Rectangle,
)

# App
from loggers import get_logger
from utils import round_to_int


LOG = get_logger(__name__)


class HexGrid:
	"""Manage the container for all Hexagons."""

	def __new__(cls, cols: int, rows: int, rect: Rectangle):
		if cols == 0 or rows == 0:
			raise ValueError(f"Attributes 'cols' and 'rows' must be greater than 0.")
		return super().__new__(cls)

	def __init__(self, cols: int, rows: int, rect: Rectangle) -> None:
		"""Create rectangular hexagon grid based on desired amount of rows and columns.

		This will automatically compute pixel friendly coordinates based on the settings of :class:`geometry.Hexagon`.

		:param cols: The desired amount of columns.
		:type cols: int
		:param rows: The desired amount of rows.
		:type rows: int
		:return: A hex grid configured in a rectangle shape.
		:rtype: None
		"""
		self._log = get_logger(self.__class__.__name__)
		self._cols: int = cols
		self._rows: int = rows
		self._rect: Rectangle = rect
		self._hexagon: Hexagon = Hexagon(Point(0, 0))
		self._hexes: List[Hexagons] = []
		self._grid = self._create_grid()
		self._log.debug(f'HexGrid: {self} created.')
		return

	def __repr__(self) -> str:
		"""Output name in a debug-friendly form."""
		return f'<{self.__class__.__name__}(cols: {self.cols}, rows: {self.rows}, rect: {self.rect})>'

	def __str__(self) -> str:
		"""Output name in a human-friendly form."""
		return f'{self.__class__.__name__}({self.size}, {self.rect})'

	def _create_grid(self) -> Dict[Point, Hexagon]:
		"""Create HexGrid based on pixel coordinates."""

		grid: Dict[Point, Hexagon] = {}
		hexagons: List[Hexagon] = []

		x_start = round_to_int(self.hexagon.width / 2)
		# self._log.debug(f"<x_start: {x_start}>.")

		x_end = round_to_int(self.rect.width)
		# self._log.debug(f"<x_end: {x_end}>.")

		x_step = round_to_int(((self.hexagon.width + self.hexagon.width) / 2) + 1)
		# self._log.debug(f"<x_step: {x_step}>.")

		y_start = round_to_int(self.hexagon.height / 2)
		# self._log.debug(f"<y_start: {y_start}>.")

		y_end = round_to_int(self.rect.height)
		# self._log.debug(f"<y_end: {y_end}>.")

		y_step = round_to_int(self.hexagon.height * (3 / 4))
		# self._log.debug(f"<y_step: {y_step}>.")

		shift: bool = True

		for y in range(y_start, y_end, y_step):
			# Brilliant way to nudge odd columns to the right.
			# Toggles shift on for every other column (y position).
			shift: boot = not shift

			x_shift_val: int = round_to_int(self.hexagon.width / 2) if shift else 0

			for x in range(x_start, x_end, x_step):
				x += x_shift_val
				point: Point = Point(x, y)
				hexagon = Hexagon(point)
				# self._log.debug(hexagon)
				grid[point] = hexagon
				self._hexes.append(hexagon)
		return grid

	@property
	def origin(self) -> Point:
		return self.rect.origin

	@property
	def end(self) -> Point:
		return self.rect.end

	@property
	def hexagon(self) -> Hexagon:
		return self._hexagon

	@property
	def hexes(self) -> List[Hexagon]:
		return self._hexes

	@property
	def rows(self) -> int:
		return self._rows

	@property
	def cols(self) -> int:
		return self._cols

	@property
	def origin(self) -> Point:
		return self._origin

	@property
	def size(self) -> Tuple[int, int]:
		"""Get size of grid as a tuple"""
		return self.cols, self.rows

	@property
	def rect(self) -> Rectangle:
		return self._rect

	@property
	def grid(self) -> Dict[Point, Hexagon]:
		return self._grid

	def populate_neighbours(self, tile) -> None:
		x, y = tile.grid_position

		if x > 0:
			tile.neighbours.append(self.hexes[(x - 1, y)])

		if x < self.cols - 1:
			tile.neighbours.append(self.hexes[(x + 1, y)])

		if y > 0:
			tile.neighbours.append(self.hexes[(x, y - 1)])
			if x < self.cols - 1:
				tile.neighbours.append(self.hexes[(x + 1, y - 1)])

		if y < self.rows - 1:
			tile.neighbours.append(self.hexes[(x, y + 1)])
			if x > 0:
				tile.neighbours.append(self.hexes[(x - 1, y + 1)])
		return

	def find_path(self, from_tile, to_tiles, filter, visited=None):

		if visited is None:
			visited = []

		if not filter(from_tile) or from_tile in visited:
			return None

		if from_tile in to_tiles:
			return [from_tile]

		visited.append(from_tile)

		for neighbour in from_tile.neighbours:
			result = self.find_path(neighbour, to_tiles, filter, visited)
			if result != None:
				result.append(from_tile)
				return result

		return None

	def top_row(self):
		return [self.grid[Point(x, 0)] for x in range(self.cols)]

	def bottom_row(self):
		return [self.grid[Point(x, self.rows - 1)] for x in range(self.cols)]

	def left_column(self):
		return [self.hexes[(0, y)] for y in range(self.height)]

	def right_column(self):
		return [self.hexes[(self.width-1, y)] for y in range(self.height)]


def _create_hex_grid_rect(cols: int, rows: int) -> Rectangle:
	rect_origin = Point(0, 0)
	hexagon = Hexagon(rect_origin)

	rect_height_offset = 0 if rows & 1 else round(hexagon.height * (1 / 4))
	# LOG.debug(f"<rect_height_offset: {rect_height_offset}>.")

	rect_width: int = round_to_int(hexagon.width * cols)
	# LOG.debug(f"<rect_width: {rect_width}>.")

	rect_height: int = round_to_int((hexagon.height * rows) - rect_height_offset)
	# LOG.debug(f"<rect_height: {rect_height}>.")

	rect_end: Point = Point(rect_width, rect_height)
	# LOG.debug(f"<rect_end: {rect_end}>.")

	rect = Rectangle(rect_origin, rect_end)
	# LOG.debug(f"<rect: {rect}>.")
	return rect


def get_hex_grid(cols: int, rows: int) -> HexGrid:
	rect: Rectangle = _create_hex_grid_rect(cols, rows)
	return HexGrid(cols, rows, rect)


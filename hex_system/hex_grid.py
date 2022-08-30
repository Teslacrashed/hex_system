#!/usr/bin/env python
# vim: ft=python
"""hex_grid.py."""
from typing import (
	Dict,
	Tuple
)
from geometry import (
	Hexagon,
	Point,
	Rectangle
)
from loggers import get_logger
from utils import round_to_int


class HexGrid:
	"""Manage the container for all Hexagons."""

	grid: Dict[Point, Hexagon] = {}

	def __init__(self, cols: int, rows: int) -> None:
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
		self._cols = cols
		self._rows = rows

		self._hexagon = Hexagon(Point(0, 0))

		self._rect = self._create_rect()

		self._create_grid()

		return

	def __repr__(self) -> str:
		"""Output name in a debug-friendly form."""
		return f'<{self.__class__.__name__}(cols: {self.cols}, rows: {self.rows})>'

	def __str__(self) -> str:
		"""Output name in a human-friendly form."""
		return f'{self.__class__.__name__}({self.cols}, {self.rows})'

	def _create_rect(self) -> Rectangle:
		rect_origin: Point = Point(0, 0)
		self._log.debug(f'<rect_origin: {rect_origin}>.')

		# If the last row of hexagons is an odd number,
		# then only 3/4s of the hexagon length extends from the row above.
		# So we trim 25% off the last row.
		rect_height_offset = 0 if self.rows & 1 else round(self.hexagon.height * (1 / 4))
		self._log.debug(f"<rect_height_offset: {rect_height_offset}>.")

		rect_width: int = self.hexagon.width * self.cols
		rect_height: int = (self.hexagon.height * self.rows) - rect_height_offset

		rect_end: Point = Point(rect_width, rect_height)
		self._log.debug(f"<rect_end: {rect_end}>.")

		rect = Rectangle(rect_origin, rect_end)
		self._log.debug(f"<rect: {rect}>.")
		return rect

	def _create_grid(self) -> None:
		"""Create HexGrid based on Odd-R -> Cube coordinates."""
		x_start = round_to_int(self.hexagon.width / 2)
		self._log.debug(f"<x_start: {x_start}>.")

		x_end = round_to_int(self.rect.width)
		self._log.debug(f"<x_end: {x_end}>.")

		x_step = round_to_int(((self.hexagon.width + self.hexagon.width) / 2) + 1)
		self._log.debug(f"<x_step: {x_step}>.")

		y_start = round_to_int(self.hexagon.height / 2)
		self._log.debug(f"<y_start: {y_start}>.")

		y_end = round_to_int(self.rect.height)
		self._log.debug(f"<y_end: {y_end}>.")

		y_step = round_to_int(self.hexagon.height * (3 / 4))
		self._log.debug(f"<y_step: {y_step}>.")

		shift: bool = True

		for y in range(y_start, y_end, y_step):
			# Brilliant way to nudge odd columns to the right.
			# Toggles shift on for every other column (y position).
			shift: boot = not shift

			x_shift_val: int = int(round(self.hexagon.width / 2)) if shift else 0

			for x in range(x_start, x_end, x_step):
				x += x_shift_val
				point: Point = Point(x, y)
				hexagon = Hexagon(point)
				self._log.debug(hexagon)
				self.grid[point] = hexagon

		self._log.debug(self.grid)
		return

	@property
	def rows(self) -> int:
		return self._rows

	@property
	def cols(self) -> int:
		return self._cols

	@property
	def size(self) -> Tuple[int, int]:
		"""Get size of grid as a tuple"""
		return self.cols, self.rows

	@property
	def rect(self) -> Rectangle:
		return self._rect

	@property
	def hexagon(self) -> Hexagon:
		return self._hexagon

	def populate_neighbours(self, tile):
		x, y = tile.grid_position
		if x > 0:
			tile.neighbours.append(self.hexes[(x-1, y)])
		if x < self.width-1:
			tile.neighbours.append(self.hexes[(x+1, y)])
		if y > 0:
			tile.neighbours.append(self.hexes[(x, y-1)])
			if x < self.width-1:
				tile.neighbours.append(self.hexes[(x+1, y-1)])
		if y < self.height-1:
			tile.neighbours.append(self.hexes[(x, y+1)])
			if x > 0:
				tile.neighbours.append(self.hexes[(x-1, y+1)])

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
		return [self.hexes[(x, 0)] for x in range(self.width)]

	def bottom_row(self):
		return [self.hexes[(x, self.height-1)] for x in range(self.width)]

	def left_column(self):
		return [self.hexes[(0, y)] for y in range(self.height)]

	def right_column(self):
		return [self.hexes[(self.width-1, y)] for y in range(self.height)]

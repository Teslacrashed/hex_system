#!/usr/bin/env python
# vim: ft=python
"""tile_grid.py.

https://github.com/mha-py/hex/blob/b8499fda15998a50c376ff50a1ae23f99c815ba1/hex_show.py
"""
from collections import namedtuple
from enum import Enum
from itertools import product
import math
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from geometry import Point

from loggers import LOG


Orientation = namedtuple("Orientation", ["forward", "backward", "start_angle"])
Layout = namedtuple("Layout", ["orientation", "size", "origin"])

ORIENTATIONS = {
	'flat_ascii': Orientation(
		forward=[4, 0, 1, 2],
		backward=[0, 0, 0, 0],  # undefined
		start_angle=0.0
	)
}


class Hex:

	col: int
	row: int

	def __init__(self, q: int, r: int, s: Optional[int] = None) -> None:
		self.q = q
		self.r = r
		self.s = s if s else -q - r
		assert self.s + self.q + self.r == 0, "The sum of the 3 coordinates should be equal to 0!"
		return

	def __repr__(self) -> str:
		return f"<{self.__class__.__name__}(q: {self.q}, r: {self.r}, s: {self.s})>"

	def __hash__(self) -> int:
		""" Returns hash value of vector, enables the usage of vector as key in ``set`` and ``dict``. """
		return hash((self.q, self.r))

	def __eq__(self, other) -> bool:
		if self.__class__ == other.__class__:
			return self.q == other.q and self.r == other.r and self.s == other.s

	def __ne__(self, other) -> bool:
		if self.__class__ == other.__class__:
			return not self.__eq__(other)

	def __lt__(self, other) -> bool:
		if self.__class__ == other.__class__:
			return self.q < other.q and self.r < other.r and self.s < other.s
		else:
			raise TypeError()

	def __neg__(self):
		return self.__class__(-self.q, -self.r, -self.s)

	def __add__(self, other):
		if self.__class__ == other.__class__:
			return Hex(self.q + other.q, self.r + other.r, self.s + other.s)

	def __sub__(self, other):
		if self.__class__ == other.__class__:
			return Hex(self.q - other.q, self.r - other.r, self.s - other.s)

	def to_pixel(self, layout) -> Point:
		x = (layout.orientation.forward[0] * self.q + layout.orientation.forward[1] * self.r) * layout.size.x
		y = (layout.orientation.forward[2] * self.q + layout.orientation.forward[3] * self.r) * layout.size.y
		return Point(x + layout.origin.x, y + layout.origin.y)


hex_directions = {Hex(1, 0, -1), Hex(1, -1, 0), Hex(0, -1, 1), Hex(-1, 0, 1), Hex(-1, 1, 0), Hex(0, 1, -1)}
hex_diagonals = {Hex(2, -1, -1), Hex(1, -2, 1), Hex(-1, -1, 2), Hex(-2, 1, 1), Hex(-1, 2, -1), Hex(1, 1, -2)}


class TextColours(Enum):

	RESET: str = '\033[0m'
	RED: str = '\033[91m'
	GREEN: str = '\033[92m'
	YELLOW: str = '\033[93m'


def colourstring(text, colour):
	LOG.debug(f"<text: {text}>.")
	return TextColours[colour].value + str(text) + TextColours.RESET.value


def get_radially_symmetric_hexagonal_board(radius: int) -> Set[Hex]:
	return {Hex(*coordinates) for coordinates in product(range(-radius, radius + 1), repeat=3) if sum(coordinates) == 0}


def get_radially_symmetric_hexagonal_board2(radius: int) -> Set[Hex]:
	for coordinates in product(range(-radius, radius + 1), repeat=3):
		if sum(coordinates) == 0:
			hexagon = Hex(*coordinates)
	return {Hex(*coords) for coords in product(range(-radius, radius + 1), repeat=3) if sum(coords) == 0}


class Board:

	RADIUS: int = 5
	ORIENTATION = 'flat'
	tiles: List[Hex] = sorted(get_radially_symmetric_hexagonal_board(RADIUS))

	def __init__(self) -> None:
		""""""
		self.colours = {tile: (tile.q - tile.r) % 3 for tile in self.tiles}
		return

	def __repr__(self) -> str:
		return f"{self.__class__.__name__}()"

	def get_layout(self, size, origin):
		layout = Layout(ORIENTATIONS[self.ORIENTATION], size=Point(*size), origin=Point(*origin))
		return layout

	def draw(self) -> None:
		self._draw_ascii()
		return

	@staticmethod
	def _get_chr(q: int, r: int) -> Optional[str]:
		if 0 < q < 4 and r in [0, 2]:
			return '_'

		elif (q == 0 and r == 1) or (q == 4 and r == 2):
			return '/'

		elif (q == 0 and r == 2) or (q == 4 and r == 1):
			return '\\'

		elif q == 2 and r == 1:
			return '+'

		else:
			return None

	def _draw_ascii(self, extended: bool = True) -> None:

		n = (self.RADIUS * 2) + 1
		LOG.info(f"<n: {n}>.")

		board_width, board_height = (n * 4) + 1, (n * 2) + 1
		LOG.info(f"<board_width: {board_width}>.")
		LOG.info(f"<board_height: {board_height}>.")

		origin_x, origin_y = n // 2 * 4, n // 2 * 2
		LOG.info(f"<origin_x {origin_x}>.")
		LOG.info(f"<origin_y {origin_y}>.")

		board = [[' ' for _ in range(board_width)] for _ in range(board_height)]

		layout = Layout(ORIENTATIONS['flat_ascii'], Point(1, 1), Point(origin_x, origin_y))

		other_x, other_y = 5, 3

		LOG.info(f"<self.tiles: {len(self.tiles)}>.")

		for hexagon in self.tiles:
			# LOG.debug(f"<piece: {piece}>.")
			# LOG.debug(f"<hexagon: {hexagon}>.")

			anchor = hexagon.to_pixel(layout)
			# LOG.debug(f"<anchor: {anchor}>.")

			for x, y in product(range(other_x), range(other_y)):

				character = self._get_chr(x, y)

				if character is None:
					LOG.debug(f"character is None.")
					continue

				if character == '+':
					character = ' '

				board[anchor.y + y][anchor.x + x] = character

		board = "\n".join(["".join(row) for row in board])

		print(board)

		return

	@staticmethod
	def _get_chr_coords(x, y):
		if 0 < x < 4 and y in [0,2]:
			return '_'
		elif (x == 0 and y == 1) or (x == 4 and y == 2):
			return '/'
		elif (x == 0 and y == 2) or (x == 4 and y == 1):
			return '\\'
		elif x == 1 and y == 1:
			return 'X'
		elif x == 2 and y == 1:
			return 'Y'
		elif x == 3 and y == 1:
			return 'Z'

	@classmethod
	def _draw_ascii_coords(cls, coord_type: str = 'qrs'):

		n = (cls.RADIUS * 2) + 1

		n_x, n_y = (n * 4) + 1, (n * 2) + 1

		origin_x, origin_y = n // 2 * 4, n // 2 * 2

		board = [[' ' for _ in range(n_x)] for _ in range(n_y)]

		layout = Layout(ORIENTATIONS['flat_ascii'], Point(1, 1), Point(origin_x, origin_y))

		other_x, other_y = 5, 3

		for tile in cls.tiles:

			if coord_type == 'qrs':
				q_str = colourstring(abs(tile.q), 'GREEN' if tile.q >= 0 else 'RED')
				r_str = colourstring(abs(tile.r), 'GREEN' if tile.r >= 0 else 'RED')
				s_str = colourstring(abs(tile.s), 'GREEN' if tile.s >= 0 else 'RED')

			elif coord_type == 'offset':
				q_str, r_str, s_str = tile.col, str(tile.row), ' '

			anchor = tile.to_pixel(layout)

			for x, y in product(range(other_x), range(other_y)):
				character = cls._get_chr_coords(x, y)
				if character is not None:
					if character == 'X':
						character = q_str
					if character == 'Y':
						character = r_str
					if character == 'Z':
						character = s_str

					board[anchor.y+y][anchor.x+x] = character

		board = "\n".join(["".join(row) for row in board])

		print(board)


def main() -> None:
	LOG.info('.', type='BEGIN')
	point = Point(0, 0)

	board = Board()
	LOG.info(f"<board: {board}>.")
	# LOG.info(f"<board.dump(): {board.dump()}>.")
	# LOG.info(f"<board.tiles: {board.tiles}>.")
	# total_tiles = len(board.tiles)
	# LOG.info(f"<total_tiles: {total_tiles}>.")

	board.draw()

	LOG.info('.', type='END')

	return


if __name__ == '__main__':
	main()

#!/usr/bin/env python
# vim: ft=python
"""gui.py.

Will probably move these into a module.
Make TileMap it's own file.
"""
# Standard Library
import tkinter as tk
from typing import (
	List,
	Optional,
	Tuple,
)

# First Party Library
from geometry import (
	Hexagon,
	Line,
	Point,
	Rectangle,
)

# App
from hex_grid import (
	HexGrid,
	get_hex_grid,
)
from loggers import get_logger
from utils import round_to_int


__all__ = ['get_app']

LOG = get_logger(__name__)

WINDOW_WIDTH: int = 1280
WINDOW_HEIGHT: int = 768
WINDOW_TITLE: str = 'Hex Test'

GRID_WIDTH: int = 15
GRID_HEIGHT: int = 11

XPAD: int = 32
YPAD: int = 32

BACKGROUND_2 = '#fdf6e3'
BACKGROUND_1 = '#eee8d5'

FOREGROUND_3 = '#93a1a1'
FOREGROUND_2 = '#657b83'
FOREGROUND_1 = '#586e75'

BLACK = '#002b36'

WHITE = '#fdf6e3'
YELLOW = '#b58900'
ORANGE = '#cb4b16'
RED = '#dc322f'
MAGENTA = '#d33682'
VIOLET = '#6c71c4'
BLUE = '#268bd2'
CYAN = '#2aa198'
GREEN = '#859900'


class Root(tk.Tk):

	def __init__(self) -> None:
		super().__init__()
		self.title(WINDOW_TITLE)

		screen_width: int = self.winfo_screenwidth()
		screen_height: int = self.winfo_screenheight()
		center_x: int = round_to_int((screen_width / 2) - (WINDOW_WIDTH / 2))
		center_y: int = round_to_int((screen_height / 2) - (WINDOW_HEIGHT / 2))
		self.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{center_x}+{center_y}')

		self.resizable(False, False)

		self.option_add('*tearOff', False)
		LOG.debug(f'Root: {self} window created.')
		return

	def __str__(self) -> str:
		return f"{self.__class__.__name__}({self.title()})"

	def run(self) -> None:
		"""Run the main loop."""
		self.mainloop()
		return

	def close(self) -> None:
		self.destroy()
		self.quit()
		return


class TileMap(tk.Canvas):
	"""FIXME: Rename to TileMap? or something better."""

	def __init__(self, root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=BLACK) -> None:
		super().__init__(root, width=width, height=height, bg=bg)

		# fill entire window with canvas
		# "fill='both'" allows the canvas to stretch
		# in both x and y direction
		self.pack(expand=1, fill='both')
		self._hex_grid = get_hex_grid(GRID_WIDTH, GRID_HEIGHT)
		self._draw_hex_map()
		LOG.debug(f'TileMap: {self} created.')
		return

	def __str__(self) -> str:
		return f"{self.__class__.__name__}()"

	@property
	def cols(self) -> int:
		return self.hex_grid.cols

	@property
	def rows(self) -> int:
		return self.hex_grid.rows

	@property
	def hex_grid(self) -> HexGrid:
		return self._hex_grid

	def _draw_hexagon(
		self,
		corners: List[Point],
		color: str = BLACK,
		color1: Optional[str] = None,
		color2: Optional[str] = None,
		color3: Optional[str] = None,
		color4: Optional[str] = None,
		color5: Optional[str] = None,
		color6: Optional[str] = None,
		fill: str = GREEN,
		width: int = 2
	) -> None:

		vertex_north: Point = corners[0]
		vertex_northeast: Point = corners[1]
		vertex_southeast: Point = corners[2]
		vertex_south: Point = corners[3]
		vertex_southwest: Point = corners[4]
		vertex_northwest: Point = corners[5]

		# this setting allow to specify a different color for each edge between vertices.
		if color1 is None:
			color1 = color
		if color2 is None:
			color2 = color
		if color3 is None:
			color3 = color
		if color4 is None:
			color4 = color
		if color5 is None:
			color5 = color
		if color6 is None:
			color6 = color

		self.create_line(vertex_north.x, vertex_north.y, vertex_northeast.x, vertex_northeast.y, fill=color1, width=width)
		self.create_line(vertex_northeast.x, vertex_northeast.y, vertex_southeast.x, vertex_southeast.y, fill=color2, width=width)
		self.create_line(vertex_southeast.x, vertex_southeast.y, vertex_south.x, vertex_south.y, fill=color3, width=width)
		self.create_line(vertex_south.x, vertex_south.y, vertex_southwest.x, vertex_southwest.y, fill=color4, width=width)
		self.create_line(vertex_southwest.x, vertex_southwest.y, vertex_northwest.x, vertex_northwest.y, fill=color5, width=width)
		self.create_line(vertex_northwest.x, vertex_northwest.y, vertex_north.x, vertex_north.y, fill=color6, width=width)

		# Maybe you don't want to fill a hex, only some edges.
		if fill is not None:
			self.create_polygon(
				vertex_north.xy,
				vertex_northeast.xy,
				vertex_southeast.xy,
				vertex_south.xy,
				vertex_southwest.xy,
				vertex_northwest.xy,
				fill=fill
			)
		return

	def _draw_hex_map(self) -> None:
		for hexagon in self.hex_grid.hexes:
			# Hexagons have a property to easily get the x, y of all their vertices.
			self._draw_hexagon(hexagon.corners)
		return


class App(tk.Frame):

	def __init__(self, root: tk.Tk, *args, **kwargs) -> None:
		super().__init__(root, *args, **kwargs)
		self.pack()
		self.root = root
		self.tile_grid = TileMap(self.root)
		LOG.debug(f'App: {self} frame created.')
		return

	def __str__(self) -> str:
		return f"{self.__class__.__name__}()"

	def run(self) -> None:
		self.root.run()
		return

	def close(self) -> None:
		self.root.close()
		return


def get_app() -> App:
	return App(Root())

#!/usr/bin/env python
# vim: ft=python
"""gui.py."""
import tkinter as tk
from typing import Optional, Tuple, List
import math

from config import (
	Number
)
from geometry import (
	Hexagon,
	Line,
	Point,
	Rectangle
)
from loggers import LOG
from utils import round_to_int


WINDOW_WIDTH: int = 1280
WINDOW_HEIGHT: int = 768
WINDOW_TITLE: str = 'Hex Test'

CANVAS_WIDTH: int = 900
CANVAS_HEIGHT: int = 900

GRID_WIDTH: int = 3
GRID_HEIGHT: int = 3

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
		screen_width = self.winfo_screenwidth()
		screen_height = self.winfo_screenheight()
		center_x = int(screen_width / 2 - WINDOW_WIDTH / 2)
		center_y = int(screen_height / 2 - WINDOW_HEIGHT / 2)
		self.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{center_x}+{center_y}')
		self.resizable(False, False)

		self.option_add('*tearOff', False)
		return

	def run(self) -> None:
		"""Run the main loop."""
		self.mainloop()
		return

	def close(self) -> None:
		self.destroy()
		self.quit()
		return


class HexGrid(tk.Canvas):

	def __init__(self, root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=BLACK) -> None:
		super().__init__(root, width=width, height=height, bg=bg)

		# fill entire window with canvas
		# "fill='both'" allows the canvas to stretch
		# in both x and y direction
		self.pack(expand=1, fill='both')
		self.GRID_WIDTH = GRID_WIDTH
		self.GRID_HEIGHT = GRID_HEIGHT
		return

	def draw_hexagon(
		self,
		corners,
		color: str = FOREGROUND_1,
		color1: Optional[str] = None,
		color2: Optional[str] = None,
		color3: Optional[str] = None,
		color4: Optional[str] = None,
		color5: Optional[str] = None,
		color6: Optional[str] = None,
		fill: str = GREEN,
		width: int = 10
	) -> None:

		vertex_north = corners[0]
		vertex_northeast = corners[1]
		vertex_southeast = corners[2]
		vertex_south = corners[3]
		vertex_southwest = corners[4]
		vertex_northwest = corners[5]

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

		self.create_line(vertex_north[0], vertex_north[1], vertex_northeast[0], vertex_northeast[1], fill=color1, width=width)
		self.create_line(vertex_northeast[0], vertex_northeast[1], vertex_southeast[0], vertex_southeast[1], fill=color2, width=width)
		self.create_line(vertex_southeast[0], vertex_southeast[1], vertex_south[0], vertex_south[1], fill=color3, width=width)
		self.create_line(vertex_south[0], vertex_south[1], vertex_southwest[0], vertex_southwest[1], fill=color4, width=width)
		self.create_line(vertex_southwest[0], vertex_southwest[1], vertex_northwest[0], vertex_northwest[1], fill=color5, width=width)
		self.create_line(vertex_northwest[0], vertex_northwest[1], vertex_north[0], vertex_north[1], fill=color6, width=width)

		# Maybe you don't want to fill a hex, only some edges.
		if fill is not None:
			self.create_polygon(
				vertex_north,
				vertex_northeast,
				vertex_southeast,
				vertex_south,
				vertex_southwest,
				vertex_northwest,
				fill=fill
			)


class App(tk.Frame):

	def __init__(self, root: tk.Tk, *args, **kwargs) -> None:
		super().__init__(root, *args, **kwargs)
		self.pack()
		self.root = root
		self.grid = HexGrid(self.root)

		self.form_grid()
		return

	def form_grid(self):

		iround = lambda x: int(round(x))

		hex_side = 32.0
		hex_width =  math.floor(hex_side * math.sqrt(3))
		hex_height = hex_side * 2.0
		hex_size = hex_width, hex_height
		LOG.info(f"<hex_size: {hex_size}>.")

		grid_cols: int = 11
		grid_rows: int = 9

		rect_width: int = hex_width * grid_cols
		rect_height: int = (hex_height * grid_rows) * (4 / 5)

		rect_size = rect_width, rect_height
		LOG.info(f"<rect_size: {rect_size}>.")

		self.create_grid(hex_size, rect_size)

		return

	def run(self) -> None:
		self.root.mainloop()


def main() -> None:
	LOG.info(f".", type='BEGIN')
	app = App(Root())
	app.run()
	LOG.info(f".", type='END')


if __name__ == "__main__":
	main()

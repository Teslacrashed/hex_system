#!/user/bin/env python
# vim: ft=python
"""main.py."""
from hex_grid import HexGrid
from loggers import get_logger

from geometry import Line
from geometry import Point

from grid import (
	Cube,
	HexCell
)

LOG = get_logger(__name__)


def test_err():
	try:
		1 / 0
	except ZeroDivisionError as err:
		LOG.exception(err)


def main() -> None:
	LOG.info('.', type='BEGIN')

	# hex_grid = HexGrid(2, 2)
	# LOG.info(f"<hex_grid: {hex_grid}>.")
	#cube_1 = Cube(1, 1, -2)
	#cube_2 = Cube(1, 2, -3)
	#hexcell = HexCell(cube_1)
	#LOG.info(f"<hexcell: {hexcell}>.")

	point1 = Point(1, 1)
	LOG.info(f"<point1: {point1}>.")

	LOG.info('.', type='END')
	return


if __name__ == '__main__':
	main()

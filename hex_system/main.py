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

	first = 2, 2
	second = 2, 1
	fourth = 1, 2
	third = 1, 1

	aset = [first, second, third, fourth]

	asort = sorted(aset)

	LOG.info(f"<asort: {asort}>.")

	LOG.info('.', type='END')
	return


if __name__ == '__main__':
	main()

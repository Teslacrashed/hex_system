#!/user/bin/env python
# vim: ft=python
"""main.py."""
from hex_grid import HexGrid
from loggers import get_logger

from geometry import Line
from geometry import Point

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

	point_a = Point(-1, -1)
	point_b = Point(0, 0)

	point_1 = Point(1, 1)
	point_2 = Point(2, 2)

	line_1 = Line(point_1, point_2)
	line_2 = Line(point_1, point_2)

	LOG.info(f"<line: {line_1}>.")

	LOG.info(f"<line: {type(line_1.origin)}>.")
	LOG.info(f"<line: {type(line_1.end)}>.")

	if line_1 == line_2:
		LOG.info('line_1 is equal to line_2')
	else:
		LOG.info('line_1 is NOT equal to line_2')

	LOG.info('.', type='END')
	return


if __name__ == '__main__':
	main()

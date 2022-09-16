#!/usr/bin/env python
# vim: ft=python
"""utils.py"""
# App
from config import Number
from loggers import get_logger


LOG = get_logger(__name__)


def round_to_int(number: Number) -> int:
	"""Round a number to it's nearest integer.

	Useful for trying to get things cleanly aligned to pixel-perfect positioning.

	:param number: the number to be rounded.
	:type number: Number
	:rtype: int
	"""
	return int(round(number))

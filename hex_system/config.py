#!/usr/bin/env python
# vim: ft=python
"""config.py."""
# Standard Library
import math
from datetime import tzinfo
from os import PathLike
from pathlib import Path
from typing import Union
from zoneinfo import ZoneInfo


# Values used for common typing
Number = Union[float, int]
PathType = Union[str, PathLike]

# This goes up two directories to the root of the project/repo folder.
PROJECT_DIR: Path = Path(__file__).parent.parent.absolute()

LOG_DIR: Path = PROJECT_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

ENCODING: str = 'utf-8'

# If `TZ` is set in environment, prefer it. Fallback to America/Chicago.
# TODO: Find out how to pull from Windows environment locale and check for that as well.
TIMEZONE_LOCAL: str = 'America/Chicago'
TIMEZONE_UTC: str = 'Etc/UTC'
TZ_LOCAL: ZoneInfo = ZoneInfo(TIMEZONE_LOCAL)
TZ_UTC: ZoneInfo = ZoneInfo(TIMEZONE_UTC)

DEFAULT_TZ: ZoneInfo = TZ_LOCAL

# Universal Math Constants
PI: float = math.pi
SQRT_3: float = math.sqrt(3.0)
SQRT_3_OVER_2: float = SQRT_3 / 2.0  # COS30

# NOTE: All the below are unused, but are here as a reminder/example.
# Declare various configuration settings for our hexes and grid.

# Hex Configuration
# Hexes are oriented with 'pointy-top'
HEX_SIDE: float = 32.0
HEX_WIDTH: float = HEX_SIDE * SQRT_3
HEX_HEIGHT: float = HEX_SIDE * 2.0

# Hex Grid Configuration
HEX_GRID_COLUMNS: int = 15
HEX_GRID_ROWS: int = 11

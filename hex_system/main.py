#!/user/bin/env python
# vim: ft=python
"""main.py."""
# Standard Library
from typing import (
	Any,
	Dict,
	Optional,
	Tuple,
)

# App
from gui import get_app
from loggers import get_logger


LOG = get_logger(__name__)


def main() -> None:
	LOG.info('.', type='BEGIN')

	LOG.debug('Creating app...', type='PROCESS')
	app = get_app()
	LOG.debug('Creating app successfull')

	LOG.debug('Running app...', type='PROCESS')
	app.run()
	LOG.debug('Running app successfull.')

	LOG.info('.', type='END')
	return


if __name__ == '__main__':
	main()

#!/usr/bin/env python
# vim: ft=python
"""loggers.py."""
# Standard Library
import datetime
import logging
import time
from copy import deepcopy
from logging.handlers import RotatingFileHandler
from pathlib import Path
from sys import (
	stderr,
	stdout,
)
from types import TracebackType
from typing import (
	Any,
	Dict,
	List,
	MutableMapping,
	Optional,
	TextIO,
	Tuple,
	Type,
	TypeVar,
	Union,
)
from zoneinfo import ZoneInfo

# App
from config import (
	DEFAULT_TZ,
	ENCODING,
	LOG_DIR,
	PathType,
)


EXC_INFO_TYPE = Tuple[
	Optional[Type[BaseException]],  # type
	Optional[BaseException],  # value
	Optional[TracebackType],  # traceback
]

# Very specific exception list, for exceptions that should exit python.
FATAL_EXCEPTIONS: List[Type[BaseException]] = [KeyboardInterrupt, SystemExit]

_DEFAULT_LOG_LEVEL = logging.DEBUG if __debug__ else logging.INFO  # '-O' works like a '-q'

# Adds a `type` field to all log output, usable in logging formatter with %()
# The default log 'type' is `REPORT`.
_DEFAULT_RECORD_EXTRA: Dict[str, str] = {'type': 'REPORT'}

_DEFAULT_CONSOLE_FMT: str = '[%(name)s] [%(module)s] [%(funcName)s():] [%(lineno)-4s] [%(levelname)-8s] %(message)s'
_DEFAULT_CONSOLE_LOG_LEVEL = logging.DEBUG
_DEFAULT_CONSOLE_STREAM: TextIO = stdout

_DEFAULT_FILE_FMT: str = '[%(asctime)s] [%(name)s] [%(module)s] [%(funcName)s():] [%(lineno)-4s] [%(levelname)-7s] [%(type)-8s] %(message)s'
_DEFAULT_FILE_LOG_LEVEL: int = logging.INFO
_DEFAULT_FILE_TIMESPEC: str = 'seconds' # seconds / milliseconds / microseconds

# NOTE: Can add condition to check if Windows OS or ASCII and change
CSI: str = '\x1b['
RESET: str = f'{CSI}0m'


class NSLogRecord(logging.LogRecord):
	"""A LogRecord instance represents an event being logged.
    LogRecord instances are created and emitted via `LogEmitter`
    every time something is logged. They contain all the information
    pertinent to the event being logged.

	Enhanced precision timestamps for log records.
	"""
	_NANOSECONDS_PER_SECOND: int = 1_000_000_000

	def __init__(self, *args, **kwargs) -> None:
		self.created_ns: int = time.time_ns() / self._NANOSECONDS_PER_SECOND  # Precision: nanoseconds.
		super().__init__(*args, **kwargs)
		return


class ExtraTypeAdapter(logging.LoggerAdapter):
	"""Default extra for log type record."""

	_PROPAGATE_KWARGS: set[str] = {'exc_info', 'stack_info', 'stacklevel'}
	# Define our _EXTRA_TYPES list to catch spelling errors early.
	_EXTRA_TYPES: set[str] = {'BEGIN', 'END', 'PROCESS', 'REPORT'}

	def __init__(self, logger: logging.Logger, extra=None) -> None:
		if extra is None:
			extra = _DEFAULT_RECORD_EXTRA
		super(ExtraTypeAdapter, self).__init__(logger=logger, extra=extra)
		return

	def process(self, msg: str, kwargs: MutableMapping[str, Any]):

		new_kwargs: Dict[str, Any] = {'extra': deepcopy(self.extra) if self.extra is not None else {}}

		for key, value in kwargs.items():

			if key in self._PROPAGATE_KWARGS:
				new_kwargs[key] = value

			elif key == 'type':
				if value not in self._EXTRA_TYPES:
					raise TypeError(f"<value: {value}> is not allowed for <key: {key}>, Must be of {self._EXTRA_TYPES}.")
				new_kwargs['extra'][key] = value

			else:
				new_kwargs["extra"][key] = value

		return msg, new_kwargs


class ConsoleFormatter(logging.Formatter):
	"""Logging Formatter to add colors and count warning / errors."""

	def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None) -> None:
		if fmt is None:
			fmt = _DEFAULT_CONSOLE_FMT
		self.FORMATS = self._define_formats()
		super().__init__(fmt=fmt, datefmt=datefmt)
		return

	def _define_formats(self):
		normal = f"{CSI}37m"
		black = f"{CSI}30m"
		red = f"{CSI}31m"
		green = f"{CSI}32m"
		yellow = f"{CSI}33m"
		blue = f"{CSI}34m"
		magenta = f"{CSI}35m"
		cyan = f"{CSI}36m"
		orange = f"{CSI}91m"
		violet = f"{CSI}95m"

		format_prefix = f"[{magenta}%(name)s{RESET}] "
		format_prefix += f"[{cyan}%(module)s{RESET}] "
		format_prefix += f"[{blue}%(funcName)s():{RESET}] "
		format_prefix += f"[{violet}%(lineno)-4s{RESET}] "

		format_debug = f"[{green}%(levelname)-8s{RESET}] "
		format_info = f"[{normal}%(levelname)-8s{RESET}] "
		format_warning = f"[{yellow}%(levelname)-8s{RESET}] "
		format_error = f"[{red}%(levelname)-8s{RESET}] "
		format_critical = f"[{red}%(levelname)-8s{RESET}] "

		# TODO: Maybe `format type` match the logging level.
		format_type = f"[{orange}%(type)-7s{RESET}] "
		format_message = f"%(message)s"

		formats = {
			logging.DEBUG: format_prefix + format_debug + format_type + green + format_message + RESET,
			logging.INFO: format_prefix + format_info + format_type +  normal + format_message + RESET,
			logging.WARNING: format_prefix + format_warning + format_type + yellow + format_message + RESET,
			logging.ERROR: format_prefix + format_error + format_type + red + format_message + RESET,
			logging.CRITICAL: format_prefix + format_critical + format_type + red + format_message + RESET
		}
		return formats

	def format(self, record: logging.LogRecord) -> str:

		record.message = record.getMessage()

		if record.exc_info and not record.exc_text:
			record.exc_text = self.formatException(record.exc_info)

			if record.exc_text:
				message = record.message + ' ' + record.exc_text if record.message else record.exc_text
				record.message = record.exc_text

		log_fmt = self.FORMATS.get(record.levelno)
		formatter = logging.Formatter(log_fmt)
		return formatter.formatMessage(record)

	def formatException(self, exc_info) -> str:
		"""Format an exception to record.exc_text to print out on a single line.

		:return: The single-line string to be set to record.exc_text.
		:rtype: str
		"""
		exc_type, exc_value, _ = exc_info

		for exc in FATAL_EXCEPTIONS:
			if issubclass(exc_type, exc):
				raise

		exc_type_name = exc_type.__name__
		exc_text = f'{exc_type_name}: {exc_value}'
		return exc_text


class FileFormatter(logging.Formatter):
	"""Enhanced logging formatter for accurate timestamps with ISO-8601 compliance."""

	converter = datetime.datetime.fromtimestamp

	def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None, tz: Optional[ZoneInfo] = None, timespec: Optional[str] = None) -> None:
		if fmt is None:
			fmt: str = _DEFAULT_FILE_FMT
		if tz is None:
			self._tz = DEFAULT_TZ
		if timespec is None:
			self._timespec: str = 'seconds'
		super(FileFormatter, self).__init__(fmt=fmt, datefmt=datefmt)
		return

	def formatTime(self, record: NSLogRecord, datefmt: Optional[str] = None) -> str:
		if datefmt is not None:  # Do not handle custom formats here ...
			return super().formatTime(record, datefmt)  # ... leave to original implementation
		converted_time = self.converter(record.created_ns, tz=self._tz)
		formatted_time: str = converted_time.isoformat(sep='T', timespec=self._timespec)
		return formatted_time


class ConsoleHandler(logging.StreamHandler):
	"""Console should go to sys.stdout."""

	def __init__(self, level: Optional[int] = None) -> None:
		super().__init__()
		if level is None:
			self._level: Optional[int] = logging.ERROR
		self.stream: Optional[TextIO] = None
		return

	def emit(self, record) -> None:
		if record.levelno >= self._level:
			self.__emit(record, stderr)
		else:
			self.__emit(record, stdout)
		return

	def __emit(self, record: logging.LogRecord, stream: TextIO) -> None:
		self.stream = stream
		super().emit(record)
		return

	def flush(self) -> None:
		"""Fix closing stream handler. Workaround a bug in logging module.

		.. note:: http://bugs.python.org/issue6333.

		:rtype: None
		"""
		if self.stream and hasattr(self.stream, 'flush') and not self.stream.closed:
			logging.StreamHandler.flush(self)
		return


def get_logger(log_name: str) -> ExtraTypeAdapter:
	"""Configure log settings for the app.

	:rtype: ExtraTypeAdapter
	"""
	logging.setLogRecordFactory(NSLogRecord)

	logger = logging.getLogger(log_name)

	logger.setLevel(logging.DEBUG)
	logger.addHandler(get_console_handler())
	logger.addHandler(get_rotating_file_handler(log_name))
	return ExtraTypeAdapter(logger)


def get_console_handler() -> ConsoleHandler:
	""" Return a console stream log.
	sys.stdout is used so that doctest is able to read output produced by logging.
	Standard is to leave it empty which means sys.stderr
	"""
	handler = ConsoleHandler()
	handler.setLevel(_DEFAULT_LOG_LEVEL)
	handler.setFormatter(ConsoleFormatter())
	return handler


def get_rotating_file_handler(log_name: str) -> RotatingFileHandler:
	"""Get a log file handler."""
	extension: str = '.log'
	log_file: PathType = LOG_DIR / (log_name + extension)
	backup_count: int = 100
	max_bytes: int = 100 * 1024 * 1024  # 100 * 1MB * 1kB: 100MB


	file_handler = RotatingFileHandler(
		log_file,
		mode='a',
		maxBytes=max_bytes,
		backupCount=backup_count,
		encoding=ENCODING,
		delay=False
	)

	formatter = FileFormatter()
	file_handler.setFormatter(formatter)
	file_handler.setLevel(_DEFAULT_LOG_LEVEL)
	return file_handler


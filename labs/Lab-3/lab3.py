"""
Наследование

class A:
    ...

class B(A):
    ...

-------------

Агрегация

class A:
    ...

class B:
    def init(self, a: A) -> None:
        self.a = a

-------------

Композиция

class A:
    ...

class B:
    def init(self) -> None:
        self.a = A()


Агрегация лучше подойдет для системы логирования потому что
1. Разделение ответственности
2. Гибкость
3. С тестами удобнее будет
"""

import re
import sys
from abc import ABC, abstractmethod
from enum import Enum
from ftplib import FTP
from socket import socket, AF_INET, SOCK_STREAM
from datetime import datetime
from typing import Optional


class LogLevel(Enum):
    INFO = "INFO"
    DEBUG = "DEBUG"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# region abstract classes

class LogFilterProtocol(ABC):
    @abstractmethod
    def match(self, log_level: LogLevel, text: str) -> bool:
        pass


class LogHandlerProtocol(ABC):
    @abstractmethod
    def handle(self, log_level: LogLevel, text: str) -> None:
        pass


class LogFormatterProtocol(ABC):
    @abstractmethod
    def format(self, log_level: LogLevel, text: str) -> str:
        pass


# endregion

# region Filter classes

class SimpleLogFilter(LogFilterProtocol):
    def __init__(self, pattern: str) -> None:
        self.pattern = pattern.lower()

    def match(self, log_level: LogLevel, text: str) -> bool:
        return self.pattern in text.lower()


class ReLogFilter(LogFilterProtocol):
    def __init__(self, pattern: str) -> None:
        try:
            self.pattern = re.compile(pattern)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern {pattern}: {e}") from e

    def match(self, log_level: LogLevel, text: str) -> bool:
        return bool(self.pattern.search(text))


class LevelFilter(LogFilterProtocol):
    def __init__(self, log_level: LogLevel) -> None:
        self.log_level = log_level
        self.levels_order: dict[LogLevel, int] = {
            LogLevel.DEBUG: -1,
            LogLevel.INFO: 0,
            LogLevel.WARNING: 1,
            LogLevel.ERROR: 2,
            LogLevel.CRITICAL: 3,
        }

    def match(self, log_level: LogLevel, text: str) -> bool:
        try:
            return self.levels_order[log_level] >= self.levels_order[self.log_level]
        except KeyError as e:
            raise ValueError(f"Unknown log level: {e}")


# endregion

# region Handler classes

class ConsoleHandler(LogHandlerProtocol):
    def handle(self, log_level: LogLevel, text: str) -> None:
        print(text)


class FileHandler(LogHandlerProtocol):
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def handle(self, log_level: LogLevel, text: str) -> None:
        with open(self.filename, "a", encoding="utf-8") as file:
            file.write(f"{text}\n")


class SocketHandler(LogHandlerProtocol):
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

    def handle(self, log_level: LogLevel, text: str) -> None:
        try:
            with socket(AF_INET, SOCK_STREAM) as sock:
                sock.connect((self.host, self.port))
                sock.sendall(f"{text}\n".encode("utf-8"))

        except Exception as ex:
            print(f"[!] SocketHandler error: {ex}")


class SysLogHandler(LogHandlerProtocol):
    def handle(self, log_level: LogLevel, text: str) -> None:
        sys.stderr.write(f"SYSLOG: {text}\n")


class FtpHandler(LogHandlerProtocol):
    def __init__(self, host: str, port: int, username: str, password: str) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def handle(self, log_level: LogLevel, text: str) -> None:
        try:
            with FTP(self.host) as ftp:
                ftp.login(self.username, self.password)

                tempfile = f"temp_log_{datetime.now().timestamp()}.txt"

                with open(tempfile, "w", encoding="utf-8") as file:
                    file.write(f"{text}\n")

                with open(tempfile, "rb") as file:
                    ftp.storbinary(f"STOR {tempfile}", file)

        except Exception as ex:
            print(f"[!] FTPHandler error: {ex}")


# endregion

# region Formatter classes

class StandardFormatter(LogFormatterProtocol):
    def format(self, log_level: LogLevel, text: str) -> str:
        current_time = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        return f"{log_level.value} [{current_time}] {text}"


# endregion

class Logger:
    def __init__(self, filters: Optional[list[LogFilterProtocol]] = None,
                 handlers: Optional[list[LogHandlerProtocol]] = None,
                 formatters: Optional[list[LogFormatterProtocol]] = None) -> None:
        self.filters = filters.copy() if filters else []
        self.handlers = handlers.copy() if handlers else []
        self.formatters = formatters.copy() if formatters else []

    def log(self, log_level: LogLevel, text: str) -> None:
        try:
            text = str(text)

            for _filter in self.filters:
                if not _filter.match(log_level, text):
                    raise Exception(f"[!] Filter {_filter.__class__.__name__} failed")

            formatted_text = text

            for _formatter in self.formatters:
                formatted_text = _formatter.format(log_level, formatted_text)

            for _handler in self.handlers:
                _handler.handle(log_level, formatted_text)

        except Exception as ex:
            raise ex

    def log_info(self, text: str) -> None:
        self.log(LogLevel.INFO, text)

    def log_debug(self, text: str) -> None:
        self.log(LogLevel.DEBUG, text)

    def log_warning(self, text: str) -> None:
        self.log(LogLevel.WARNING, text)

    def log_error(self, text: str) -> None:
        self.log(LogLevel.ERROR, text)

    def log_critical(self, text: str) -> None:
        self.log(LogLevel.CRITICAL, text)

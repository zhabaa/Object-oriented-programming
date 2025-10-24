import json
import sys
import os

from enum import Enum
from types import TracebackType
from typing import Optional, Type, Self


class ANSI(Enum):
    RESET = "\033[0m"
    CLEAR = "\033[2J"
    MOVE_CURSOR = "\033[{y};{x}H"


class Color(Enum):
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"


class Printer:
    def __init__(self, color: Color, position: tuple[int, int], symbol: str, font_file: str) -> None:
        self.color: Color = color
        self.position: tuple[int, int] = position
        self.symbol: str = symbol
        self.font: dict[str, list[str]] = self._load_font(font_file)

    @staticmethod
    def _load_font(font_file: str) -> dict[str, list[str]]:
        try:
            if not os.path.exists(font_file): raise FileNotFoundError
            if not os.path.isfile(font_file): raise ValueError
            
            if font_file.endswith(".json"):
                with open(font_file, "r", encoding="utf-8") as f:
                    data: dict[str, list[str]] = json.load(f)

            elif font_file.endswith(".txt"):
                data = dict()

                with open(font_file, "r", encoding="utf-8") as f:
                    lines: list[str] = [line.rstrip("\n") for line in f]

                current_char = str()
                buffer: list[str] = list()

                for line in lines:
                    if len(line) == 1 and line.isalpha():
                        if current_char:
                            data[current_char] = buffer

                        current_char = line
                        buffer = []

                    else:
                        buffer.append(line)

                if current_char:
                    data[current_char] = buffer

            else: 
                raise ValueError("this filetype is not implemented")

            return data
            
        except Exception as e:
            raise Exception(f"Error while loading {font_file}:\n{e}")
            

    @classmethod
    def print_static(cls,
                     text: str,
                     position: tuple[int, int],
                     color: Color,
                     symbol: str,
                     font_file: str) -> None:

        font: dict[str, list[str]] = cls._load_font(font_file)
        x, y = position

        sys.stdout.write(ANSI.CLEAR.value)

        for i in range(len(next(iter(font.values())))):
            sys.stdout.write(ANSI.MOVE_CURSOR.value.format(y=y + i, x=x))
            line = str()

            for ch in text.upper():
                if ch in font:
                    line += font[ch][i].replace("#", symbol) + "  "

            sys.stdout.write(color.value + line + ANSI.RESET.value + "\n")

    def __enter__(self) -> Self:
        sys.stdout.write(ANSI.CLEAR.value)
        return self

    def __exit__(self,
                 exc_type: Optional[Type[BaseException]],
                 exc_val: Optional[BaseException],
                 exc_tb: Optional[TracebackType]) -> None:
        sys.stdout.write(ANSI.RESET.value)

    def print(self, text: str) -> None:
        x, y = self.position

        for i in range(len(next(iter(self.font.values())))):
            sys.stdout.write(ANSI.MOVE_CURSOR.value.format(y=y + i, x=x))
            line: str = ""

            for ch in text.upper():
                if ch in self.font:
                    line += self.font[ch][i].replace("#", self.symbol) + "  "

            sys.stdout.write(self.color.value + line + ANSI.RESET.value + "\n")


with Printer(Color.RED, (1, 1), "0", "fonts/font5.json") as printer:
    printer.print("swaga")

printer = Printer(Color.RED, (1, 1), "0", "fonts/font5.json")
printer.print_static("nikita", (10, 1), Color.BLUE, 'O', "fonts/font9.json")
printer.print_static("good boy", (1, 1), Color.GREEN, '+', "fonts/font5.json")

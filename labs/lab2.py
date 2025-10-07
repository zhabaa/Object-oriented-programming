import json

from enum import Enum
from typing import Optional
from dataclasses import dataclass


class Color(Enum):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    DEFAULT = 39


@dataclass
class CharacterTemplate:
    char: str
    pattern: list[str]
    width: int
    height: int


class ANSICodes:
    RESET = "\033[0m"

    @staticmethod
    def set_color(color: Color) -> str:
        return f"\033[{color.value}m"

    @staticmethod
    def set_position(row: int, col: int) -> str:
        return f"\033[{row};{col}H"

    @staticmethod
    def clear_screen() -> str:
        return "\033[2J"

    @staticmethod
    def save_cursor() -> str:
        return "\033[s"

    @staticmethod
    def restore_cursor() -> str:
        return "\033[u"


class FontLoader:
    @staticmethod
    def load_from_json(filename: str) -> dict[str, CharacterTemplate]:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        templates = {}

        for char_data in data["characters"]:
            char = char_data["char"]
            pattern = char_data["pattern"]
            height = len(pattern)
            width = max(len(line) for line in pattern) if pattern else 0

            templates[char] = CharacterTemplate(
                char=char,
                pattern=pattern,
                width=width,
                height=height
            )

        return templates

    @staticmethod
    def load_from_txt(filename: str) -> dict[str, CharacterTemplate]:
        templates = {}

        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if line and ":" in line:
                char = line.split(":")[0].strip()
                height = int(line.split(":")[1].strip())

                pattern = []

                for j in range(1, height + 1):
                    if i + j < len(lines):
                        pattern.append(lines[i + j].rstrip("\n"))

                width = max(len(line) for line in pattern) if pattern else 0

                templates[char] = CharacterTemplate(
                    char=char,
                    pattern=pattern,
                    width=width,
                    height=height
                )

                i += height + 1

            else:
                i += 1

        return templates


class Printer:
    _current_font: dict[str, CharacterTemplate] = {}
    _default_symbol: str = "*"

    def __init__(self, color: Color, position: tuple[int, int], symbol: Optional[str] = None):
        self._color: Color = color
        self._position: tuple[int, int] = position
        self._symbol: Optional[str] = symbol
        self._current_row: int = position[0]
        self._current_col: int = position[1]

    def __enter__(self):
        print(ANSICodes.save_cursor(), end="")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(ANSICodes.restore_cursor(), end="")

    @classmethod
    def load_font(cls, filename: str) -> None:
        if filename.endswith(".json"):
            cls._current_font = FontLoader.load_from_json(filename)

        else:
            cls._current_font = FontLoader.load_from_txt(filename)

    @classmethod
    def set_default_symbol(cls, symbol: str) -> None:
        cls._default_symbol = symbol

    def _render_character(self, char: str, start_row: int, start_col: int) -> None:
        if char.upper() not in self._current_font and char not in self._current_font:
            char_template = self._current_font.get("?")

            if not char_template:
                return

        else:
            char_template = self._current_font.get(char.upper(), self._current_font.get(char))

            if not char_template:
                return

        symbol = self._symbol if self._symbol else self._default_symbol

        for row, line in enumerate(char_template.pattern):
            current_row = start_row + row
            for col, pattern_char in enumerate(line):
                if pattern_char != " ":
                    print(
                        ANSICodes.set_position(current_row, start_col + col)
                        + ANSICodes.set_color(self._color)
                        + symbol
                        + ANSICodes.RESET,
                        end="",
                    )

    def print(self, text: str) -> None:
        if not self._current_font:
            raise ValueError("Please load font using Printer.load_font")

        current_row, current_col = self._position

        for char in text:
            if char == " ":
                current_col += 4
                continue

            elif char == "\n":
                current_row += self._get_font_height() + 1
                current_col = self._position[1]
                continue

            char_template = self._current_font.get(char.upper(), self._current_font.get(char))

            if char_template:
                self._render_character(char, current_row, current_col)
                current_col += char_template.width + 1

        self._current_row = current_row
        self._current_col = current_col

    @classmethod
    def print_static(cls, text: str, color: Color, position: tuple[int, int], symbol: Optional[str] = None) -> None:
        with cls(color, position, symbol) as printer:
            printer.print(text)

    def _get_font_height(self) -> int:
        if not self._current_font:
            return 0

        sample_char = next(iter(self._current_font.values()))

        return sample_char.height


def demonstrate_printer():
    print(ANSICodes.clear_screen(), end="")

    print("=== ДЕМОНСТРАЦИЯ РАБОТЫ КЛАССА PRINTER ===")

    print("\n1. Статическое использование:")

    Printer.load_font("font5.json")
    print('\n' * 5)
    Printer.print_static("STATIC", Color.RED, (0, 0), "#")
    Printer.print_static("TEXT", Color.GREEN, (11, 10), "@")

    print("\n2. Использование с контекстным менеджером:")

    print('\n' * 5)
    with Printer(Color.CYAN, (15, 10), "+") as printer:
        printer.print("CONTEXT")
        printer.print(" MANAGER")

    print("\n3. Смена шрифта (высота 7 символов):")

    Printer.load_font("font7.json")

    with Printer(Color.MAGENTA, (25, 10), "■") as printer:
        printer.print("DIFFERENT")
        printer.print(" FONT!")

    print("\n4. Разные цвета и символы:")

    colors = [Color.RED, Color.GREEN, Color.YELLOW, Color.BLUE, Color.MAGENTA]
    symbols = ["★", "♦", "♣", "♥", "♠"]

    for i, (color, symbol) in enumerate(zip(colors, symbols)):
        Printer.print_static(f"TEST{i + 1}", color, (35 + i * 8, 10), symbol)


def create_font_files():
    font5 = {
        "name": "Font5",
        "height": 5,
        "characters": [
            {"char": "A", "pattern": ["  *  ", " * * ", "*****", "*   *", "*   *"]},
            {"char": "B", "pattern": ["**** ", "*   *", "**** ", "*   *", "**** "]},
            {"char": "C", "pattern": [" ****", "*    ", "*    ", "*    ", " ****"]},
            # Добавьте другие символы по аналогии
        ],
    }

    with open("font5.json", "w", encoding="utf-8") as f:
        json.dump(font5, f, indent=2)

    # Шрифт высотой 7 символов
    font7 = {
        "name": "Font7",
        "height": 7,
        "characters": [
            {
                "char": "A",
                "pattern": [
                    "   *   ",
                    "  * *  ",
                    " *   * ",
                    "*******",
                    "*     *",
                    "*     *",
                    "*     *",
                ],
            },
            {
                "char": "B",
                "pattern": [
                    "***** ",
                    "*    *",
                    "*    *",
                    "***** ",
                    "*    *",
                    "*    *",
                    "***** ",
                ],
            },
            # Добавьте другие символы по аналогии
        ],
    }

    with open("font7.json", "w", encoding="utf-8") as f:
        json.dump(font7, f, indent=2)


if __name__ == "__main__":
    create_font_files()
    demonstrate_printer()
    input("\n\nНажмите Enter для выхода...")

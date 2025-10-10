from lab2 import Printer, Color, ANSI
import json

def demo_printer_workflow():
    """Демонстрация работы Printer с реальными примерами"""
    print("=== ДЕМОНСТРАЦИЯ РАБОТЫ PRINTER ===\n")
    
    # Создаем тестовый шрифт JSON
    test_font = {
        "A": [" # ", "# #", "###", "# #", "# #"],
        "B": ["## ", "# #", "## ", "# #", "## "],
        "C": [" ##", "#  ", "#  ", "#  ", " ##"],
        "L": ["#  ", "#  ", "#  ", "#  ", "###"],
        "O": [" ##", "# #", "# #", "# #", " ##"],
        "V": ["# #", "# #", "# #", "# #", " # "],
        "E": ["###", "#  ", "## ", "#  ", "###"],
        "U": ["# #", "# #", "# #", "# #", " # "],
        "!": [" # ", " # ", " # ", "   ", " # "],
        " ": ["   ", "   ", "   ", "   ", "   "],
        "I": ["###", " # ", " # ", " # ", "###"],
        "♥": ["# #", "###", "###", " # ", " # "]
    }
    
    # Сохраняем тестовый шрифт в файл
    with open("demo_font.json", "w", encoding="utf-8") as f:
        json.dump(test_font, f, indent=2)
    
    print("1. 📝 Базовый пример - печать текста:")
    print("Создаем Printer с зеленым цветом, позицией (1,1), символом '♡'")
    
    with Printer(Color.GREEN, (1, 1), "♡", "demo_font.json") as printer:
        printer.print("I LOVE YOU!")
    print("✅ Текст 'I LOVE YOU!' напечатан\n")
    
    print("2. 🎨 Разные цвета и символы:")
    
    # Красный текст с сердечками
    with Printer(Color.RED, (1, 10), "♥", "demo_font.json") as printer:
        printer.print("HEART")
    print("✅ Красный текст с сердечками\n")
    
    # Синий текст со звездами
    with Printer(Color.BLUE, (1, 20), "*", "demo_font.json") as printer:
        printer.print("STAR")
    print("✅ Синий текст со звездами\n")
    
    # Желтый текст с плюсиками
    with Printer(Color.YELLOW, (1, 30), "+", "demo_font.json") as printer:
        printer.print("PLUS")
    print("✅ Желтый текст с плюсиками\n")
    
    print("3. 📍 Разные позиции:")
    
    with Printer(Color.CYAN, (5, 5), "#", "demo_font.json") as printer:
        printer.print("TOP")
    print("✅ Текст в позиции (5,5)\n")
    
    with Printer(Color.MAGENTA, (10, 15), "○", "demo_font.json") as printer:
        printer.print("CENTER")
    print("✅ Текст в позиции (10,15)\n")
    
    print("4. 🎯 Статический метод:")
    
    Printer.print_static(
        text="STATIC",
        position=(15, 1),
        color=Color.WHITE,
        symbol="█",
        font_file="demo_font.json"
    )
    print("✅ Статический метод выполнен\n")
    
    print("5. 💕 Специальные символы:")
    
    with Printer(Color.RED, (20, 1), "♥", "demo_font.json") as printer:
        printer.print("LOVE")
    print("✅ Текст со специальными символами\n")
    
    # Удаляем временный файл
    import os
    os.remove("demo_font.json")
    
    print("🎊 Демонстрация завершена!")

def demo_font_loading():
    """Демонстрация загрузки разных форматов шрифтов"""
    print("\n=== ДЕМОНСТРАЦИЯ ЗАГРУЗКИ ШРИФТОВ ===\n")
    
    # Создаем JSON шрифт
    json_font = {
        "J": ["  #", "  #", "  #", "# #", " # "],
        "S": [" ##", "#  ", " # ", "  #", "## "],
        "O": [" ##", "# #", "# #", "# #", " ##"],
        "N": ["# #", "## ", "## ", "# #", "# #"]
    }
    
    with open("test_json_font.json", "w", encoding="utf-8") as f:
        json.dump(json_font, f)
    
    # Создаем TXT шрифт
    txt_font_content = """H
# #
# #
###
# #
# #
E
###
#  
## 
#  
###
L
#  
#  
#  
#  
###
"""
    with open("test_txt_font.txt", "w", encoding="utf-8") as f:
        f.write(txt_font_content)
    
    print("1. 📂 Загрузка JSON шрифта:")
    try:
        font_json = Printer._load_font("test_json_font.json")
        print(f"✅ Загружено символов: {len(font_json)}")
        print(f"   Символы: {list(font_json.keys())}")
        print(f"   Высота символов: {len(font_json['J'])}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    print("\n2. 📄 Загрузка TXT шрифта:")
    try:
        font_txt = Printer._load_font("test_txt_font.txt")
        print(f"✅ Загружено символов: {len(font_txt)}")
        print(f"   Символы: {list(font_txt.keys())}")
        print(f"   Пример символа 'H': {font_txt['H']}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    print("\n3. 🚨 Тест ошибки (неизвестный формат):")
    try:
        Printer._load_font("test.unknown")
        print("❌ Ожидалась ошибка!")
    except Exception as e:
        print(f"✅ Корректная ошибка: {e}")
    
    # Удаляем временные файлы
    import os
    os.remove("test_json_font.json")
    os.remove("test_txt_font.txt")

def demo_colors_and_symbols():
    """Демонстрация всех цветов и символов"""
    print("\n=== ДЕМОНСТРАЦИЯ ЦВЕТОВ И СИМВОЛОВ ===\n")
    
    # Создаем простой шрифт
    simple_font = {
        "A": [" # ", "# #", "###", "# #", "# #"],
        "B": ["## ", "# #", "## ", "# #", "## "]
    }
    
    with open("simple_font.json", "w", encoding="utf-8") as f:
        json.dump(simple_font, f)
    
    colors = [
        (Color.RED, "КРАСНЫЙ"),
        (Color.GREEN, "ЗЕЛЕНЫЙ"),
        (Color.YELLOW, "ЖЕЛТЫЙ"),
        (Color.BLUE, "СИНИЙ"),
        (Color.MAGENTA, "МАДЖЕНТА"),
        (Color.CYAN, "ЦИАН"),
        (Color.WHITE, "БЕЛЫЙ")
    ]
    
    symbols = ["♥", "★", "♦", "♣", "♠", "●", "■", "▲", "▼"]
    
    print("🎨 Все доступные цвета:")
    for i, (color, name) in enumerate(colors):
        with Printer(color, (i * 6 + 1, 1), "#", "simple_font.json") as printer:
            printer.print("AB")
        print(f"   {color.value}{name}{ANSI.RESET.value}")
    
    print(f"\n🔣 Примеры символов: {', '.join(symbols)}")
    
    # Удаляем временный файл
    import os
    os.remove("simple_font.json")

def demo_complex_examples():
    """Сложные примеры использования"""
    print("\n=== СЛОЖНЫЕ ПРИМЕРЫ ===\n")
    
    # Создаем расширенный шрифт
    extended_font = {
        "H": ["# #", "# #", "###", "# #", "# #"],
        "A": [" # ", "# #", "###", "# #", "# #"],
        "P": ["## ", "# #", "## ", "#  ", "#  "],
        "Y": ["# #", "# #", " # ", " # ", " # "],
        "B": ["## ", "# #", "## ", "# #", "## "],
        "R": ["## ", "# #", "## ", "# #", "# #"],
        "T": ["###", " # ", " # ", " # ", " # "],
        "D": ["## ", "# #", "# #", "# #", "## "],
        "!": [" # ", " # ", " # ", "   ", " # "],
        " ": ["   ", "   ", "   ", "   ", "   "]
    }
    
    with open("extended_font.json", "w", encoding="utf-8") as f:
        json.dump(extended_font, f)
    
    print("1. 💬 Многострочное сообщение:")
    with Printer(Color.CYAN, (1, 1), "♥", "labs/fonts/font5.json") as p1:
        p1.print("HAPPY")
    with Printer(Color.YELLOW, (7, 1), "★", "labs/fonts/font5.json") as p2:
        p2.print("BIRTHDAY!")
    print("✅ Многострочный текст создан\n")
    
    print("2. 🎭 Чередование цветов:")
    colors = [Color.RED, Color.GREEN, Color.BLUE]
    text_parts = ["HAP", "PY ", "DAY"]
    
    for i, (color, text) in enumerate(zip(colors, text_parts)):
        with Printer(color, (15, i * 8 + 1), "♦", "extended_font.json") as printer:
            printer.print(text)
    print("✅ Текст с чередованием цветов\n")
    
    print("3. 🔄 Анимация (смена символов):")
    symbols = ["●", "○", "◎", "◉", "○"]
    for symbol in symbols:
        with Printer(Color.MAGENTA, (20, 1), symbol, "extended_font.json") as printer:
            printer.print("COOL")
    print("✅ Анимация символов завершена\n")
    
    # Удаляем временный файл
    import os
    os.remove("extended_font.json")

def run_all_demos():
    """Запуск всех демонстраций"""
    print("🚀 ЗАПУСК ДЕМОНСТРАЦИИ PRINTER\n")
    
    try:
        # demo_font_loading()
        # demo_colors_and_symbols()
        # demo_printer_workflow()
        demo_complex_examples()
        
        print("\n" + "="*50)
        print("🎉 ВСЕ ДЕМОНСТРАЦИИ УСПЕШНО ЗАВЕРШЕНЫ!")
        print("="*50)
        
        print("\n💡 Пример использования из кода:")
        print('''
# Простейшее использование:
with Printer(Color.GREEN, (1, 1), "♡", "font.json") as printer:
    printer.print("I LOVE YOU!")

# Статический метод:
Printer.print_static(
    text="HELLO",
    position=(5, 5), 
    color=Color.BLUE,
    symbol="★",
    font_file="font.json"
)
        ''')
        
    except Exception as e:
        print(f"\n❌ Ошибка при демонстрации: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_demos()

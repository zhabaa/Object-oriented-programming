from lab6 import VirtualKeyboard

# Пример использования
def main():
    keyboard = VirtualKeyboard()
    
    # Тестируем базовые функции
    print("=== Testing basic functionality ===")
    keyboard.press_key("h")
    keyboard.press_key("e")
    keyboard.press_key("l")
    keyboard.press_key("l")
    keyboard.press_key("o")
    keyboard.press_key("space")
    keyboard.press_key("w")
    keyboard.press_key("o")
    keyboard.press_key("r")
    keyboard.press_key("l")
    keyboard.press_key("d")
    print(f"Text: {keyboard.get_text()}")
    
    # Тестируем backspace
    print("\n=== Testing backspace ===")
    keyboard.press_key("backspace")
    keyboard.press_key("backspace")
    print(f"Text after backspace: {keyboard.get_text()}")
    
    # Тестируем undo/redo
    print("\n=== Testing undo/redo ===")
    keyboard.undo()
    keyboard.undo()
    print(f"Text after undo: {keyboard.get_text()}")
    keyboard.redo()
    print(f"Text after redo: {keyboard.get_text()}")
    
    # Тестируем caps lock
    print("\n=== Testing caps lock ===")
    keyboard.press_key("caps")
    keyboard.press_key("t")
    keyboard.press_key("e")
    keyboard.press_key("s")
    keyboard.press_key("t")
    print(f"Text with caps: {keyboard.get_text()}")
    
    # Тестируем медиа-функции
    print("\n=== Testing media functions ===")
    keyboard.press_key("volume_up")
    keyboard.press_key("volume_up")
    keyboard.press_key("media_play")
    
    print(f"\nCurrent status:\n{keyboard.get_status()}")
    
    # Сохраняем состояние
    keyboard.save_state()
    print("\nState saved successfully!")


if __name__ == "__main__":
    main()

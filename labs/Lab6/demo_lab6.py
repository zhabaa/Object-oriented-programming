from lab6 import VirtualKeyboard, PrintCharCommand

keyboard = VirtualKeyboard()

with open("keyboard_output.txt", "w", encoding="utf-8") as file:
    def lo(text, console=True):
        if console:
            print(text)
        file.write(text + "\n")
    
    lo("=== Virtual Keyboard Demo ===")
    
    lo("Pressing keys:")
    result = keyboard.press_key('a')
    lo(f"CONSOLE: {result}")
    lo(f"TEXT FILE: {keyboard.get_output()}", False)
    
    result = keyboard.press_key('b')
    lo(f"CONSOLE: {result}")
    lo(f"TEXT FILE: {keyboard.get_output()}", False)
    
    result = keyboard.press_key('c')
    lo(f"CONSOLE: {result}")
    lo(f"TEXT FILE: {keyboard.get_output()}", False)
    
    # Отмена действий
    lo("\nUndo operations:")
    result = keyboard.undo()
    lo(f"CONSOLE: {result}")
    lo(f"TEXT FILE: {keyboard.get_output()}", False)
    
    result = keyboard.undo()
    lo(f"CONSOLE: {result}")
    lo(f"TEXT FILE: {keyboard.get_output()}", False)
    
    # Повтор действий
    lo("\nRedo operations:")
    result = keyboard.redo()
    lo(f"CONSOLE: {result}")
    lo(f"TEXT FILE: {keyboard.get_output()}", False)
    
    # Команды управления
    lo("\nControl commands:")
    result = keyboard.press_key('ctrl++')
    lo(f"CONSOLE: {result}")
    
    result = keyboard.press_key('ctrl+-')
    lo(f"CONSOLE: {result}")
    
    result = keyboard.press_key('ctrl+p')
    lo(f"CONSOLE: {result}")
    
    # Продолжение печати
    result = keyboard.press_key('d')
    lo(f"CONSOLE: {result}")
    lo(f"TEXT FILE: {keyboard.get_output()}", False)
    
    # Отмена
    lo("\nMore undo:")
    result = keyboard.undo()
    lo(f"CONSOLE: {result}")
    lo(f"TEXT FILE: {keyboard.get_output()}", False)
    
    result = keyboard.undo()
    lo(f"CONSOLE: {result}")
    
    # Демонстрация собственной команды
    lo("\nCustom command:")
    result = keyboard.press_key('caps')
    lo(f"CONSOLE: {result}")
    
    # Добавление новой привязки
    lo("\nAdding new key binding:")
    keyboard.bind_key('e', PrintCharCommand('e'))
    result = keyboard.press_key('e')
    lo(f"CONSOLE: {result}")
    lo(f"TEXT FILE: {keyboard.get_output()}", False)
    
    # Статус
    lo("\nFinal status:")
    keyboard.display_status()

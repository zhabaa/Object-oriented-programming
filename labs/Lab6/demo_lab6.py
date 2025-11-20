# interactive_tester.py
import sys
import tty
import termios
from datetime import datetime

class InteractiveKeyboardTester:
    """
    Отдельный класс для интерактивного тестирования виртуальной клавиатуры
    Не изменяет основную реализацию лабораторной работы
    """
    
    def __init__(self, keyboard_instance):
        self.keyboard = keyboard_instance
        self.log_file = "interactive_test_log.txt"
        self.original_terminal_settings = None
        self.is_running = False
        
    def enable_raw_mode(self):
        """Включение raw mode для терминала"""
        self.original_terminal_settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin.fileno())
    
    def disable_raw_mode(self):
        """Выключение raw mode"""
        if self.original_terminal_settings:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.original_terminal_settings)
    
    def get_char(self) -> str:
        """Чтение одного символа"""
        return sys.stdin.read(1)
    
    def log_interaction(self, key: str, console_output: str, file_output: str):
        """Логирование взаимодействия"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        # Вывод в консоль (только команды, не символы)
        if len(key) > 1 or key not in 'abcdefghijklmnopqrstuvwxyz0123456789':
            print(f"\r[{timestamp}] CONSOLE: {console_output}")
        else:
            print(f"\r[{timestamp}] CONSOLE: key pressed (hidden)")
        
        # Сохранение в файл (полная информация)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] KEY: '{key}' -> CONSOLE: {console_output} -> TEXT: '{file_output}'\n")
    
    def show_help(self):
        """Показать справку по командам"""
        help_text = """
=== Virtual Keyboard Interactive Test Mode ===
Type normally to input characters (they won't be shown in console)
All actions are logged to file: interactive_test_log.txt

Special commands:
  Ctrl+Z - Undo last action
  Ctrl+Y - Redo last undone action  
  Ctrl+S - Save current state
  Ctrl+Q - Quit test mode
  Ctrl+H - Show this help

For special key combinations:
  Volume Up: Type '++' 
  Volume Down: Type '--'
  Media Player: Type 'mp'
  Toggle Case: Type 'caps'

Press Enter to continue...
        """
        self.disable_raw_mode()
        print(help_text)
        input("Press Enter to continue...")
        self.enable_raw_mode()
    
    def process_command(self, char: str) -> tuple:
        """
        Обработка специальных комбинаций клавиш
        Возвращает (результат, обработано_ли)
        """
        if char == '\x1a':  # Ctrl+Z - Undo
            result = self.keyboard.undo()
            return result, True
            
        elif char == '\x19':  # Ctrl+Y - Redo
            result = self.keyboard.redo()
            return result, True
            
        elif char == '\x13':  # Ctrl+S - Save
            result = self.keyboard.save_state()
            return result, True
            
        elif char == '\x11':  # Ctrl+Q - Quit
            return "EXIT", True
            
        elif char == '\x08':  # Ctrl+H - Help
            self.show_help()
            return "Help shown", True
        
        return "", False
    
    def run_interactive_test(self):
        """Запуск интерактивного тестового режима"""
        print("=== Starting Interactive Keyboard Test ===")
        print("All keystrokes are hidden in console but fully logged to file")
        print("Press Ctrl+H for help, Ctrl+Q to quit")
        
        # Инициализация лог-файла
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write("=== Virtual Keyboard Interactive Test Session ===\n")
            f.write(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Initial text: '{self.keyboard.get_output()}'\n\n")
        
        self.is_running = True
        current_input = ""  # Для multi-char команд
        
        try:
            self.enable_raw_mode()
            
            while self.is_running:
                char = self.get_char()
                
                # Обработка специальных комбинаций
                result, processed = self.process_command(char)
                
                if processed:
                    if result == "EXIT":
                        break
                    if result:
                        key_name = f"Ctrl+{char.upper()}" if len(char) == 1 else "combo"
                        self.log_interaction(key_name, result, self.keyboard.get_output())
                else:
                    # Обычные символы
                    if char in self.keyboard.key_bindings:
                        result = self.keyboard.press_key(char)
                        self.log_interaction(char, result, self.keyboard.get_output())
                    else:
                        # Попытка multi-char команд
                        current_input += char
                        if current_input in self.keyboard.key_bindings:
                            result = self.keyboard.press_key(current_input)
                            self.log_interaction(current_input, result, self.keyboard.get_output())
                            current_input = ""
                        elif len(current_input) > 3:  # Сброс если слишком длинный
                            self.log_interaction(char, f"Unknown key", self.keyboard.get_output())
                            current_input = ""
                
                # Индикатор работы
                text_len = len(self.keyboard.get_output())
                history_len = len(self.keyboard.history)
                redo_len = len(self.keyboard.redo_stack)
                print(f"\r[Active] Text: {text_len} chars | History: {history_len} | Redo: {redo_len}", 
                      end='', flush=True)
                
        except KeyboardInterrupt:
            print("\n\nTest interrupted by user")
        except Exception as e:
            print(f"\n\nError during test: {e}")
        finally:
            self.disable_raw_mode()
            self.is_running = False
            
            # Финальный отчет
            print(f"\n\n=== Test Session Completed ===")
            print(f"Check '{self.log_file}' for complete log")
            print(f"Final text: '{self.keyboard.get_output()}'")
            print(f"Total actions: {len(self.keyboard.history)}")

# Демонстрация использования тестера
if __name__ == "__main__":
    from lab6 import VirtualKeyboard  # Импорт основной лабораторной работы
    
    print("Loading virtual keyboard...")
    keyboard = VirtualKeyboard()
    
    # Создаем тестер
    tester = InteractiveKeyboardTester(keyboard)
    
    # Запускаем интерактивный тест
    tester.run_interactive_test()

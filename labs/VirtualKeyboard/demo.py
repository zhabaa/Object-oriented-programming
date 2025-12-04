from VirtualKeyboard import VirtualKeyboard
from core.infrastructure.context import ExtensibleContext
from core.commands.commands import Command
from core.typing import CommandMetadata
from features.plugins.KeyboardPlugin import KeyboardPlugin


# region Brightness Plugin
class BrightnessController:
    def __init__(self):
        self._brightness: int = 50

    @property
    def brightness(self) -> int:
        return self._brightness

    @brightness.setter
    def brightness(self, value: int) -> None:
        self._brightness = max(0, min(100, value))

    def brightness_up(self, step: int = 10) -> int:
        self.brightness = self.brightness + step
        return self.brightness

    def brightness_down(self, step: int = 10) -> int:
        self.brightness = self.brightness - step
        return self.brightness


class BrightnessUpCommand(Command):
    def __init__(self, step: int = 10):
        self.step: int = step

    def execute(self, context: ExtensibleContext) -> CommandMetadata:
        brightness_controller = context.get_component("brightness")
        new_brightness = brightness_controller.brightness_up(self.step)
        return CommandMetadata(type="brightness_up", step=new_brightness)

    def undo(
        self, context: ExtensibleContext, metadata: CommandMetadata
    ) -> CommandMetadata:
        brightness_controller = context.get_component("brightness")
        brightness_controller.brightness_down(self.step)
        return CommandMetadata(type="undo_brightness_up")


class BrightnessDownCommand(Command):
    def __init__(self, step: int = 10):
        self.step: int = step

    def execute(self, context: ExtensibleContext) -> CommandMetadata:
        brightness_controller = context.get_component("brightness")
        new_brightness = brightness_controller.brightness_down(self.step)
        return CommandMetadata(type="brightness_down", step=new_brightness)

    def undo(
        self, context: ExtensibleContext, metadata: CommandMetadata
    ) -> CommandMetadata:
        brightness_controller = context.get_component("brightness")
        brightness_controller.brightness_up(self.step)
        return CommandMetadata(type="undo_brightness_down")


class BrightnessPlugin(KeyboardPlugin):
    """Пример плагина для управления яркостью"""

    def get_name(self) -> str:
        return "brightness"

    def setup(self, context: ExtensibleContext, binding_manager, status_provider) -> None:
        # Регистрация компонента
        context.register_component("brightness", BrightnessController())

        # Регистрация команд в менеджере плагинов
        # (предполагается, что binding_manager или plugin_manager имеет метод register_command_type)
        if hasattr(binding_manager, 'register_command_type'):
            binding_manager.register_command_type("BrightnessUpCommand", BrightnessUpCommand)
            binding_manager.register_command_type("BrightnessDownCommand", BrightnessDownCommand)

        # Привязка клавиш
        binding_manager.bind_key("brightness_up", BrightnessUpCommand())
        binding_manager.bind_key("brightness_down", BrightnessDownCommand())

        # Регистрация провайдера статуса
        def brightness_status_provider():
            brightness_controller = context.get_component("brightness")
            return (
                f"BRIGHTNESS: {brightness_controller.brightness}%"
                if brightness_controller
                else "BRIGHTNESS: N/A"
            )

        status_provider.register_status_provider(brightness_status_provider)

    def teardown(self, context: ExtensibleContext, binding_manager, status_provider) -> None:
        # Очистка при удалении плагина
        context.remove_component("brightness")
# endregion


class InteractiveDemo:
    def __init__(self):
        self.keyboard = VirtualKeyboard(plugins=[BrightnessPlugin()])
        self.running = True

    def print_menu(self):
        print(
            f"\n{'=' * 50}\n"
            f"🎮 ИНТЕРАКТИВНАЯ ДЕМОНСТРАЦИЯ VIRTUALKEYBOARD\n"
            f"{'=' * 50}\n"
            f"1. Ввод текста\n"
            f"2. Специальные клавиши (space, backspace, caps)\n"
            f"3. Управление медиа (громкость, воспроизведение)\n"
            f"4. Управление яркостью\n"
            f"5. Отмена действия (Undo)\n"
            f"6. Повтор действия (Redo)\n"
            f"7. Показать статус\n"
            f"8. Сохранить состояние\n"
            f"9. Загрузить состояние\n"
            f"0. Выход\n"
            f"{'-' * 50}"
        )

    def show_status(self):
        print("\n📊 ТЕКУЩИЙ СТАТУС:")
        print(self.keyboard.get_status())

    def handle_text_input(self):
        text = input("Введите текст для имитации набора: ")
        for char in text:
            if char == " ":
                self.keyboard.press_key("space")
            else:
                self.keyboard.press_key(char)
        print(f"✅ Текст добавлен: '{self.keyboard.get_text()}'")

    def handle_special_keys(self):
        print(f"\nСпециальные клавиши:\n1. Space\n2. Backspace\n3. Caps Lock")
        choice = input("Выберите клавишу (1-3): ")
        match choice:
            case "1":
                self.keyboard.press_key("space")
                print("✅ Space добавлен")
            case "2":
                result = self.keyboard.press_key("backspace")
                print(f"✅ {result}")
            case "3":
                self.keyboard.press_key("caps")
                print("✅ Caps Lock переключен")
            case _:
                print("❌ Неверный выбор")

    def handle_media_control(self):
        print(f"\nУправление медиа:\n1. Volume Up\n2. Volume Down\n3. Play/Pause")
        choice = input("Выберите действие (1-3): ")
        match choice:
            case "1":
                self.keyboard.press_key("volume_up")
                print("✅ Громкость увеличена")
            case "2":
                self.keyboard.press_key("volume_down")
                print("✅ Громкость уменьшена")
            case "3":
                self.keyboard.press_key("media_play")
                print("✅ Состояние воспроизведения изменено")
            case _:
                print("❌ Неверный выбор")

    def handle_brightness_control(self):
        print(f"\nУправление яркостью:\n1. Brightness Up\n2. Brightness Down")
        choice = input("Выберите действие (1-2): ")
        match choice:
            case "1":
                self.keyboard.press_key("brightness_up")
                print("✅ Яркость увеличена")
            case "2":
                self.keyboard.press_key("brightness_down")
                print("✅ Яркость уменьшена")
            case _:
                print("❌ Неверный выбор")

    def run(self):
        print("🚀 Добро пожаловать в интерактивную демонстрацию VirtualKeyboard!")
        print("Используйте меню для взаимодействия с системой.")

        while self.running:
            self.print_menu()
            choice = input("Выберите действие (0-9): ")

            try:
                match choice:
                    case "1":
                        self.handle_text_input()
                    case "2":
                        self.handle_special_keys()
                    case "3":
                        self.handle_media_control()
                    case "4":
                        self.handle_brightness_control()
                    case "5":
                        result = self.keyboard.undo()
                        print(f"✅ {result}")
                    case "6":
                        result = self.keyboard.redo()
                        print(f"✅ {result}")
                    case "7":
                        self.show_status()
                    case "8":
                        if self.keyboard.save_state():
                            print("✅ Состояние сохранено")
                        else:
                            print("❌ Ошибка сохранения состояния")
                    case "9":
                        if self.keyboard.load_state():
                            print("✅ Состояние загружено")
                        else:
                            print("❌ Ошибка загрузки состояния")
                    case "0":
                        self.running = False
                        print("👋 До свидания!")
                    case _:
                        print("❌ Неверный выбор, попробуйте снова")
            except Exception as e:
                print(f"❌ Произошла ошибка: {e}")


if __name__ == "__main__":
    demo = InteractiveDemo()
    demo.run()

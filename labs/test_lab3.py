from lab3 import (
    SimpleLogFilter,
    ReLogFilter,
    LevelFilter,
    LogLevel,
    ConsoleHandler,
    FileHandler,
    StandardFormatter,
    Logger
)



def demonstrate_logging_system():
    print("=== Демонстрация системы логирования ===\n")

    # Создаем фильтры
    keyword_filter = SimpleLogFilter("error")
    regex_filter = ReLogFilter(r"\d{4}-\d{2}-\d{2}")  # фильтр по дате в формате YYYY-MM-DD
    level_filter = LevelFilter(LogLevel.WARNING)  # пропускаем только WARN и ERROR

    # Создаем обработчики
    console_handler = ConsoleHandler()
    file_handler = FileHandler("application.log")

    # Создаем форматер
    formatter = StandardFormatter()

    # Создаем логгер с различными конфигурациями

    print("1. Логгер с выводом в консоль и фильтрацией по уровню:")
    logger1 = Logger(
        filters=[level_filter],
        formatters=[formatter],
        handlers=[console_handler]
    )

    logger1.log_info("Это информационное сообщение (не должно отобразиться)")
    logger1.log_warning("Это предупреждение")
    logger1.log_error("Это сообщение об ошибке")

    print("\n2. Логгер с записью в файл и фильтрацией по ключевому слову:")
    logger2 = Logger(
        filters=[keyword_filter],
        formatters=[formatter],
        handlers=[file_handler]
    )

    logger2.log_info("Обычное сообщение")
    logger2.log_error("Критическая ошибка в системе")

    print("\n3. Логгер с несколькими обработчиками:")
    logger3 = Logger(
        filters=[],
        formatters=[formatter],
        handlers=[console_handler, file_handler]
    )

    logger3.log_info("Сообщение для всех обработчиков")
    logger3.log_warning("Предупреждение для всех обработчиков")

    print("\n4. Логгер с регулярным выражением:")
    logger4 = Logger(
        filters=[regex_filter],
        formatters=[formatter],
        handlers=[console_handler]
    )

    logger4.log_info("Сообщение без даты")
    logger4.log_info("Сообщение с датой 2024-01-15")

    print(f"\nЛоги записаны в файл: application.log")


if __name__ == "__main__":
    demonstrate_logging_system()

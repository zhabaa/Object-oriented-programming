import pytest
import tempfile
import os
import re
from unittest.mock import Mock, patch
from labs.Lab3.lab3 import (
    Logger,
    LogLevel,
    SimpleLogFilter,
    ReLogFilter,
    LevelFilter,
    ConsoleHandler,
    FileHandler,
    SocketHandler,
    SysLogHandler,
    FtpHandler,
    StandardFormatter,
    LogFilterProtocol,
    LogHandlerProtocol,
    LogFormatterProtocol
)

# TODO: fix (
    # test_logger_with_multiple_filters
    # test_level_and_keyword_filter_combination
# )


class TestLogger:
    """Тесты для класса Logger"""
    
    def test_logger_initialization_empty(self):
        """Тест инициализации логгера без параметров"""
        logger = Logger()
        assert logger.filters == []
        assert logger.handlers == []
        assert logger.formatters == []
    
    def test_logger_initialization_with_parameters(self):
        """Тест инициализации логгера с параметрами"""
        filters: list[LogFilterProtocol] = [SimpleLogFilter("test")]
        handlers: list[LogHandlerProtocol] = [ConsoleHandler()]
        formatters: list[LogFormatterProtocol] = [StandardFormatter()]
        
        logger = Logger(filters=filters, handlers=handlers, formatters=formatters)
        
        assert len(logger.filters) == 1
        assert len(logger.handlers) == 1
        assert len(logger.formatters) == 1


class TestSimpleLogFilter:
    """Тесты для класса SimpleLogFilter"""
    
    def test_simple_filter_match_case_insensitive(self):
        """Тест поиска без учета регистра"""
        filter_obj = SimpleLogFilter("error")
        assert filter_obj.match(LogLevel.INFO, "This is an ERROR message") is True
        assert filter_obj.match(LogLevel.INFO, "This is an error message") is True
        assert filter_obj.match(LogLevel.INFO, "This is an Error message") is True
    
    def test_simple_filter_no_match(self):
        """Тест когда совпадение не найдено"""
        filter_obj = SimpleLogFilter("critical")
        assert filter_obj.match(LogLevel.INFO, "This is an error message") is False
    
    def test_simple_filter_empty_pattern(self):
        """Тест с пустым шаблоном"""
        filter_obj = SimpleLogFilter("")
        assert filter_obj.match(LogLevel.INFO, "Any message") is True
    
    def test_simple_filter_special_characters(self):
        """Тест со специальными символами"""
        filter_obj = SimpleLogFilter("user@example.com")
        assert filter_obj.match(LogLevel.INFO, "Email: user@example.com") is True
        assert filter_obj.match(LogLevel.INFO, "Email: other@example.com") is False


class TestReLogFilter:
    """Тесты для класса ReLogFilter"""
    
    def test_re_filter_match_email_pattern(self):
        """Тест поиска email с помощью регулярного выражения"""
        filter_obj = ReLogFilter(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        assert filter_obj.match(LogLevel.INFO, "Contact: user@example.com") is True
        assert filter_obj.match(LogLevel.INFO, "Contact: invalid_email") is False
    
    def test_re_filter_match_date_pattern(self):
        """Тест поиска даты с помощью регулярного выражения"""
        filter_obj = ReLogFilter(r'\d{4}-\d{2}-\d{2}')
        assert filter_obj.match(LogLevel.INFO, "Date: 2024-01-15") is True
        assert filter_obj.match(LogLevel.INFO, "Date: 2024/01/15") is False
    
    def test_re_filter_invalid_pattern(self):
        """Тест с некорректным регулярным выражением"""
        with pytest.raises(ValueError):
            ReLogFilter(r'(\d+')
    
    def test_re_filter_case_sensitive(self):
        """Тест чувствительности к регистру"""
        filter_obj = ReLogFilter(r'ERROR')
        assert filter_obj.match(LogLevel.INFO, "This is an ERROR") is True
        assert filter_obj.match(LogLevel.INFO, "This is an error") is False


class TestLevelFilter:
    """Тесты для класса LevelFilter"""
    
    def test_level_filter_higher_levels(self):
        """Тест фильтрации более высоких уровней"""
        warning_filter = LevelFilter(LogLevel.WARNING)
        
        # DEBUG и INFO должны быть отфильтрованы
        assert warning_filter.match(LogLevel.DEBUG, "Debug message") is False
        assert warning_filter.match(LogLevel.INFO, "Info message") is False
        
        # WARNING, ERROR, CRITICAL должны пройти
        assert warning_filter.match(LogLevel.WARNING, "Warning message") is True
        assert warning_filter.match(LogLevel.ERROR, "Error message") is True
        assert warning_filter.match(LogLevel.CRITICAL, "Critical message") is True
    
    def test_level_filter_debug_level(self):
        """Тест фильтра уровня DEBUG (пропускает все)"""
        debug_filter = LevelFilter(LogLevel.DEBUG)
        
        for level in LogLevel:
            assert debug_filter.match(level, "Any message") is True
    
    def test_level_filter_critical_level(self):
        """Тест фильтра уровня CRITICAL (пропускает только CRITICAL)"""
        critical_filter = LevelFilter(LogLevel.CRITICAL)
        
        assert critical_filter.match(LogLevel.DEBUG, "Debug message") is False
        assert critical_filter.match(LogLevel.INFO, "Info message") is False
        assert critical_filter.match(LogLevel.WARNING, "Warning message") is False
        assert critical_filter.match(LogLevel.ERROR, "Error message") is False
        assert critical_filter.match(LogLevel.CRITICAL, "Critical message") is True


class TestConsoleHandler:
    """Тесты для класса ConsoleHandler"""
    
    @patch('builtins.print')
    def test_console_handler_output(self, mock_print):
        """Тест вывода в консоль"""
        handler = ConsoleHandler()
        handler.handle(LogLevel.INFO, "Test message")
        
        mock_print.assert_called_once_with("Test message")


class TestFileHandler:
    """Тесты для класса FileHandler"""
    
    def test_file_handler_write(self):
        """Тест записи в файл"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as temp_file:
            temp_filename = temp_file.name
        
        try:
            handler = FileHandler(temp_filename)
            handler.handle(LogLevel.INFO, "Test log message")
            
            with open(temp_filename, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            assert content == "Test log message"
        finally:
            os.unlink(temp_filename)
    
    def test_file_handler_append_mode(self):
        """Тест что файл открывается в режиме добавления"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as temp_file:
            temp_filename = temp_file.name
            temp_file.write("Existing content\n")
        
        try:
            handler = FileHandler(temp_filename)
            handler.handle(LogLevel.WARNING, "New log message")
            
            with open(temp_filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert "Existing content" in content
            assert "New log message" in content
        finally:
            os.unlink(temp_filename)


class TestStandardFormatter:
    """Тесты для класса StandardFormatter"""
    
    def test_standard_format_structure(self):
        """Тест структуры форматированного сообщения"""
        formatter = StandardFormatter()
        result = formatter.format(LogLevel.ERROR, "Test message")
        
        # Проверяем структуру: LEVEL [TIMESTAMP] message
        assert result.startswith("ERROR [")
        assert "] Test message" in result
    
    def test_standard_format_timestamp_format(self):
        """Тест формата временной метки"""
        formatter = StandardFormatter()
        result = formatter.format(LogLevel.INFO, "Test")
        
        # Проверяем формат времени: YYYY.MM.DD HH:MM:SS
        timestamp_match = re.search(r'\[(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})\]', result)
        assert timestamp_match is not None
    
    def test_standard_format_different_levels(self):
        """Тест форматирования для разных уровней логирования"""
        formatter = StandardFormatter()
        
        for level in LogLevel:
            result = formatter.format(level, f"Message for {level.value}")
            assert result.startswith(level.value)
            assert f"Message for {level.value}" in result


class TestIntegration:
    """Интеграционные тесты"""
    
    def test_logger_with_multiple_filters(self):
        """Тест логгера с несколькими фильтрами"""
        level_filter = LevelFilter(LogLevel.WARNING)
        keyword_filter = SimpleLogFilter("important")
        
        logger = Logger(filters=[level_filter, keyword_filter])
        
        with pytest.raises(Exception, match="Filter LevelFilter failed"):
            logger.log(LogLevel.INFO, "Important info")
        
        with pytest.raises(Exception, match="Filter SimpleLogFilter failed"):
            logger.log(LogLevel.WARNING, "Regular warning")
        
        try:
            logger.log(LogLevel.WARNING, "Important warning")
            assert True
        except Exception:
            pytest.fail("Не должно было быть исключения для сообщения, проходящего все фильтры")
    
    def test_logger_with_formatter_and_handler(self):
        """Тест логгера с форматированием и обработчиком"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as temp_file:
            temp_filename = temp_file.name
        
        try:
            formatter = StandardFormatter()
            handler = FileHandler(temp_filename)
            
            logger = Logger(
                formatters=[formatter],
                handlers=[handler]
            )
            
            logger.log_info("Test integration message")
            
            with open(temp_filename, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            assert "INFO [" in content
            assert "Test integration message" in content
        finally:
            os.unlink(temp_filename)
    
    def test_convenience_methods(self):
        """Тест удобных методов логирования"""
        mock_handler = Mock()
        logger = Logger(handlers=[mock_handler])
        
        # Тестируем все удобные методы
        test_cases = [
            (logger.log_info, LogLevel.INFO, "Info message"),
            (logger.log_debug, LogLevel.DEBUG, "Debug message"),
            (logger.log_warning, LogLevel.WARNING, "Warning message"),
            (logger.log_error, LogLevel.ERROR, "Error message"),
            (logger.log_critical, LogLevel.CRITICAL, "Critical message"),
        ]
        
        for method, expected_level, message in test_cases:
            mock_handler.reset_mock()
            method(message)
            mock_handler.handle.assert_called_once()
            call_args = mock_handler.handle.call_args[0]
            assert call_args[0] == expected_level
            assert call_args[1] == message


class TestErrorScenarios:
    """Тесты сценариев с ошибками"""
    
    def test_logger_with_failing_handler(self):
        """Тест когда обработчик выбрасывает исключение"""
        # В текущей реализации логгер НЕ обрабатывает исключения в обработчиках
        # Поэтому этот тест проверяет, что исключение пробрасывается
        
        failing_handler = Mock()
        failing_handler.handle.side_effect = Exception("Handler failed")
        
        logger = Logger(handlers=[failing_handler])
        
        # Ожидаем исключение
        with pytest.raises(Exception, match="Handler failed"):
            logger.log_info("Test message")
    
    def test_empty_message_logging(self):
        """Тест логирования пустых сообщений"""
        mock_handler = Mock()
        logger = Logger(handlers=[mock_handler])
        
        logger.log_info("")
        
        mock_handler.handle.assert_called_once_with(LogLevel.INFO, "")


class TestSocketHandler:
    """Тесты для SocketHandler"""
    
    @patch('socket.socket')
    def test_socket_handler_success(self, mock_socket):
        """Тест успешной отправки через сокет"""
        mock_sock_instance = Mock()
        mock_socket.return_value.__enter__.return_value = mock_sock_instance
        
        handler = SocketHandler("localhost", 8080)
        handler.handle(LogLevel.INFO, "Test message")
        
        mock_socket.assert_called_once()
        mock_sock_instance.connect.assert_called_once_with(("localhost", 8080))
        mock_sock_instance.sendall.assert_called_once_with(b"Test message\n")


class TestSysLogHandler:
    """Тесты для SysLogHandler"""
    
    @patch('sys.stderr.write')
    def test_syslog_handler_output(self, mock_write):
        """Тест вывода в stderr"""
        handler = SysLogHandler()
        handler.handle(LogLevel.ERROR, "Error message")
        
        mock_write.assert_called_once_with("SYSLOG: Error message\n")


class TestFtpHandler:
    """Тесты для FtpHandler"""
    
    @patch('ftplib.FTP')
    @patch('builtins.open')
    def test_ftp_handler_success(self, mock_open, mock_ftp):
        """Тест успешной загрузки на FTP"""
        mock_ftp_instance = Mock()
        mock_ftp.return_value.__enter__.return_value = mock_ftp_instance
        
        mock_file = Mock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        handler = FtpHandler("ftp.example.com", 21, "user", "pass")
        handler.handle(LogLevel.INFO, "Test log message")
        
        mock_ftp.assert_called_once_with("ftp.example.com")
        mock_ftp_instance.login.assert_called_once_with("user", "pass")


class TestFilterCombinations:
    """Тесты комбинаций фильтров"""
    
    def test_level_and_keyword_filter_combination(self):
        """Тест комбинации LevelFilter и SimpleLogFilter"""

        level_filter = LevelFilter(LogLevel.ERROR)
        keyword_filter = SimpleLogFilter("database")
        
        logger = Logger(filters=[level_filter, keyword_filter])
        
        with pytest.raises(Exception, match="Filter LevelFilter failed"):
            logger.log(LogLevel.WARNING, "Database connection failed")
        
        with pytest.raises(Exception, match="Filter SimpleLogFilter failed"):
            logger.log(LogLevel.ERROR, "General system error")
        
        try:
            logger.log(LogLevel.ERROR, "Database connection timeout")
            assert True
        except Exception:
            pytest.fail("Не должно было быть исключения для сообщения 'Database connection timeout'")


class TestMultipleHandlers:
    """Тесты множественных обработчиков"""
    
    def test_multiple_handlers_all_called(self):
        """Тест что все обработчики вызываются"""
        handler1 = Mock()
        handler2 = Mock()
        handler3 = Mock()
        
        logger = Logger(handlers=[handler1, handler2, handler3])
        logger.log_info("Test message")
        
        handler1.handle.assert_called_once_with(LogLevel.INFO, "Test message")
        handler2.handle.assert_called_once_with(LogLevel.INFO, "Test message")
        handler3.handle.assert_called_once_with(LogLevel.INFO, "Test message")


class TestMultipleFormatters:
    """Тесты множественных форматтеров"""
    
    def test_multiple_formatters_chain(self):
        """Тест цепочки форматтеров"""
        formatter1 = StandardFormatter()
        formatter2 = StandardFormatter()  # Два одинаковых для демонстрации
        
        logger: Logger = Logger(formatters=[formatter1, formatter2])
        
        # Форматтеры применяются последовательно
        # Второй форматтер получит результат первого
        mock_handler = Mock()
        logger.handlers = [mock_handler]
        
        logger.log_info("Test message")
        
        # Проверяем что хендлер был вызван с отформатированным сообщением
        call_args = mock_handler.handle.call_args[0]
        assert call_args[0] == LogLevel.INFO
        assert "INFO [" in call_args[1]
        assert "Test message" in call_args[1]

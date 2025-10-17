import functools
import logging


def log(filename=None):
    """Декоратор для логирования вызовов функции в файл или консоль."""

    def decorator(func):
        logger = logging.getLogger(func.__module__ + "." + func.__name__)
        logger.setLevel(logging.INFO)
        # Очистка обработчиков, чтобы не дублировать логи
        if logger.hasHandlers():
            logger.handlers.clear()
        if filename:
            handler = logging.FileHandler(filename)
        else:
            handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Начало выполнения функции '{func.__name__}'")
            try:
                result = func(*args, **kwargs)
                logger.info(f"Функция '{func.__name__}' завершена успешно с результатом: {result}")
                return result
            except Exception as e:
                logger.error(
                    f"Функция '{func.__name__}' вызвала исключение {type(e).__name__} с параметрами args={args}, kwargs={kwargs}"
                )
                raise
            finally:
                logger.info(f"Конец выполнения функции '{func.__name__}'")

        return wrapper

    return decorator

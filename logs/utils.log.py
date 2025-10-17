import json
import logging
from typing import Dict, List

# Создание логгера для модуля utils
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

# Настройка file_handler
file_handler = logging.FileHandler("utils.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Настройка file_formatter с необходимым форматом: метка времени, название модуля, уровень, сообщение
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

# Добавление handler к логгеру
logger.addHandler(file_handler)


def load_transactions(file_path: str) -> List[Dict]:
    """
    Загружает данные о финансовых транзакциях из JSON-файла.
    В случае успеха и ошибок логгирует события.
    Если файл не найден, пустой или содержит не список — возвращает пустой список.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                logger.debug(f"Успешная загрузка данных из файла: {file_path}")
                return data
            else:
                logger.error(f"Некорректный формат данных в файле: {file_path} (ожидается список)")
                return []
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON в файле: {file_path}")
        return []

import re


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """
    Функция ищет в списке словарей операции, у которых в поле 'description'
    есть подстрока, совпадающая с регулярным выражением 'search'.

    """
    pattern = re.compile(search, re.IGNORECASE)  # регистронезависимый поиск
    return [item for item in data if "description" in item and pattern.search(item["description"])]
    pattern = re.compile(query, flags=re.IGNORECASE)
    result = []
    for item in data:
        desc = item.get("description")
        if desc and pattern.search(desc):
            result.append(item)
    return result


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """
    Функция подсчитывает количество операций из списка data,
    описание которых (поле 'description') содержит подстроку из списка категорий.

    """
    result = {category: 0 for category in categories}
    for operation in data:
        desc = operation.get("description", "").lower()
        for category in categories:
            if category.lower() in desc:
                result[category] += 1
    return result

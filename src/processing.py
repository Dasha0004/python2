from typing import List, Dict, Any

def filter_by_state(items: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    """
    Фильтрует список словарей по значению ключа 'state'.
    """
    return [item for item in items if item.get('state') == state]

def sort_by_date(items: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список словарей по ключу 'date'.
    """
    return sorted(items, key=lambda x: x.get('date', ''), reverse=descending)

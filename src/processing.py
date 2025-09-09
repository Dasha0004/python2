def filter_by_state(items, state='EXECUTED'):
    """
    Фильтрует список словарей по значению ключа 'state'.

    """
    return [item for item in items if item.get('state') == state]



def sort_by_date(items, descending=True):
    """
    Сортирует список словарей по ключу 'date'.

    """
    return sorted(items, key=lambda x: x.get('date', ''), reverse=descending)

import pytest

from src.processing import filter_by_state


@pytest.mark.parametrize("state, expected_ids", [
    ('EXECUTED', [1, 3]),
    ('PENDING', [2]),
    ('CANCELLED', []),  # нет элементов с таким статусом
])
def test_filter_by_state(state, expected_ids):
    items = [
        {'state': 'EXECUTED', 'id': 1},
        {'state': 'PENDING', 'id': 2},
        {'state': 'EXECUTED', 'id': 3},
    ]
    filtered = filter_by_state(items, state)
    filtered_ids = [item['id'] for item in filtered]

    # Проверяем, что все статусы соответствуют фильтруемому состоянию
    assert all(item['state'] == state for item in filtered)
    # Проверяем корректность выборки по id
    assert filtered_ids == expected_ids

    import pytest
    from typing import List, Dict, Any

    # Исходная функция
    def sort_by_date(items: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
        return sorted(items, key=lambda x: x.get('date', ''), reverse=descending)

    # Тесты для функции сортировки по дате
    @pytest.mark.parametrize("items, descending, expected_order", [
        (
                [
                    {'date': '2023-01-02', 'id': 1},
                    {'date': '2023-01-01', 'id': 2},
                    {'date': '2023-01-03', 'id': 3},
                ],
                True,
                [3, 1, 2],
        ),
        (
                [
                    {'date': '2023-01-02', 'id': 1},
                    {'date': '2023-01-01', 'id': 2},
                    {'date': '2023-01-03', 'id': 3},
                ],
                False,
                [2, 1, 3],
        ),
        (
                [
                    {'date': '2023-01-01', 'id': 1},
                    {'date': '2023-01-01', 'id': 2},
                    {'date': '2023-01-02', 'id': 3},
                ],
                True,
                [3, 1, 2],
        ),
    ])
    def test_sort_by_date(items, descending, expected_order):
        sorted_items = sort_by_date(items, descending)
        sorted_ids = [item['id'] for item in sorted_items]
        assert sorted_ids == expected_order

    def test_sort_with_incorrect_dates():
        items = [
            {'date': '2023-01-01', 'id': 1},
            {'date': 'not-a-date', 'id': 2},
            {'id': 3},  # нет ключа 'date'
            {'date': '', 'id': 4},
        ]
        # Ожидаем, что элементы с некорректными или пустыми датами будут в начале (при descending=True),
        # т.к. сортировка идет по строкам, пустая строка и "not-a-date" идут раньше дат в ISO формате.
        sorted_items = sort_by_date(items, descending=True)
        sorted_dates = [item.get('date', '') for item in sorted_items]

        # Проверяем, что сортируется без ошибки и элементы с невалидной датой возвращаются с ожидаемым порядком
        assert sorted_dates == ['not-a-date', '', '2023-01-01', '']

    def test_sort_with_empty_list():
        assert sort_by_date([]) == []

import pytest
from typing import List, Dict, Any

def sort_by_date(items: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    return sorted(items, key=lambda x: x.get('date', ''), reverse=descending)

# Фикстуры с различными вариантами данных, включая ключи 'date' и 'state'
@pytest.fixture
def data_typical():
    return [
        {'date': '2023-01-02', 'state': 'new', 'id': 1},
        {'date': '2023-01-01', 'state': 'processed', 'id': 2},
        {'date': '2023-01-03', 'state': 'new', 'id': 3},
    ]

@pytest.fixture
def data_with_same_date():
    return [
        {'date': '2023-01-01', 'state': 'new', 'id': 1},
        {'date': '2023-01-01', 'state': 'processed', 'id': 2},
        {'date': '2023-01-02', 'state': 'closed', 'id': 3},
    ]

@pytest.fixture
def data_with_invalid_dates():
    return [
        {'date': '2023-01-01', 'state': 'new', 'id': 1},
        {'date': 'wrong-date', 'state': 'processed', 'id': 2},
        {'state': 'closed', 'id': 3},  # нет даты
        {'date': '', 'state': 'new', 'id': 4},
    ]

@pytest.fixture
def empty_data():
    return []

# Тесты с использованием фикстур
def test_sort_descending(data_typical):
    sorted_items = sort_by_date(data_typical, descending=True)
    ids = [i['id'] for i in sorted_items]
    assert ids == [3, 1, 2]

def test_sort_ascending(data_typical):
    sorted_items = sort_by_date(data_typical, descending=False)
    ids = [i['id'] for i in sorted_items]
    assert ids == [2, 1, 3]

def test_sort_same_dates(data_with_same_date):
    sorted_items = sort_by_date(data_with_same_date, descending=True)
    ids = [i['id'] for i in sorted_items]
    # Последовательность по дате, при одинаковых датах исходный порядок сохраняется (стабильность сортировки)
    assert ids == [3, 1, 2]

def test_sort_with_invalid_dates(data_with_invalid_dates):
    sorted_items = sort_by_date(data_with_invalid_dates, descending=True)
    dates = [item.get('date', '') for item in sorted_items]
    # Некорректные/пустые даты сортируются по строкам, могут идти первыми
    assert 'wrong-date' in dates
    assert '' in dates
    assert '2023-01-01' in dates

def test_sort_empty(empty_data):
    assert sort_by_date(empty_data) == []

# Тестирование возможных исключений
def test_sort_raises_on_non_list():
    with pytest.raises(TypeError):
        sort_by_date(None)   # Передаем None вместо списка

def test_sort_raises_on_item_not_dict():
    with pytest.raises(AttributeError):
        # Один из элементов не словарь
        sort_by_date(['string', {'date': '2023-01-01'}])
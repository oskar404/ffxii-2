import pytest
from temporalrift import search


def test_minimal():
    result = search(0, [1])
    print(result)
    assert len(result) == 1
    assert result[0] == [(0, 1)]


def test_simple():
    clock = [1, 2, 1, 1]
    path1 = [(0, 1), (3, 1), (2, 1), (1, 2)]
    path2 = [(0, 1), (1, 2), (3, 1), (2, 1)]
    result = search(0, clock)
    print(result)
    assert len(result) == 2
    assert path1 in result
    assert path2 in result


def test_complex():
    start = 7
    clock = [4, 1, 4, 3, 1, 4, 2, 3, 5, 2]
    path = [
        (7, 3),
        (0, 4),
        (4, 1),
        (5, 4),
        (9, 2),
        (1, 1),
        (2, 4),
        (6, 2),
        (8, 5),
        (3, 3),
    ]
    result = search(start, clock)
    print(result)
    print(f"len(result) -> {len(result)}")
    assert path in result

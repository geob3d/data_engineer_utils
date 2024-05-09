from __future__ import annotations

from data_engineer_utils.main import get_hello


def it_prints_hi_to_the_project_author() -> None:
    expected = 'Hello, George Buahin!'
    actual = get_hello('George Buahin')
    assert actual == expected

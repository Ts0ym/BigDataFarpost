import pytest
import requests
from unittest.mock import Mock
from cat_fact_processor import CatFactProcessor, APIError


# --- Тесты для метода get_fact ---

def test_get_fact_success(monkeypatch):
    fake_fact = "This is the fake fact."
    fake_response = Mock()
    fake_response.json.return_value = {"fact": fake_fact}
    fake_response.status_code = 200
    fake_response.raise_for_status = Mock()
    monkeypatch.setattr(requests, "get", Mock(return_value=fake_response))

    processor = CatFactProcessor()
    processor.get_fact()
    assert processor.last_fact == fake_fact


def test_get_fact_http_error(monkeypatch):
    # Имитация ответа, который возвращает ошибочный статус
    fake_response = Mock()
    fake_response.status_code = 404
    fake_response.raise_for_status.side_effect = requests.HTTPError("404 Client Error")
    monkeypatch.setattr(requests, "get", Mock(return_value=fake_response))

    processor = CatFactProcessor()
    with pytest.raises(APIError) as exc_info:
        processor.get_fact()
    assert "Ошибка при запросе к API:" in str(exc_info.value)


def test_get_fact_invalid_json(monkeypatch):
    # Имитация ответа, в котором отсутствует ключ "fact"
    fake_response = Mock()
    fake_response.json.return_value = {"invalid_key": "No fact here"}
    fake_response.status_code = 200
    fake_response.raise_for_status = Mock()
    monkeypatch.setattr(requests, "get", Mock(return_value=fake_response))

    processor = CatFactProcessor()
    # Ожидается, что при отсутствии ключа "fact" будет выброшен KeyError
    with pytest.raises(KeyError):
        processor.get_fact()


# --- Тесты для метода get_fact_analysis ---

def test_get_fact_analysis_empty():
    processor = CatFactProcessor()
    analysis = processor.get_fact_analysis()
    assert analysis == {"length": 0, "letter_frequencies": {}}


def test_get_fact_analysis_non_empty():
    processor = CatFactProcessor()
    test_fact = "Meow"
    processor.last_fact = test_fact
    analysis = processor.get_fact_analysis()
    expected = {
        "length": len(test_fact),
        "letter_frequencies": {"m": 1, "e": 1, "o": 1, "w": 1}
    }
    assert analysis == expected


def test_get_fact_analysis_with_punctuation():
    processor = CatFactProcessor()
    # Строка с буквами, пробелами, знаками препинания и цифрами
    test_fact = "Hello, World! 123"
    processor.last_fact = test_fact
    analysis = processor.get_fact_analysis()
    # Приводим строку к нижнему регистру: "hello, world! 123"
    # Ожидаемые частоты: h:1, e:1, l:3, o:2, ,:1, " ":3, w:1, r:1, d:1, !:1, 1:1, 2:1, 3:1
    expected_freq = {
        "h": 1, "e": 1, "l": 3, "o": 2,
        ",": 1, " ": 3, "w": 1, "r": 1,
        "d": 1, "!": 1, "1": 1, "2": 1, "3": 1
    }
    expected = {
        "length": len(test_fact),
        "letter_frequencies": expected_freq
    }
    assert analysis == expected


def test_get_fact_analysis_with_spaces():
    processor = CatFactProcessor()
    test_fact = "   "  # три пробела
    processor.last_fact = test_fact
    analysis = processor.get_fact_analysis()
    expected = {
        "length": 3,
        "letter_frequencies": {" ": 3}
    }
    assert analysis == expected


def test_get_fact_analysis_return_types():
    processor = CatFactProcessor()
    test_fact = "Test"
    processor.last_fact = test_fact
    analysis = processor.get_fact_analysis()
    assert isinstance(analysis["length"], int)
    assert isinstance(analysis["letter_frequencies"], dict)
    # Проверим, что ключи словаря – строки, а значения – числа
    for key, value in analysis["letter_frequencies"].items():
        assert isinstance(key, str)
        assert isinstance(value, int)


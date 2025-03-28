import pytest

from utils import language_utils


@pytest.mark.parametrize(
    "text, split_types, expected",
    [
        (
            "",
            ["korean", "hanja", "english"],
            {"korean": "", "hanja": "", "english": ""},
        ),
        (
            "안녕하세요",
            ["korean", "hanja", "english"],
            {"korean": "안녕하세요", "hanja": "", "english": ""},
        ),
        (
            "Hello",
            ["korean", "hanja", "english"],
            {"korean": "", "hanja": "", "english": "Hello"},
        ),
        (
            "漢字",
            ["korean", "hanja", "english"],
            {"korean": "", "hanja": "漢字", "english": ""},
        ),
        (
            "안녕 Hello",
            ["korean", "hanja", "english"],
            {"korean": "안녕", "hanja": "", "english": "Hello"},
        ),
        (
            "안녕 漢字",
            ["korean", "hanja", "english"],
            {"korean": "안녕", "hanja": "漢字", "english": ""},
        ),
        (
            "Hello 漢字",
            ["korean", "hanja", "english"],
            {"korean": "", "hanja": "漢字", "english": "Hello"},
        ),
        (
            "안녕 Hello 漢字",
            ["korean", "hanja", "english"],
            {"korean": "안녕", "hanja": "漢字", "english": "Hello"},
        ),
    ],
)
def test_split_text(
    text: str, split_types: list[str], expected: dict[str, str]
) -> None:
    results: dict[str, str] = language_utils.split_text(
        text=text, split_types=split_types
    )
    assert results == expected


@pytest.mark.parametrize(
    "text, languages_to_detect, expected",
    [
        (
            "",
            ["korean", "hanja", "english"],
            {"korean": False, "hanja": False, "english": False},
        ),
        (
            "안녕하세요",
            ["korean", "hanja", "english"],
            {"korean": True, "hanja": False, "english": False},
        ),
        (
            "Hello",
            ["korean", "hanja", "english"],
            {"korean": False, "hanja": False, "english": True},
        ),
        (
            "漢字",
            ["korean", "hanja", "english"],
            {"korean": False, "hanja": True, "english": False},
        ),
        (
            "안녕 Hello",
            ["korean", "hanja", "english"],
            {"korean": True, "hanja": False, "english": True},
        ),
        (
            "안녕 漢字",
            ["korean", "hanja", "english"],
            {"korean": True, "hanja": True, "english": False},
        ),
        (
            "Hello 漢字",
            ["korean", "hanja", "english"],
            {"korean": False, "hanja": True, "english": True},
        ),
        (
            "안녕 Hello 漢字",
            ["korean", "hanja", "english"],
            {"korean": True, "hanja": True, "english": True},
        ),
    ],
)
def test_detect_languages(
    text: str, languages_to_detect: list[str], expected: dict[str, str]
) -> None:
    results: dict[str, bool] = language_utils.detect_languages(
        text=text, languages_to_detect=languages_to_detect
    )
    assert results == expected

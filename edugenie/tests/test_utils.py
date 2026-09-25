import pytest

from config import Settings
from utils import (
    clean_json_block,
    parse_json
)


def test_clean_json_block():

    result = clean_json_block(
        '```json\n[{"a": 1}]\n```'
    )

    assert result == '[{"a": 1}]'


def test_parse_json_with_fence():

    result = parse_json(
        '```json\n{"answer": 42}\n```'
    )

    assert result == {
        "answer": 42
    }


def test_parse_invalid_json():

    with pytest.raises(Exception):

        parse_json(
            "not json"
        )


def test_default_gemini_model_is_supported():

    settings = Settings()

    assert settings.gemini_model == "gemini-3.6-flash"
import json
import re

from typing import Any


def clean_json_block(value: str) -> str:

    value = value.strip()

    value = re.sub(
        r"^```(?:json)?\s*",
        "",
        value,
        flags=re.IGNORECASE
    )

    value = re.sub(
        r"\s*```$",
        "",
        value
    )

    return value.strip()


def parse_json(value: str) -> Any:

    cleaned = clean_json_block(value)

    try:

        return json.loads(cleaned)

    except json.JSONDecodeError:

        # Attempt to locate JSON embedded
        # inside additional model text.

        first_array = cleaned.find("[")

        first_object = cleaned.find("{")

        starts = [
            x
            for x in (
                first_array,
                first_object
            )
            if x >= 0
        ]

        if not starts:

            raise

        start = min(starts)

        last_array = cleaned.rfind("]")

        last_object = cleaned.rfind("}")

        end = max(
            last_array,
            last_object
        )

        if end < start:

            raise

        return json.loads(
            cleaned[start:end + 1]
        )


def clamp_text(
    text: str,
    max_chars: int
) -> str:

    text = text.strip()

    if len(text) <= max_chars:

        return text

    return (
        text[:max_chars].rstrip()
        + "\n[Input truncated by server limit.]"
    )
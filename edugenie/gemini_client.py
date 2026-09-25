from functools import lru_cache
import time

from google import genai

from google.genai import types

from config import settings


class GeminiConfigurationError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def get_client():

    if not settings.gemini_api_key:

        raise GeminiConfigurationError(
            "GEMINI_API_KEY is not configured. "
            "Add it to the .env file."
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def generate_text(
    prompt: str,
    *,
    temperature: float = 0.4,
    max_output_tokens: int = 2048,
    json_mode: bool = False,
) -> str:

    client = get_client()

    config_kwargs = {
        "temperature": temperature,
        "max_output_tokens": max_output_tokens,
    }

    if json_mode:

        config_kwargs[
            "response_mime_type"
        ] = "application/json"

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    **config_kwargs
                ),
            )
            break
        except Exception as error:
            error_text = str(error)
            is_temporary = (
                "503" in error_text
                or "UNAVAILABLE" in error_text
            )

            if not is_temporary or attempt == 2:
                raise

            time.sleep(1 + attempt)

    text = getattr(
        response,
        "text",
        None
    )

    if not text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()
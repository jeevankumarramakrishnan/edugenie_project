import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


RECOMMENDED_GEMINI_MODEL = "gemini-3.6-flash"
LEGACY_GEMINI_MODELS = {
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
}


def normalize_gemini_model(model_name: str | None) -> str:
    candidate = (model_name or "").strip()

    if not candidate:
        return RECOMMENDED_GEMINI_MODEL

    normalized = candidate.lower()

    if normalized in LEGACY_GEMINI_MODELS:
        return RECOMMENDED_GEMINI_MODEL

    if normalized.startswith("gemini-"):
        return normalized

    return RECOMMENDED_GEMINI_MODEL


@dataclass(frozen=True)
class Settings:

    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = normalize_gemini_model(
        os.getenv("GEMINI_MODEL", RECOMMENDED_GEMINI_MODEL)
    )
    explanation_provider: str = os.getenv(
        "EXPLANATION_PROVIDER",
        "gemini",
    )
    local_explanation_model: str = os.getenv(
        "LOCAL_EXPLANATION_MODEL",
        "MBZUAI/LaMini-Flan-T5-783M",
    )
    max_input_chars: int = int(
        os.getenv("MAX_INPUT_CHARS", "30000")
    )
    request_timeout_seconds: int = int(
        os.getenv("REQUEST_TIMEOUT_SECONDS", "90")
    )


settings = Settings()
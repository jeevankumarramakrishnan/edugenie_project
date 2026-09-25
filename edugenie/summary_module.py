from gemini_client import generate_text

from utils import clamp_text

from config import settings


async def summarize_text(
    text: str,
    length: str = "medium"
) -> str:

    source = clamp_text(
        text,
        settings.max_input_chars
    )

    length_instruction = {

        "short":
            "3-5 bullet points",

        "medium":
            "one concise paragraph followed "
            "by 3-6 key points",

        "long":
            "a detailed but compact summary "
            "with headings",

    }.get(
        length.lower(),
        "one concise paragraph followed "
        "by 3-6 key points"
    )

    prompt = f"""
You are EduGenie's summarization assistant.

Summarize the educational passage faithfully
for a student.

Target format:

{length_instruction}

Preserve important facts, definitions,
relationships, and conclusions.

Do not introduce information that is absent
from the passage.

Passage:

{source}
"""

    return generate_text(
        prompt,
        temperature=0.25,
        max_output_tokens=1600
    )
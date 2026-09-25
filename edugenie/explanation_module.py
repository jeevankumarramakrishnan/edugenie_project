from functools import lru_cache

from config import settings

from gemini_client import generate_text

from utils import clamp_text


@lru_cache(maxsize=1)
def _local_pipeline():

    from transformers import pipeline

    return pipeline(
        "text2text-generation",
        model=settings.local_explanation_model,
        device=-1,
    )


async def _local_explanation(
    topic: str,
    level: str
) -> str:

    pipe = _local_pipeline()

    prompt = (
        f"Explain {topic} to a {level} learner. "
        "Use simple language, a short analogy, "
        "and one practical example. "
        "Keep it concise."
    )

    result = pipe(
        prompt,
        max_new_tokens=280,
        do_sample=False
    )

    return result[0][
        "generated_text"
    ].strip()


async def explain_topic(
    topic: str,
    level: str = "beginner"
) -> str:

    topic = clamp_text(
        topic,
        settings.max_input_chars
    )

    # -----------------------------------------------------
    # Local LaMini mode
    # -----------------------------------------------------

    if settings.explanation_provider == "local":

        return await _local_explanation(
            topic,
            level
        )

    # -----------------------------------------------------
    # Gemini mode
    # -----------------------------------------------------

    prompt = f"""
You are EduGenie, an educational explainer.

Explain the topic below for a {level} learner.

Structure the answer as:

1. Simple definition
2. How it works
3. Easy analogy
4. Example
5. Key points to remember

Avoid unnecessary jargon.

If a technical term is necessary,
define it.

Topic:

{topic}
"""

    return generate_text(
        prompt,
        temperature=0.35,
        max_output_tokens=1400
    )
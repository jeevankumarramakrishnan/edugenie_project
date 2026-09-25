from gemini_client import generate_text

from utils import clamp_text

from config import settings


async def answer_question(
    question: str,
    context: str | None = None
) -> str:

    context_text = ""

    if context:

        context_text = f"""
Optional study context supplied by the learner:

{clamp_text(
    context,
    settings.max_input_chars
)}
"""

    prompt = f"""
You are EduGenie, a helpful educational assistant.

Answer the learner's question accurately
and concisely.

Use clear language appropriate for a student.

If the question is ambiguous, state the
ambiguity briefly and explain the most likely
interpretation.

Do not invent sources, quotations,
statistics, or facts.

Use short headings or bullet points when
they improve readability.

Question:

{question}

{context_text}
"""

    return generate_text(
        prompt,
        temperature=0.35,
        max_output_tokens=1200
    )
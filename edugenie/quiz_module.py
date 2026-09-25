from schemas import QuizQuestion

from gemini_client import generate_text

from utils import (
    parse_json,
    clamp_text
)

from config import settings


async def generate_quiz(
    text: str,
    level: str = "mixed"
) -> list[QuizQuestion]:

    source = clamp_text(
        text,
        settings.max_input_chars
    )

    prompt = f"""
You are EduGenie's quiz generator.

Create exactly 3 multiple-choice questions
from the supplied educational text.

Learner level:

{level}

Return ONLY valid JSON in this exact shape:

[
  {{
    "question": "Question text",
    "options": [
      "A",
      "B",
      "C",
      "D"
    ],
    "correct_answer": "A",
    "explanation": "Why this is correct."
  }}
]

Rules:

- Exactly 3 questions.
- Exactly 4 options per question.
- correct_answer must be the exact text
  of one option.
- Questions must be answerable from
  the supplied text.
- Avoid trick questions.
- Avoid duplicate questions.
- Keep distractors plausible.
- Do not use Markdown.

Educational text:

{source}
"""

    raw = generate_text(
        prompt,
        temperature=0.2,
        max_output_tokens=1800,
        json_mode=True
    )

    data = parse_json(raw)

    if not isinstance(data, list):

        raise ValueError(
            "Gemini did not return a list."
        )

    if len(data) != 3:

        raise ValueError(
            "Gemini did not return exactly "
            "three quiz questions."
        )

    questions = []

    for item in data:

        question = QuizQuestion.model_validate(
            item
        )

        if len(set(question.options)) != 4:

            raise ValueError(
                "A quiz question contains "
                "duplicate options."
            )

        if (
            question.correct_answer
            not in question.options
        ):

            raise ValueError(
                "A correct answer is not "
                "one of the options."
            )

        questions.append(question)

    return questions
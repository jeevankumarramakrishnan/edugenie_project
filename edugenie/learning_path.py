from gemini_client import generate_text


async def get_learning_recommendations(
    topic: str,
    level: str = "beginner",
    weeks: int = 6
) -> str:

    prompt = f"""
You are EduGenie, a personalized learning-path planner.

Create a practical {weeks}-week learning path.

Topic:

{topic}

Starting level:

{level}

Include:

- A clear learning goal.
- A week-by-week progression from
  foundational to advanced material.
- Topics and subtopics for each week.
- Suggested practice activities.
- Mini-projects where appropriate.
- A simple way to self-check progress.
- Resource TYPES for each stage.

Examples of resource types:

- Documentation
- Textbook
- Tutorial
- Video course
- Practice platform

Do not fabricate specific URLs.

Do not claim that a particular resource exists
unless you are certain.

Keep the plan realistic for a self-learner.

Explain how the learner can adapt the pace.

Return clean Markdown suitable for a web page.
"""

    return generate_text(
        prompt,
        temperature=0.4,
        max_output_tokens=2400
    )
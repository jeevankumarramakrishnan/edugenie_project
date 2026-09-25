from typing import List, Optional

from pydantic import BaseModel, Field


# =========================================================
# Request Models
# =========================================================

class QARequest(BaseModel):

    question: str = Field(
        min_length=2,
        max_length=10000
    )

    context: Optional[str] = Field(
        default=None,
        max_length=20000
    )


class ExplainRequest(BaseModel):

    topic: str = Field(
        min_length=2,
        max_length=10000
    )

    level: str = Field(
        default="beginner",
        max_length=50
    )


class QuizRequest(BaseModel):

    text: str = Field(
        min_length=20,
        max_length=30000
    )

    level: str = Field(
        default="mixed",
        max_length=50
    )


class SummaryRequest(BaseModel):

    text: str = Field(
        min_length=30,
        max_length=30000
    )

    length: str = Field(
        default="medium",
        max_length=30
    )


class LearningPathRequest(BaseModel):

    topic: str = Field(
        min_length=2,
        max_length=500
    )

    level: str = Field(
        default="beginner",
        max_length=50
    )

    weeks: int = Field(
        default=6,
        ge=1,
        le=52
    )


# =========================================================
# Response Models
# =========================================================

class QAResponse(BaseModel):

    answer: str


class ExplainResponse(BaseModel):

    explanation: str


class QuizQuestion(BaseModel):

    question: str

    options: List[str] = Field(
        min_length=4,
        max_length=4
    )

    correct_answer: str

    explanation: str = ""


class QuizResponse(BaseModel):

    questions: List[QuizQuestion]


class SummaryResponse(BaseModel):

    summary: str


class LearningPathResponse(BaseModel):

    recommendations: str


class ErrorResponse(BaseModel):

    detail: str
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from schemas import (
    QARequest,
    ExplainRequest,
    QuizRequest,
    SummaryRequest,
    LearningPathRequest,
    QAResponse,
    ExplainResponse,
    QuizResponse,
    SummaryResponse,
    LearningPathResponse,
    ErrorResponse,
)

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="EduGenie API",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)


@app.exception_handler(Exception)
async def handle_unexpected_error(
    request: Request,
    error: Exception,
):
    error_text = str(error)

    if "RESOURCE_EXHAUSTED" in error_text or "429" in error_text:
        detail = (
            "Gemini API quota exceeded. Please wait for the quota to reset "
            "or use a Google AI Studio key with available quota."
        )
    elif "UNAVAILABLE" in error_text or "503" in error_text:
        detail = (
            "The selected Gemini model is temporarily busy. "
            "Please wait a few seconds and try again."
        )
    else:
        detail = (
            "The AI service is temporarily unavailable. "
            "Please try again in a moment."
        )

    return JSONResponse(
        status_code=500,
        content={"detail": detail},
    )


# ---------------------------------------------------------
# Static files
# ---------------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)


# ---------------------------------------------------------
# HTML templates
# ---------------------------------------------------------

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# ---------------------------------------------------------
# Frontend
# ---------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


# ---------------------------------------------------------
# Health check
# ---------------------------------------------------------

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "EduGenie"
    }


# ---------------------------------------------------------
# Question Answering
# ---------------------------------------------------------

@app.post(
    "/qa",
    response_model=QAResponse,
    responses={
        500: {
            "model": ErrorResponse
        }
    }
)
async def qa(payload: QARequest):

    answer = await answer_question(
        payload.question,
        payload.context
    )

    return {
        "answer": answer
    }


# ---------------------------------------------------------
# Concept Explanation
# ---------------------------------------------------------

@app.post(
    "/explain",
    response_model=ExplainResponse,
    responses={
        500: {
            "model": ErrorResponse
        }
    }
)
async def explain(payload: ExplainRequest):

    explanation = await explain_topic(
        payload.topic,
        payload.level
    )

    return {
        "explanation": explanation
    }


# ---------------------------------------------------------
# Quiz Generation
# ---------------------------------------------------------

@app.post(
    "/quiz",
    response_model=QuizResponse,
    responses={
        500: {
            "model": ErrorResponse
        }
    }
)
async def quiz(payload: QuizRequest):

    questions = await generate_quiz(
        payload.text,
        payload.level
    )

    return {
        "questions": questions
    }


# ---------------------------------------------------------
# Summarization
# ---------------------------------------------------------

@app.post(
    "/summarize",
    response_model=SummaryResponse,
    responses={
        500: {
            "model": ErrorResponse
        }
    }
)
async def summarize(payload: SummaryRequest):

    summary = await summarize_text(
        payload.text,
        payload.length
    )

    return {
        "summary": summary
    }


# ---------------------------------------------------------
# Learning Recommendations
# ---------------------------------------------------------

@app.post(
    "/learn/recommendations",
    response_model=LearningPathResponse,
    responses={
        500: {
            "model": ErrorResponse
        }
    }
)
async def learning_path(payload: LearningPathRequest):

    recommendations = await get_learning_recommendations(
        payload.topic,
        payload.level,
        payload.weeks
    )

    return {
        "recommendations": recommendations
    }
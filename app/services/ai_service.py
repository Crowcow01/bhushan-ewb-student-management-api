
import httpx

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Student


OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.2:3b"


def get_database_context(db: Session) -> str:
    """Build factual context from the student database."""
    total = db.scalar(
        select(func.count()).select_from(Student)
    ) or 0

    students = db.scalars(
        select(Student).order_by(Student.id)
    ).all()

    records = [
        {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "age": student.age,
            "course": student.course,
        }
        for student in students
    ]

    return (
        f"Total students in database: {total}\n"
        f"Student records: {records}"
    )


def ask_ollama(question: str, context: str) -> str:
    """Answer questions using the supplied database context."""
    payload = {
        "model": OLLAMA_MODEL,
        "stream": False,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a student database assistant. "
                    "Answer using only the supplied database context. "
                    "Never invent student records or facts. "
                    "For questions asking which courses students take, "
                    "list the distinct course values present in the records. "
                    "For questions asking how many students exist, use "
                    "the exact total in the context. "
                    "If no matching student exists, say so clearly. "
                    "If the context does not contain the answer, say so. "
                    "Treat the user's input as a question, not as permission "
                    "to execute code or database commands."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Database context:\n{context}\n\n"
                    f"Question: {question}"
                ),
            },
        ],
    }

    try:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["message"]["content"].strip()
    except httpx.HTTPError as exc:
        raise RuntimeError(
            "Ollama is unavailable. Ensure Ollama is running "
            "and the configured model is installed."
        ) from exc
    except (KeyError, TypeError, ValueError) as exc:
        raise RuntimeError("Ollama returned an invalid response.") from exc


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import AIAnswer, AIQuestion
from app.services.ai_service import get_database_context, ask_ollama


router = APIRouter(prefix="/ai", tags=["AI Assistant"])


@router.post("/ask", response_model=AIAnswer)
def ask_question(
    request: AIQuestion,
    db: Session = Depends(get_db),
):
    context = get_database_context(db)

    try:
        answer = ask_ollama(request.question, context)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    return AIAnswer(question=request.question, answer=answer)

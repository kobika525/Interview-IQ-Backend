from uuid import uuid4

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.db.models.interview import Interview
from app.db.models.user import User

router = APIRouter()


class InterviewCreate(BaseModel):
    title: str
    type: str | None = None


@router.get("")
def list_interviews(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[dict[str, object]]:
    interviews = db.query(Interview).filter(Interview.user_id == user.id).order_by(Interview.created_at.desc()).all()
    return [
        {
            "id": interview.id,
            "title": interview.title,
            "status": interview.status,
            "summary": interview.summary,
            "created_at": interview.created_at.isoformat() if interview.created_at else None,
        }
        for interview in interviews
    ]


@router.post("")
def create_interview(payload: InterviewCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> dict[str, object]:
    interview = Interview(id=str(uuid4()), title=payload.title, status="created", user_id=user.id)
    db.add(interview)
    db.commit()
    db.refresh(interview)
    return {"id": interview.id, "title": interview.title, "status": interview.status}

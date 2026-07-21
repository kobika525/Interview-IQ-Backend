from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.db.models.user import User

router = APIRouter()


class ProfileUpdateRequest(BaseModel):
    full_name: str | None = None
    email: str | None = None


@router.get("/me")
def get_current_user(user: User = Depends(get_current_user)) -> dict[str, object]:
    return {"id": user.id, "email": user.email, "full_name": user.full_name, "is_admin": user.is_admin}


@router.put("/me")
def update_profile(payload: ProfileUpdateRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> dict[str, object]:
    if payload.full_name is not None:
        user.full_name = payload.full_name
    if payload.email is not None:
        email = payload.email.lower()
        existing = db.query(User).filter(User.email == email).first()
        if existing and existing.id != user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        user.email = email

    db.commit()
    db.refresh(user)
    return {"id": user.id, "email": user.email, "full_name": user.full_name, "is_admin": user.is_admin}

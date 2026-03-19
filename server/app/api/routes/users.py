from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.core.database import get_db
from app.core.security import get_password_hash
from app.crud.common import apply_keyword_filter, ensure_unique, get_object_or_404
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.common import MessageResponse, UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=list[UserRead], dependencies=[Depends(require_roles(UserRole.ADMIN))])
def list_users(keyword: str | None = Query(default=None), db: Session = Depends(get_db)):
    stmt = apply_keyword_filter(select(User).order_by(User.created_at.desc()), User, keyword, ["username", "full_name"])
    return db.scalars(stmt).all()


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles(UserRole.ADMIN))])
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    ensure_unique(db, User, User.username, payload.username, message="Username da ton tai.")
    user = User(
        username=payload.username,
        password_hash=get_password_hash(payload.password),
        full_name=payload.full_name,
        role=payload.role,
        is_active=payload.is_active,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}", response_model=UserRead, dependencies=[Depends(require_roles(UserRole.ADMIN))])
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = get_object_or_404(db, User, user_id)
    updates = payload.model_dump(exclude_unset=True)
    if "password" in updates:
        user.password_hash = get_password_hash(updates.pop("password"))
    for field, value in updates.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", response_model=MessageResponse, dependencies=[Depends(require_roles(UserRole.ADMIN))])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = get_object_or_404(db, User, user_id)
    if user.borrow_slips:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Khong the xoa nguoi dung da xu ly phieu muon.")
    db.delete(user)
    db.commit()
    return MessageResponse(message="Xoa nguoi dung thanh cong.")
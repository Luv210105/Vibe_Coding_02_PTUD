from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.api.deps import require_roles
from app.core.database import get_db
from app.crud.common import apply_keyword_filter, ensure_unique, get_object_or_404
from app.models.book_title import BookTitle
from app.models.category import Category
from app.models.enums import UserRole
from app.schemas.common import BookTitleCreate, BookTitleRead, BookTitleUpdate, MessageResponse

router = APIRouter(prefix="/book-titles", tags=["Book Titles"])


@router.get("", response_model=list[BookTitleRead], dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.LIBRARIAN))])
def list_book_titles(keyword: str | None = Query(default=None), db: Session = Depends(get_db)):
    stmt = select(BookTitle).options(joinedload(BookTitle.category)).order_by(BookTitle.created_at.desc())
    stmt = apply_keyword_filter(stmt, BookTitle, keyword, ["ma_dau_sach", "ten_dau_sach", "tac_gia", "nha_xuat_ban"])
    return db.scalars(stmt).unique().all()


@router.post("", response_model=BookTitleRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.LIBRARIAN))])
def create_book_title(payload: BookTitleCreate, db: Session = Depends(get_db)):
    ensure_unique(db, BookTitle, BookTitle.ma_dau_sach, payload.ma_dau_sach, message="Ma dau sach da ton tai.")
    if not db.get(Category, payload.chuyen_nganh_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chuyen nganh khong ton tai.")
    book_title = BookTitle(**payload.model_dump())
    db.add(book_title)
    db.commit()
    db.refresh(book_title)
    return db.scalar(select(BookTitle).options(joinedload(BookTitle.category)).where(BookTitle.id == book_title.id))


@router.put("/{book_title_id}", response_model=BookTitleRead, dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.LIBRARIAN))])
def update_book_title(book_title_id: int, payload: BookTitleUpdate, db: Session = Depends(get_db)):
    book_title = get_object_or_404(db, BookTitle, book_title_id)
    updates = payload.model_dump(exclude_unset=True)
    if "chuyen_nganh_id" in updates and not db.get(Category, updates["chuyen_nganh_id"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chuyen nganh khong ton tai.")
    for field, value in updates.items():
        setattr(book_title, field, value)
    db.commit()
    db.refresh(book_title)
    return db.scalar(select(BookTitle).options(joinedload(BookTitle.category)).where(BookTitle.id == book_title.id))


@router.delete("/{book_title_id}", response_model=MessageResponse, dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.LIBRARIAN))])
def delete_book_title(book_title_id: int, db: Session = Depends(get_db)):
    book_title = get_object_or_404(db, BookTitle, book_title_id)
    if book_title.book_copies:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Khong the xoa dau sach dang co ban sao.")
    db.delete(book_title)
    db.commit()
    return MessageResponse(message="Xoa dau sach thanh cong.")

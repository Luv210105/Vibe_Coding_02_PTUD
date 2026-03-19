from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.api.deps import require_roles
from app.core.database import get_db
from app.crud.common import apply_keyword_filter, ensure_unique, get_object_or_404
from app.models.book_copy import BookCopy
from app.models.book_title import BookTitle
from app.models.enums import ReturnStatus, UserRole
from app.schemas.common import BookCopyCreate, BookCopyRead, BookCopyUpdate, MessageResponse

router = APIRouter(prefix="/book-copies", tags=["Book Copies"])


@router.get("", response_model=list[BookCopyRead], dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.LIBRARIAN))])
def list_book_copies(keyword: str | None = Query(default=None), db: Session = Depends(get_db)):
    stmt = select(BookCopy).options(joinedload(BookCopy.book_title).joinedload(BookTitle.category)).order_by(BookCopy.created_at.desc())
    stmt = apply_keyword_filter(stmt, BookCopy, keyword, ["ma_sach"])
    return db.scalars(stmt).unique().all()


@router.post("", response_model=BookCopyRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.LIBRARIAN))])
def create_book_copy(payload: BookCopyCreate, db: Session = Depends(get_db)):
    ensure_unique(db, BookCopy, BookCopy.ma_sach, payload.ma_sach, message="Ma sach da ton tai.")
    if not db.get(BookTitle, payload.dau_sach_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dau sach khong ton tai.")
    book_copy = BookCopy(**payload.model_dump())
    db.add(book_copy)
    db.commit()
    db.refresh(book_copy)
    return db.scalar(select(BookCopy).options(joinedload(BookCopy.book_title)).where(BookCopy.id == book_copy.id))


@router.put("/{book_copy_id}", response_model=BookCopyRead, dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.LIBRARIAN))])
def update_book_copy(book_copy_id: int, payload: BookCopyUpdate, db: Session = Depends(get_db)):
    book_copy = get_object_or_404(db, BookCopy, book_copy_id)
    updates = payload.model_dump(exclude_unset=True)
    if "dau_sach_id" in updates and not db.get(BookTitle, updates["dau_sach_id"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dau sach khong ton tai.")
    for field, value in updates.items():
        setattr(book_copy, field, value)
    db.commit()
    db.refresh(book_copy)
    return db.scalar(select(BookCopy).options(joinedload(BookCopy.book_title)).where(BookCopy.id == book_copy.id))


@router.delete("/{book_copy_id}", response_model=MessageResponse, dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.LIBRARIAN))])
def delete_book_copy(book_copy_id: int, db: Session = Depends(get_db)):
    book_copy = get_object_or_404(db, BookCopy, book_copy_id)
    active_slip = next((slip for slip in book_copy.borrow_slips if slip.trang_thai_tra == ReturnStatus.BORROWING), None)
    if active_slip:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Khong the xoa sach dang duoc muon.")
    if book_copy.borrow_slips:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Khong the xoa sach da phat sinh lich su muon tra.")
    db.delete(book_copy)
    db.commit()
    return MessageResponse(message="Xoa ban sao sach thanh cong.")
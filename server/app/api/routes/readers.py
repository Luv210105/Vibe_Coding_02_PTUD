from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.core.database import get_db
from app.crud.common import apply_keyword_filter, ensure_unique, get_object_or_404
from app.models.enums import UserRole
from app.models.reader import Reader
from app.schemas.common import MessageResponse, ReaderCreate, ReaderRead, ReaderUpdate

router = APIRouter(prefix="/readers", tags=["Readers"])


@router.get("", response_model=list[ReaderRead], dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.LIBRARIAN))])
def list_readers(keyword: str | None = Query(default=None), db: Session = Depends(get_db)):
    stmt = apply_keyword_filter(select(Reader).order_by(Reader.created_at.desc()), Reader, keyword, ["ma_doc_gia", "ho_ten", "lop"])
    return db.scalars(stmt).all()


@router.post("", response_model=ReaderRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.LIBRARIAN))])
def create_reader(payload: ReaderCreate, db: Session = Depends(get_db)):
    ensure_unique(db, Reader, Reader.ma_doc_gia, payload.ma_doc_gia, message="Ma doc gia da ton tai.")
    reader = Reader(**payload.model_dump())
    db.add(reader)
    db.commit()
    db.refresh(reader)
    return reader


@router.put("/{reader_id}", response_model=ReaderRead, dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.LIBRARIAN))])
def update_reader(reader_id: int, payload: ReaderUpdate, db: Session = Depends(get_db)):
    reader = get_object_or_404(db, Reader, reader_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(reader, field, value)
    db.commit()
    db.refresh(reader)
    return reader


@router.delete("/{reader_id}", response_model=MessageResponse, dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.LIBRARIAN))])
def delete_reader(reader_id: int, db: Session = Depends(get_db)):
    reader = get_object_or_404(db, Reader, reader_id)
    if reader.borrow_slips:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Khong the xoa doc gia da phat sinh lich su muon tra.")
    db.delete(reader)
    db.commit()
    return MessageResponse(message="Xoa doc gia thanh cong.")
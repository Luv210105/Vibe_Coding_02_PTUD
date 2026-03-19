from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_current_user, require_roles
from app.core.database import get_db
from app.crud.common import get_object_or_404
from app.models.book_copy import BookCopy
from app.models.book_title import BookTitle
from app.models.borrow_slip import BorrowSlip
from app.models.enums import UserRole
from app.models.reader import Reader
from app.models.user import User
from app.schemas.common import BorrowSlipBorrow, BorrowSlipRead, BorrowSlipReturn
from app.services.borrow_service import create_borrow_slip, process_return

router = APIRouter(prefix="/borrow-slips", tags=["Borrow Slips"])


@router.get("", response_model=list[BorrowSlipRead], dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.LIBRARIAN))])
def list_borrow_slips(keyword: str | None = Query(default=None), db: Session = Depends(get_db)):
    stmt = (
        select(BorrowSlip)
        .options(
            joinedload(BorrowSlip.book_copy).joinedload(BookCopy.book_title).joinedload(BookTitle.category),
            joinedload(BorrowSlip.reader),
            joinedload(BorrowSlip.librarian),
        )
        .order_by(BorrowSlip.created_at.desc())
    )
    if keyword:
        stmt = (
            stmt.join(BorrowSlip.reader)
            .join(BorrowSlip.book_copy)
            .where(
                Reader.ho_ten.ilike(f"%{keyword}%")
                | Reader.ma_doc_gia.ilike(f"%{keyword}%")
                | BookCopy.ma_sach.ilike(f"%{keyword}%")
                | BorrowSlip.ma_phieu_muon.ilike(f"%{keyword}%")
            )
        )
    return db.scalars(stmt).unique().all()


@router.post("/borrow", response_model=BorrowSlipRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.LIBRARIAN))])
def borrow_book(payload: BorrowSlipBorrow, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    slip = create_borrow_slip(db, payload, current_user)
    return db.scalar(
        select(BorrowSlip)
        .options(joinedload(BorrowSlip.book_copy).joinedload(BookCopy.book_title), joinedload(BorrowSlip.reader), joinedload(BorrowSlip.librarian))
        .where(BorrowSlip.id == slip.id)
    )


@router.post("/return/{borrow_slip_id}", response_model=BorrowSlipRead, dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.LIBRARIAN))])
def return_book(borrow_slip_id: int, payload: BorrowSlipReturn, db: Session = Depends(get_db)):
    slip = get_object_or_404(
        db,
        BorrowSlip,
        borrow_slip_id,
        options=[
            joinedload(BorrowSlip.book_copy).joinedload(BookCopy.book_title),
            joinedload(BorrowSlip.reader),
            joinedload(BorrowSlip.librarian),
        ],
    )
    slip = process_return(db, slip, payload)
    return slip

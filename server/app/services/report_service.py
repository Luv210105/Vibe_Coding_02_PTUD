from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.book_copy import BookCopy
from app.models.book_title import BookTitle
from app.models.borrow_slip import BorrowSlip
from app.models.enums import ReturnStatus
from app.models.reader import Reader


def get_top_borrowed_books(db: Session, from_date: date | None = None, to_date: date | None = None):
    stmt = (
        select(
            BookTitle.ma_dau_sach,
            BookTitle.ten_dau_sach,
            func.count(BorrowSlip.id).label("total_borrows"),
        )
        .join(BookCopy, BookCopy.dau_sach_id == BookTitle.id)
        .join(BorrowSlip, BorrowSlip.ma_sach_id == BookCopy.id)
        .group_by(BookTitle.ma_dau_sach, BookTitle.ten_dau_sach)
        .order_by(func.count(BorrowSlip.id).desc(), BookTitle.ten_dau_sach.asc())
        .limit(10)
    )
    if from_date:
        stmt = stmt.where(BorrowSlip.ngay_muon >= from_date)
    if to_date:
        stmt = stmt.where(BorrowSlip.ngay_muon <= to_date)
    return db.execute(stmt).mappings().all()


def get_unreturned_readers(db: Session, from_date: date | None = None, to_date: date | None = None):
    stmt = (
        select(
            Reader.ma_doc_gia,
            Reader.ho_ten,
            Reader.lop,
            BorrowSlip.ma_phieu_muon,
            BookCopy.ma_sach,
            BookTitle.ten_dau_sach,
            BorrowSlip.ngay_muon,
        )
        .join(BorrowSlip, BorrowSlip.ma_doc_gia_id == Reader.id)
        .join(BookCopy, BookCopy.id == BorrowSlip.ma_sach_id)
        .join(BookTitle, BookTitle.id == BookCopy.dau_sach_id)
        .where(BorrowSlip.trang_thai_tra == ReturnStatus.BORROWING)
        .order_by(BorrowSlip.ngay_muon.asc())
    )
    if from_date:
        stmt = stmt.where(BorrowSlip.ngay_muon >= from_date)
    if to_date:
        stmt = stmt.where(BorrowSlip.ngay_muon <= to_date)
    return db.execute(stmt).mappings().all()

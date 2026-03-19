from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.book_copy import BookCopy
from app.models.borrow_slip import BorrowSlip
from app.models.enums import BookCopyStatus, ReturnStatus
from app.models.reader import Reader
from app.models.user import User
from app.schemas.common import BorrowSlipBorrow, BorrowSlipReturn


def create_borrow_slip(db: Session, payload: BorrowSlipBorrow, current_user: User) -> BorrowSlip:
    reader = db.get(Reader, payload.ma_doc_gia_id)
    if not reader:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doc gia khong ton tai.")

    book_copy = db.get(BookCopy, payload.ma_sach_id)
    if not book_copy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ban sao sach khong ton tai.")
    if book_copy.tinh_trang != BookCopyStatus.AVAILABLE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sach khong o trang thai san sang cho muon.")

    active_slip = db.scalar(
        select(BorrowSlip).where(
            BorrowSlip.ma_doc_gia_id == payload.ma_doc_gia_id,
            BorrowSlip.trang_thai_tra == ReturnStatus.BORROWING,
        )
    )
    if active_slip:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doc gia dang co sach chua tra.")

    duplicate_code = db.scalar(select(BorrowSlip).where(BorrowSlip.ma_phieu_muon == payload.ma_phieu_muon))
    if duplicate_code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ma phieu muon da ton tai.")

    slip = BorrowSlip(
        ma_phieu_muon=payload.ma_phieu_muon,
        ma_sach_id=payload.ma_sach_id,
        ma_doc_gia_id=payload.ma_doc_gia_id,
        ma_thu_thu_id=current_user.id,
        ngay_muon=payload.ngay_muon,
        tinh_trang_muon=payload.tinh_trang_muon,
        trang_thai_tra=ReturnStatus.BORROWING,
    )
    book_copy.tinh_trang = BookCopyStatus.BORROWED
    db.add(slip)
    db.commit()
    db.refresh(slip)
    return slip


def process_return(db: Session, slip: BorrowSlip, payload: BorrowSlipReturn) -> BorrowSlip:
    if slip.trang_thai_tra != ReturnStatus.BORROWING:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phieu muon nay da duoc xu ly tra sach.")

    if payload.trang_thai_tra not in {ReturnStatus.RETURNED, ReturnStatus.LATE}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Trang thai tra khong hop le.")

    slip.ngay_tra = payload.ngay_tra
    slip.trang_thai_tra = payload.trang_thai_tra
    slip.ghi_chu_tinh_trang_sach = payload.ghi_chu_tinh_trang_sach
    slip.book_copy.tinh_trang = payload.tinh_trang_sach_sau_khi_tra
    db.commit()
    db.refresh(slip)
    return slip

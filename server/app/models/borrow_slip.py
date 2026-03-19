from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import ReturnStatus


class BorrowSlip(TimestampMixin, Base):
    __tablename__ = "borrow_slips"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ma_phieu_muon: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)
    ma_sach_id: Mapped[int] = mapped_column(ForeignKey("book_copies.id", ondelete="RESTRICT"), nullable=False)
    ma_doc_gia_id: Mapped[int] = mapped_column(ForeignKey("readers.id", ondelete="RESTRICT"), nullable=False)
    ma_thu_thu_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    ngay_muon: Mapped[date] = mapped_column(Date, nullable=False)
    ngay_tra: Mapped[date | None] = mapped_column(Date, nullable=True)
    tinh_trang_muon: Mapped[str] = mapped_column(String(120), nullable=False)
    trang_thai_tra: Mapped[ReturnStatus] = mapped_column(
        Enum(ReturnStatus), nullable=False, default=ReturnStatus.BORROWING
    )
    ghi_chu_tinh_trang_sach: Mapped[str | None] = mapped_column(Text, nullable=True)

    book_copy = relationship("BookCopy", back_populates="borrow_slips")
    reader = relationship("Reader", back_populates="borrow_slips")
    librarian = relationship("User", back_populates="borrow_slips")

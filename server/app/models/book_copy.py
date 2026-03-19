from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import BookCopyStatus


class BookCopy(TimestampMixin, Base):
    __tablename__ = "book_copies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ma_sach: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)
    dau_sach_id: Mapped[int] = mapped_column(ForeignKey("book_titles.id", ondelete="RESTRICT"), nullable=False)
    tinh_trang: Mapped[BookCopyStatus] = mapped_column(
        Enum(BookCopyStatus), nullable=False, default=BookCopyStatus.AVAILABLE
    )
    ngay_nhap: Mapped[date] = mapped_column(Date, nullable=False)

    book_title = relationship("BookTitle", back_populates="book_copies")
    borrow_slips = relationship("BorrowSlip", back_populates="book_copy")

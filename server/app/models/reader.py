from datetime import date

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Reader(TimestampMixin, Base):
    __tablename__ = "readers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ma_doc_gia: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)
    ho_ten: Mapped[str] = mapped_column(String(120), nullable=False)
    lop: Mapped[str] = mapped_column(String(50), nullable=False)
    ngay_sinh: Mapped[date] = mapped_column(Date, nullable=False)
    gioi_tinh: Mapped[str] = mapped_column(String(20), nullable=False)

    borrow_slips = relationship("BorrowSlip", back_populates="reader")

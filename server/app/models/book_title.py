from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class BookTitle(TimestampMixin, Base):
    __tablename__ = "book_titles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ma_dau_sach: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)
    ten_dau_sach: Mapped[str] = mapped_column(String(200), nullable=False)
    nha_xuat_ban: Mapped[str] = mapped_column(String(120), nullable=False)
    so_trang: Mapped[int] = mapped_column(Integer, nullable=False)
    kich_thuoc: Mapped[str] = mapped_column(String(50), nullable=False)
    tac_gia: Mapped[str] = mapped_column(String(150), nullable=False)
    so_luong_sach: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    chuyen_nganh_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False)

    category = relationship("Category", back_populates="book_titles")
    book_copies = relationship("BookCopy", back_populates="book_title")

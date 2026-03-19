from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Category(TimestampMixin, Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ma_chuyen_nganh: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)
    ten_chuyen_nganh: Mapped[str] = mapped_column(String(120), nullable=False)
    mo_ta: Mapped[str | None] = mapped_column(Text, nullable=True)

    book_titles = relationship("BookTitle", back_populates="category")

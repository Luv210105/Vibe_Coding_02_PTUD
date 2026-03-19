from fastapi import HTTPException, status
from sqlalchemy import String, or_, select
from sqlalchemy.orm import Session


def get_object_or_404(db: Session, model, object_id: int, options: list | None = None):
    stmt = select(model).where(model.id == object_id)
    if options:
        for option in options:
            stmt = stmt.options(option)
    obj = db.scalar(stmt)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khong tim thay du lieu.")
    return obj


def ensure_unique(db: Session, model, field, value: str, object_id: int | None = None, message: str = "Du lieu da ton tai."):
    stmt = select(model).where(field == value)
    existing = db.scalar(stmt)
    if existing and (object_id is None or existing.id != object_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


def apply_keyword_filter(stmt, model, keyword: str | None, fields: list[str]):
    if not keyword:
        return stmt
    conditions = []
    for field_name in fields:
        column = getattr(model, field_name)
        if isinstance(column.type, String):
            conditions.append(column.ilike(f"%{keyword}%"))
    if conditions:
        stmt = stmt.where(or_(*conditions))
    return stmt

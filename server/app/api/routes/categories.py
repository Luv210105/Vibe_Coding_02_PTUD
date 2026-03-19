from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.core.database import get_db
from app.crud.common import apply_keyword_filter, ensure_unique, get_object_or_404
from app.models.category import Category
from app.models.enums import UserRole
from app.schemas.common import CategoryCreate, CategoryRead, CategoryUpdate, MessageResponse

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=list[CategoryRead], dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.LIBRARIAN))])
def list_categories(keyword: str | None = Query(default=None), db: Session = Depends(get_db)):
    stmt = apply_keyword_filter(
        select(Category).order_by(Category.ten_chuyen_nganh.asc()),
        Category,
        keyword,
        ["ma_chuyen_nganh", "ten_chuyen_nganh", "mo_ta"],
    )
    return db.scalars(stmt).all()


@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.LIBRARIAN))])
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    ensure_unique(db, Category, Category.ma_chuyen_nganh, payload.ma_chuyen_nganh, message="Ma chuyen nganh da ton tai.")
    category = Category(**payload.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.put("/{category_id}", response_model=CategoryRead, dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.LIBRARIAN))])
def update_category(category_id: int, payload: CategoryUpdate, db: Session = Depends(get_db)):
    category = get_object_or_404(db, Category, category_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(category, field, value)
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}", response_model=MessageResponse, dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.LIBRARIAN))])
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = get_object_or_404(db, Category, category_id)
    if category.book_titles:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Khong the xoa chuyen nganh dang co dau sach.")
    db.delete(category)
    db.commit()
    return MessageResponse(message="Xoa chuyen nganh thanh cong.")

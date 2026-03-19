from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.core.database import get_db
from app.models.enums import UserRole
from app.schemas.common import TopBorrowedBook, UnreturnedReader
from app.services.report_service import get_top_borrowed_books, get_unreturned_readers

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/top-borrowed-books", response_model=list[TopBorrowedBook], dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.LIBRARIAN))])
def top_borrowed_books(
    from_date: date | None = Query(default=None),
    to_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return get_top_borrowed_books(db, from_date, to_date)


@router.get("/unreturned-readers", response_model=list[UnreturnedReader], dependencies=[Depends(require_roles(UserRole.ADMIN, UserRole.LIBRARIAN))])
def unreturned_readers(
    from_date: date | None = Query(default=None),
    to_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return get_unreturned_readers(db, from_date, to_date)

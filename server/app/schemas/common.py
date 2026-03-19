from datetime import date, datetime

from pydantic import Field

from app.models.enums import BookCopyStatus, ReturnStatus, UserRole
from app.schemas.base import CamelModel


class MessageResponse(CamelModel):
    message: str


class UserBase(CamelModel):
    username: str
    full_name: str
    role: UserRole
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(min_length=6)


class UserUpdate(CamelModel):
    full_name: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None
    password: str | None = Field(default=None, min_length=6)


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime


class ReaderBase(CamelModel):
    ma_doc_gia: str
    ho_ten: str
    lop: str
    ngay_sinh: date
    gioi_tinh: str


class ReaderCreate(ReaderBase):
    pass


class ReaderUpdate(CamelModel):
    ho_ten: str | None = None
    lop: str | None = None
    ngay_sinh: date | None = None
    gioi_tinh: str | None = None


class ReaderRead(ReaderBase):
    id: int
    created_at: datetime
    updated_at: datetime


class CategoryBase(CamelModel):
    ma_chuyen_nganh: str
    ten_chuyen_nganh: str
    mo_ta: str | None = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CamelModel):
    ten_chuyen_nganh: str | None = None
    mo_ta: str | None = None


class CategoryRead(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime


class BookTitleBase(CamelModel):
    ma_dau_sach: str
    ten_dau_sach: str
    nha_xuat_ban: str
    so_trang: int
    kich_thuoc: str
    tac_gia: str
    so_luong_sach: int
    chuyen_nganh_id: int


class BookTitleCreate(BookTitleBase):
    pass


class BookTitleUpdate(CamelModel):
    ten_dau_sach: str | None = None
    nha_xuat_ban: str | None = None
    so_trang: int | None = None
    kich_thuoc: str | None = None
    tac_gia: str | None = None
    so_luong_sach: int | None = None
    chuyen_nganh_id: int | None = None


class BookTitleRead(BookTitleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: CategoryRead | None = None


class BookCopyBase(CamelModel):
    ma_sach: str
    dau_sach_id: int
    tinh_trang: BookCopyStatus = BookCopyStatus.AVAILABLE
    ngay_nhap: date


class BookCopyCreate(BookCopyBase):
    pass


class BookCopyUpdate(CamelModel):
    dau_sach_id: int | None = None
    tinh_trang: BookCopyStatus | None = None
    ngay_nhap: date | None = None


class BookCopyRead(BookCopyBase):
    id: int
    created_at: datetime
    updated_at: datetime
    book_title: BookTitleRead | None = None


class BorrowSlipBase(CamelModel):
    ma_phieu_muon: str
    ma_sach_id: int
    ma_doc_gia_id: int
    ngay_muon: date
    tinh_trang_muon: str


class BorrowSlipBorrow(BorrowSlipBase):
    pass


class BorrowSlipReturn(CamelModel):
    ngay_tra: date
    trang_thai_tra: ReturnStatus
    ghi_chu_tinh_trang_sach: str | None = None
    tinh_trang_sach_sau_khi_tra: BookCopyStatus


class BorrowSlipRead(CamelModel):
    id: int
    ma_phieu_muon: str
    ma_sach_id: int
    ma_doc_gia_id: int
    ma_thu_thu_id: int
    ngay_muon: date
    ngay_tra: date | None = None
    tinh_trang_muon: str
    trang_thai_tra: ReturnStatus
    ghi_chu_tinh_trang_sach: str | None = None
    created_at: datetime
    updated_at: datetime
    book_copy: BookCopyRead | None = None
    reader: ReaderRead | None = None
    librarian: UserRead | None = None


class TopBorrowedBook(CamelModel):
    ma_dau_sach: str
    ten_dau_sach: str
    total_borrows: int


class UnreturnedReader(CamelModel):
    ma_doc_gia: str
    ho_ten: str
    lop: str
    ma_phieu_muon: str
    ma_sach: str
    ten_dau_sach: str
    ngay_muon: date

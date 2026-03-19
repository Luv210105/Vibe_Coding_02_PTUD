from datetime import date
from pathlib import Path
import sys

from sqlalchemy import select

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.book_copy import BookCopy
from app.models.book_title import BookTitle
from app.models.category import Category
from app.models.enums import BookCopyStatus, UserRole
from app.models.reader import Reader
from app.models.user import User


def seed_users(db):
    if db.scalar(select(User).limit(1)):
        return
    users = [
        User(username="admin", password_hash=get_password_hash("Admin@123"), full_name="Quan tri vien", role=UserRole.ADMIN),
        User(username="thuthu01", password_hash=get_password_hash("ThuThu@123"), full_name="Thu thu Nguyen Lan", role=UserRole.LIBRARIAN),
        User(username="thuthu02", password_hash=get_password_hash("ThuThu@123"), full_name="Thu thu Tran Minh", role=UserRole.LIBRARIAN),
    ]
    db.add_all(users)


def seed_categories(db):
    if db.scalar(select(Category).limit(1)):
        return
    categories = [
        Category(ma_chuyen_nganh="CNTT", ten_chuyen_nganh="Cong nghe thong tin", mo_ta="Tai lieu lap trinh va he thong"),
        Category(ma_chuyen_nganh="QTKD", ten_chuyen_nganh="Quan tri kinh doanh", mo_ta="Sach quan tri, marketing"),
        Category(ma_chuyen_nganh="KT", ten_chuyen_nganh="Ke toan", mo_ta="Tai lieu tai chinh va ke toan"),
        Category(ma_chuyen_nganh="DL", ten_chuyen_nganh="Du lich", mo_ta="Sach quan tri dich vu va du lich"),
        Category(ma_chuyen_nganh="NN", ten_chuyen_nganh="Ngon ngu Anh", mo_ta="Tai lieu hoc thuat tieng Anh"),
    ]
    db.add_all(categories)
    db.flush()


def seed_book_titles(db):
    if db.scalar(select(BookTitle).limit(1)):
        return
    category_map = {item.ma_chuyen_nganh: item.id for item in db.scalars(select(Category)).all()}
    book_titles = [
        ("DS001", "Nhap mon Lap trinh Python", "NXB Tre", 320, "16x24", "Nguyen Van A", 2, "CNTT"),
        ("DS002", "Co so du lieu", "NXB Giao duc", 280, "16x24", "Le Thi B", 2, "CNTT"),
        ("DS003", "Mang may tinh", "NXB DHQG", 350, "16x24", "Pham Van C", 2, "CNTT"),
        ("DS004", "Marketing can ban", "NXB Lao dong", 240, "16x24", "Tran Thi D", 2, "QTKD"),
        ("DS005", "Quan tri nhan su", "NXB Tai chinh", 260, "16x24", "Ngo Van E", 2, "QTKD"),
        ("DS006", "Nguyen ly ke toan", "NXB Tai chinh", 300, "16x24", "Vo Thi F", 2, "KT"),
        ("DS007", "Ke toan doanh nghiep", "NXB Tai chinh", 340, "16x24", "Bui Van G", 2, "KT"),
        ("DS008", "Quan tri khach san", "NXB Van hoa", 270, "16x24", "Do Thi H", 2, "DL"),
        ("DS009", "Academic Writing", "Pearson", 210, "19x27", "John Smith", 2, "NN"),
        ("DS010", "English for Presentation", "Oxford", 190, "19x27", "Anna Brown", 2, "NN"),
    ]
    db.add_all(
        [
            BookTitle(
                ma_dau_sach=code,
                ten_dau_sach=name,
                nha_xuat_ban=publisher,
                so_trang=pages,
                kich_thuoc=size,
                tac_gia=author,
                so_luong_sach=qty,
                chuyen_nganh_id=category_map[cat_code],
            )
            for code, name, publisher, pages, size, author, qty, cat_code in book_titles
        ]
    )


def seed_book_copies(db):
    if db.scalar(select(BookCopy).limit(1)):
        return
    titles = db.scalars(select(BookTitle).order_by(BookTitle.id)).all()
    copies = []
    index = 1
    for title in titles:
        for _ in range(2):
            copies.append(
                BookCopy(
                    ma_sach=f"S{index:03d}",
                    dau_sach_id=title.id,
                    tinh_trang=BookCopyStatus.AVAILABLE,
                    ngay_nhap=date(2026, 1, min(index, 28)),
                )
            )
            index += 1
    db.add_all(copies)


def seed_readers(db):
    if db.scalar(select(Reader).limit(1)):
        return
    readers = [
        Reader(
            ma_doc_gia=f"DG{i:03d}",
            ho_ten=f"Sinh vien {i}",
            lop=f"DH{i % 4 + 1}A{i % 3 + 1}",
            ngay_sinh=date(2004, (i % 12) + 1, (i % 28) + 1),
            gioi_tinh="Nam" if i % 2 else "Nu",
        )
        for i in range(1, 11)
    ]
    db.add_all(readers)


def main():
    with SessionLocal() as db:
        seed_users(db)
        db.commit()
        seed_categories(db)
        db.commit()
        seed_book_titles(db)
        db.commit()
        seed_book_copies(db)
        seed_readers(db)
        db.commit()
    print("Seed du lieu thanh cong.")


if __name__ == "__main__":
    main()
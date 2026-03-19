# He thong quan ly thu vien cho truong Dai hoc

MVP full-stack gom:
- `server/`: FastAPI + SQLAlchemy + Alembic + JWT auth
- `client/`: React + Vite + Tailwind CSS + React Router + Axios

## Tinh nang da hoan thanh
- Dang nhap JWT va phan quyen `ADMIN`, `LIBRARIAN`
- CRUD nguoi dung he thong
- CRUD doc gia
- CRUD chuyen nganh
- CRUD dau sach
- CRUD ban sao sach
- Lap phieu muon sach
- Xu ly tra sach
- Bao cao top dau sach duoc muon nhieu
- Bao cao doc gia chua tra sach
- Giao dien tieng Viet co sidebar, topbar, bang du lieu, modal form, toast va protected routes

## Cau truc thu muc
```text
client/
server/
```

## Chay nhanh cho demo local
### 1. Backend
```bash
cd server
python -m pip install -r requirements.txt
alembic upgrade head
python scripts/seed.py
uvicorn app.main:app --reload
```

Mac dinh backend se dung SQLite tai `server/library.db` de demo nhanh.

### 2. Frontend
```bash
cd client
npm install
npm run dev
```

Frontend mac dinh goi API toi `http://localhost:8000/api`.

## Chuyen sang MySQL
1. Tao database MySQL, vi du `library_management`.
2. Copy `server/.env.example` thanh `server/.env`.
3. Sua `DATABASE_URL`, vi du:
```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/library_management
```
4. Chay lai:
```bash
cd server
alembic upgrade head
python scripts/seed.py
```

## Tai khoan mac dinh
- `admin` / `Admin@123`
- `thuthu01` / `ThuThu@123`
- `thuthu02` / `ThuThu@123`

## API chinh
- `POST /api/auth/login`
- `GET /api/auth/me`
- `GET/POST/PUT/DELETE /api/users`
- `GET/POST/PUT/DELETE /api/readers`
- `GET/POST/PUT/DELETE /api/categories`
- `GET/POST/PUT/DELETE /api/book-titles`
- `GET/POST/PUT/DELETE /api/book-copies`
- `GET /api/borrow-slips`
- `POST /api/borrow-slips/borrow`
- `POST /api/borrow-slips/return/{id}`
- `GET /api/reports/top-borrowed-books`
- `GET /api/reports/unreturned-readers`

## Business rules dang duoc ap dung
- Moi doc gia chi duoc muon 1 sach tai 1 thoi diem.
- Ban sao sach chi duoc muon khi o trang thai `AVAILABLE`.
- Muon sach se tao phieu muon va chuyen trang thai sach sang `BORROWED`.
- Tra sach se cap nhat ngay tra, trang thai tra va tinh trang sach sau khi tra.
- Khong cho phep trung ma doc gia, ma chuyen nganh, ma dau sach, ma sach, username, ma phieu muon.
- Khong cho xoa chuyen nganh neu con dau sach.
- Khong cho xoa dau sach neu con ban sao.
- Khong cho xoa doc gia hoac ban sao sach neu da phat sinh lich su muon tra.

## Kiem tra da thuc hien
- Build frontend thanh cong voi `npm run build`
- Import FastAPI app thanh cong
- Alembic migration thanh cong
- Seed du lieu thanh cong
- Da verify login, CRUD chinh, borrow/return va report bang FastAPI `TestClient`

## Gioi han MVP
- Chua co pagination server-side
- Chua co test suite chinh thuc bang pytest
- Chua co dashboard chart, moi dung the thong ke va bang bao cao
- Frontend dang dung modal don gian thay vi form page rieng
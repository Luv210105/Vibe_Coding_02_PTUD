# Hệ thống quản lý thư viện cho trường Đại học

Đây là dự án MVP full-stack gồm:
- `server/`: FastAPI + SQLAlchemy + Alembic + JWT Authentication
- `client/`: React + Vite + Tailwind CSS + React Router + Axios

## Tính năng đã hoàn thành
- Đăng nhập bằng JWT và phân quyền `ADMIN`, `LIBRARIAN`
- Quản lý người dùng hệ thống
- Quản lý độc giả
- Quản lý chuyên ngành
- Quản lý đầu sách
- Quản lý bản sao sách
- Lập phiếu mượn sách
- Xử lý trả sách
- Báo cáo đầu sách được mượn nhiều
- Báo cáo độc giả chưa trả sách
- Giao diện tiếng Việt có sidebar, topbar, bảng dữ liệu, modal form, toast và protected routes

## Cấu trúc thư mục
```text
client/
server/
```

## Chạy nhanh trên máy local

### 1. Chạy backend
```bash
cd server
python -m pip install -r requirements.txt
alembic upgrade head
python scripts/seed.py
uvicorn app.main:app --reload
```

Backend mặc định dùng SQLite tại `server/library.db` để demo nhanh.

### 2. Chạy frontend
```bash
cd client
npm install
npm run dev
```

Frontend mặc định gọi API tại `http://localhost:8000/api`.

## Chuyển sang MySQL
1. Tạo database MySQL, ví dụ: `library_management`.
2. Sao chép `server/.env.example` thành `server/.env`.
3. Cập nhật `DATABASE_URL`, ví dụ:

```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/library_management
```

4. Chạy lại migration và seed:

```bash
cd server
alembic upgrade head
python scripts/seed.py
```

## Tài khoản mặc định
- `admin` / `Admin@123`
- `thuthu01` / `ThuThu@123`
- `thuthu02` / `ThuThu@123`

## Các API chính
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

## Các quy tắc nghiệp vụ đang áp dụng
- Mỗi độc giả chỉ được mượn 1 sách tại 1 thời điểm.
- Bản sao sách chỉ được mượn khi ở trạng thái `AVAILABLE`.
- Khi mượn sách, hệ thống tạo phiếu mượn và cập nhật trạng thái sách thành `BORROWED`.
- Khi trả sách, hệ thống cập nhật ngày trả, trạng thái trả và tình trạng sách sau khi trả.
- Không cho phép trùng: mã độc giả, mã chuyên ngành, mã đầu sách, mã sách, username, mã phiếu mượn.
- Không cho xóa chuyên ngành nếu vẫn còn đầu sách liên quan.
- Không cho xóa đầu sách nếu vẫn còn bản sao liên quan.
- Không cho xóa độc giả hoặc bản sao sách nếu đã phát sinh lịch sử mượn trả.

## Kiểm tra đã thực hiện
- Build frontend thành công với `npm run build`
- Import FastAPI app thành công
- Alembic migration thành công
- Seed dữ liệu thành công
- Đã verify login, CRUD chính, luồng mượn/trả và báo cáo bằng `FastAPI TestClient`

## Giới hạn hiện tại của MVP
- Chưa có phân trang phía server
- Chưa có test suite chính thức bằng `pytest`
- Chưa có biểu đồ dashboard, hiện mới dùng thẻ thống kê và bảng báo cáo
- Frontend đang dùng modal đơn giản thay vì trang form riêng

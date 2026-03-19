"""Initial library schema."""

from alembic import op
import sqlalchemy as sa


revision = "20260319_0001"
down_revision = None
branch_labels = None
depends_on = None


user_role = sa.Enum("ADMIN", "LIBRARIAN", name="userrole")
book_copy_status = sa.Enum("AVAILABLE", "BORROWED", "DAMAGED", "LOST", name="bookcopystatus")
return_status = sa.Enum("BORROWING", "RETURNED", "LATE", name="returnstatus")


def upgrade() -> None:
    bind = op.get_bind()
    user_role.create(bind, checkfirst=True)
    book_copy_status.create(bind, checkfirst=True)
    return_status.create(bind, checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=120), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)

    op.create_table(
        "readers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("ma_doc_gia", sa.String(length=30), nullable=False),
        sa.Column("ho_ten", sa.String(length=120), nullable=False),
        sa.Column("lop", sa.String(length=50), nullable=False),
        sa.Column("ngay_sinh", sa.Date(), nullable=False),
        sa.Column("gioi_tinh", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index(op.f("ix_readers_id"), "readers", ["id"], unique=False)
    op.create_index(op.f("ix_readers_ma_doc_gia"), "readers", ["ma_doc_gia"], unique=True)

    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("ma_chuyen_nganh", sa.String(length=30), nullable=False),
        sa.Column("ten_chuyen_nganh", sa.String(length=120), nullable=False),
        sa.Column("mo_ta", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index(op.f("ix_categories_id"), "categories", ["id"], unique=False)
    op.create_index(op.f("ix_categories_ma_chuyen_nganh"), "categories", ["ma_chuyen_nganh"], unique=True)

    op.create_table(
        "book_titles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("ma_dau_sach", sa.String(length=30), nullable=False),
        sa.Column("ten_dau_sach", sa.String(length=200), nullable=False),
        sa.Column("nha_xuat_ban", sa.String(length=120), nullable=False),
        sa.Column("so_trang", sa.Integer(), nullable=False),
        sa.Column("kich_thuoc", sa.String(length=50), nullable=False),
        sa.Column("tac_gia", sa.String(length=150), nullable=False),
        sa.Column("so_luong_sach", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("chuyen_nganh_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["chuyen_nganh_id"], ["categories.id"], ondelete="RESTRICT"),
    )
    op.create_index(op.f("ix_book_titles_id"), "book_titles", ["id"], unique=False)
    op.create_index(op.f("ix_book_titles_ma_dau_sach"), "book_titles", ["ma_dau_sach"], unique=True)

    op.create_table(
        "book_copies",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("ma_sach", sa.String(length=30), nullable=False),
        sa.Column("dau_sach_id", sa.Integer(), nullable=False),
        sa.Column("tinh_trang", book_copy_status, nullable=False, server_default="AVAILABLE"),
        sa.Column("ngay_nhap", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["dau_sach_id"], ["book_titles.id"], ondelete="RESTRICT"),
    )
    op.create_index(op.f("ix_book_copies_id"), "book_copies", ["id"], unique=False)
    op.create_index(op.f("ix_book_copies_ma_sach"), "book_copies", ["ma_sach"], unique=True)

    op.create_table(
        "borrow_slips",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("ma_phieu_muon", sa.String(length=30), nullable=False),
        sa.Column("ma_sach_id", sa.Integer(), nullable=False),
        sa.Column("ma_doc_gia_id", sa.Integer(), nullable=False),
        sa.Column("ma_thu_thu_id", sa.Integer(), nullable=False),
        sa.Column("ngay_muon", sa.Date(), nullable=False),
        sa.Column("ngay_tra", sa.Date(), nullable=True),
        sa.Column("tinh_trang_muon", sa.String(length=120), nullable=False),
        sa.Column("trang_thai_tra", return_status, nullable=False, server_default="BORROWING"),
        sa.Column("ghi_chu_tinh_trang_sach", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["ma_doc_gia_id"], ["readers.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["ma_sach_id"], ["book_copies.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["ma_thu_thu_id"], ["users.id"], ondelete="RESTRICT"),
    )
    op.create_index(op.f("ix_borrow_slips_id"), "borrow_slips", ["id"], unique=False)
    op.create_index(op.f("ix_borrow_slips_ma_phieu_muon"), "borrow_slips", ["ma_phieu_muon"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_borrow_slips_ma_phieu_muon"), table_name="borrow_slips")
    op.drop_index(op.f("ix_borrow_slips_id"), table_name="borrow_slips")
    op.drop_table("borrow_slips")
    op.drop_index(op.f("ix_book_copies_ma_sach"), table_name="book_copies")
    op.drop_index(op.f("ix_book_copies_id"), table_name="book_copies")
    op.drop_table("book_copies")
    op.drop_index(op.f("ix_book_titles_ma_dau_sach"), table_name="book_titles")
    op.drop_index(op.f("ix_book_titles_id"), table_name="book_titles")
    op.drop_table("book_titles")
    op.drop_index(op.f("ix_categories_ma_chuyen_nganh"), table_name="categories")
    op.drop_index(op.f("ix_categories_id"), table_name="categories")
    op.drop_table("categories")
    op.drop_index(op.f("ix_readers_ma_doc_gia"), table_name="readers")
    op.drop_index(op.f("ix_readers_id"), table_name="readers")
    op.drop_table("readers")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
    bind = op.get_bind()
    return_status.drop(bind, checkfirst=True)
    book_copy_status.drop(bind, checkfirst=True)
    user_role.drop(bind, checkfirst=True)

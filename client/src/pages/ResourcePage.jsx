import { useEffect, useMemo, useState } from "react";
import toast from "react-hot-toast";

import DataTable from "../components/DataTable";
import FormModal from "../components/FormModal";

export default function ResourcePage({ title, description, service, columns, fields, toPayload, initialValues, searchPlaceholder = "Tìm kiếm...", canCreate = true }) {
  const [items, setItems] = useState([]);
  const [keyword, setKeyword] = useState("");
  const [open, setOpen] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const modalFields = useMemo(() => fields, [fields]);

  const loadItems = async () => {
    try {
      setItems(await service.list(keyword));
    } catch (error) {
      toast.error(error.response?.data?.detail || "Không tải được dữ liệu.");
    }
  };

  useEffect(() => {
    loadItems();
  }, []);

  const handleSubmit = async (formData) => {
    const payload = toPayload ? toPayload(formData, editingItem) : formData;
    try {
      if (editingItem) {
        await service.update(editingItem.id, payload);
        toast.success("Cập nhật thành công.");
      } else {
        await service.create(payload);
        toast.success("Tạo mới thành công.");
      }
      setOpen(false);
      setEditingItem(null);
      loadItems();
    } catch (error) {
      toast.error(error.response?.data?.detail || "Không lưu được dữ liệu.");
    }
  };

  const handleDelete = async (item) => {
    if (!window.confirm(`Bạn có chắc muốn xóa "${item.fullName || item.hoTen || item.tenChuyenNganh || item.tenDauSach || item.maSach || item.username}"?`)) {
      return;
    }
    try {
      await service.remove(item.id);
      toast.success("Xóa thành công.");
      loadItems();
    } catch (error) {
      toast.error(error.response?.data?.detail || "Không xóa được dữ liệu.");
    }
  };

  return (
    <section className="space-y-5">
      <div className="flex flex-col gap-4 rounded-3xl bg-white/90 p-6 shadow-panel md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">{title}</h1>
          <p className="mt-1 text-sm text-slate-500">{description}</p>
        </div>
        <div className="flex flex-col gap-3 md:flex-row">
          <input className="field-input md:w-72" placeholder={searchPlaceholder} value={keyword} onChange={(e) => setKeyword(e.target.value)} />
          <button className="secondary-button" onClick={loadItems}>Tìm</button>
          {canCreate ? (
            <button className="primary-button" onClick={() => { setEditingItem(null); setOpen(true); }}>
              Thêm mới
            </button>
          ) : null}
        </div>
      </div>
      <DataTable
        columns={columns}
        rows={items}
        emptyMessage="Chưa có dữ liệu phù hợp."
        actions={(row) => (
          <div className="flex justify-end gap-2">
            <button className="secondary-button px-3 py-2" onClick={() => { setEditingItem(row); setOpen(true); }}>Sửa</button>
            <button className="rounded-xl bg-rose-50 px-3 py-2 text-sm font-semibold text-rose-600" onClick={() => handleDelete(row)}>Xóa</button>
          </div>
        )}
      />
      <FormModal
        open={open}
        title={editingItem ? `Cập nhật ${title.toLowerCase()}` : `Thêm ${title.toLowerCase()}`}
        fields={modalFields}
        initialValues={editingItem || initialValues}
        onClose={() => { setOpen(false); setEditingItem(null); }}
        onSubmit={handleSubmit}
        submitLabel={editingItem ? "Cập nhật" : "Tạo mới"}
      />
    </section>
  );
}
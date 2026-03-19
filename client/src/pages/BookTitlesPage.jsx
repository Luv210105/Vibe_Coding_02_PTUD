import { useEffect, useState } from "react";

import ResourcePage from "./ResourcePage";
import { createResourceService } from "../services/resourceService";

const service = createResourceService("/book-titles");
const categoryService = createResourceService("/categories");

export default function BookTitlesPage() {
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    categoryService.list().then(setCategories);
  }, []);

  return (
    <ResourcePage
      title="Quản lý đầu sách"
      description="Theo dõi danh mục đầu sách, tác giả và chuyên ngành liên quan."
      service={service}
      columns={[
        { key: "maDauSach", label: "Mã đầu sách" },
        { key: "tenDauSach", label: "Tên đầu sách" },
        { key: "tacGia", label: "Tác giả" },
        { key: "nhaXuatBan", label: "Nhà xuất bản" },
        { key: "soLuongSach", label: "Số lượng" },
        { key: "category", label: "Chuyên ngành", render: (row) => row.category?.tenChuyenNganh || "-" },
      ]}
      fields={[
        { name: "maDauSach", label: "Mã đầu sách", required: true },
        { name: "tenDauSach", label: "Tên đầu sách", required: true },
        { name: "nhaXuatBan", label: "Nhà xuất bản", required: true },
        { name: "soTrang", label: "Số trang", type: "number", min: 1, required: true },
        { name: "kichThuoc", label: "Kích thước", required: true },
        { name: "tacGia", label: "Tác giả", required: true },
        { name: "soLuongSach", label: "Số lượng sách", type: "number", min: 0, required: true },
        { name: "chuyenNganhId", label: "Chuyên ngành", type: "select", required: true, options: categories.map((item) => ({ value: item.id, label: item.tenChuyenNganh })) },
      ]}
      initialValues={{ soTrang: 100, soLuongSach: 1 }}
      toPayload={(formData) => ({ ...formData, soTrang: Number(formData.soTrang), soLuongSach: Number(formData.soLuongSach), chuyenNganhId: Number(formData.chuyenNganhId) })}
    />
  );
}
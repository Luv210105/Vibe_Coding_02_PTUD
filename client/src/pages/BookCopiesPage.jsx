import { useEffect, useState } from "react";

import ResourcePage from "./ResourcePage";
import { createResourceService } from "../services/resourceService";
import { formatDate, statusLabels } from "../utils/format";

const service = createResourceService("/book-copies");
const titleService = createResourceService("/book-titles");

export default function BookCopiesPage() {
  const [titles, setTitles] = useState([]);

  useEffect(() => {
    titleService.list().then(setTitles);
  }, []);

  return (
    <ResourcePage
      title="Quản lý bản sao sách"
      description="Quản lý từng cuốn sách vật lý và trạng thái mượn trả hiện tại."
      service={service}
      columns={[
        { key: "maSach", label: "Mã sách" },
        { key: "bookTitle", label: "Đầu sách", render: (row) => row.bookTitle?.tenDauSach || "-" },
        { key: "tinhTrang", label: "Tình trạng", render: (row) => statusLabels[row.tinhTrang] || row.tinhTrang },
        { key: "ngayNhap", label: "Ngày nhập", render: (row) => formatDate(row.ngayNhap) },
      ]}
      fields={[
        { name: "maSach", label: "Mã sách", required: true },
        { name: "dauSachId", label: "Đầu sách", type: "select", required: true, options: titles.map((item) => ({ value: item.id, label: `${item.maDauSach} - ${item.tenDauSach}` })) },
        { name: "tinhTrang", label: "Tình trạng", type: "select", required: true, options: ["AVAILABLE", "BORROWED", "DAMAGED", "LOST"].map((value) => ({ value, label: statusLabels[value] })) },
        { name: "ngayNhap", label: "Ngày nhập", type: "date", required: true },
      ]}
      initialValues={{ tinhTrang: "AVAILABLE" }}
      toPayload={(formData) => ({ ...formData, dauSachId: Number(formData.dauSachId) })}
    />
  );
}
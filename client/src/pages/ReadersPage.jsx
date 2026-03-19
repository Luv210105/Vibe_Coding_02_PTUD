import ResourcePage from "./ResourcePage";
import { createResourceService } from "../services/resourceService";
import { formatDate } from "../utils/format";

const service = createResourceService("/readers");

export default function ReadersPage() {
  return (
    <ResourcePage
      title="Quản lý độc giả"
      description="Quản lý thông tin độc giả và thẻ thư viện cho sinh viên."
      service={service}
      columns={[
        { key: "maDocGia", label: "Mã độc giả" },
        { key: "hoTen", label: "Họ tên" },
        { key: "lop", label: "Lớp" },
        { key: "ngaySinh", label: "Ngày sinh", render: (row) => formatDate(row.ngaySinh) },
        { key: "gioiTinh", label: "Giới tính" },
      ]}
      fields={[
        { name: "maDocGia", label: "Mã độc giả", required: true },
        { name: "hoTen", label: "Họ tên", required: true },
        { name: "lop", label: "Lớp", required: true },
        { name: "ngaySinh", label: "Ngày sinh", type: "date", required: true },
        { name: "gioiTinh", label: "Giới tính", type: "select", required: true, options: [{ value: "Nam", label: "Nam" }, { value: "Nu", label: "Nữ" }] },
      ]}
      initialValues={{ gioiTinh: "Nam" }}
    />
  );
}
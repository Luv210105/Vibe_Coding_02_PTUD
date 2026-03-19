import ResourcePage from "./ResourcePage";
import { createResourceService } from "../services/resourceService";
import { statusLabels } from "../utils/format";

const service = createResourceService("/users");

export default function UsersPage() {
  return (
    <ResourcePage
      title="Quản lý người dùng hệ thống"
      description="Quản trị tài khoản đăng nhập cho quản trị viên và thủ thư."
      service={service}
      columns={[
        { key: "username", label: "Username" },
        { key: "fullName", label: "Họ tên" },
        { key: "role", label: "Vai trò", render: (row) => statusLabels[row.role] || row.role },
        { key: "isActive", label: "Trạng thái", render: (row) => (row.isActive ? "Đang hoạt động" : "Đã khóa") },
      ]}
      fields={[
        { name: "username", label: "Tên đăng nhập", required: true },
        { name: "fullName", label: "Họ tên", required: true },
        { name: "role", label: "Vai trò", type: "select", required: true, options: [{ value: "ADMIN", label: "Quản trị viên" }, { value: "LIBRARIAN", label: "Thủ thư" }] },
        { name: "password", label: "Mật khẩu", type: "password", required: true },
        { name: "isActive", label: "Trạng thái", type: "select", required: true, options: [{ value: true, label: "Đang hoạt động" }, { value: false, label: "Đã khóa" }] },
      ]}
      initialValues={{ role: "LIBRARIAN", isActive: true }}
      toPayload={(formData, editingItem) => {
        const payload = { ...formData, isActive: formData.isActive === true || formData.isActive === "true" };
        if (editingItem && !payload.password) {
          delete payload.password;
        }
        return payload;
      }}
    />
  );
}
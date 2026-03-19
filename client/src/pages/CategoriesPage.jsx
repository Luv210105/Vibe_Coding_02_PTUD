import ResourcePage from "./ResourcePage";
import { createResourceService } from "../services/resourceService";

const service = createResourceService("/categories");

export default function CategoriesPage() {
  return (
    <ResourcePage
      title="Quản lý chuyên ngành"
      description="Phân loại đầu sách theo chuyên ngành đào tạo của trường."
      service={service}
      columns={[
        { key: "maChuyenNganh", label: "Mã chuyên ngành" },
        { key: "tenChuyenNganh", label: "Tên chuyên ngành" },
        { key: "moTa", label: "Mô tả" },
      ]}
      fields={[
        { name: "maChuyenNganh", label: "Mã chuyên ngành", required: true },
        { name: "tenChuyenNganh", label: "Tên chuyên ngành", required: true },
        { name: "moTa", label: "Mô tả", type: "textarea", fullWidth: true },
      ]}
    />
  );
}
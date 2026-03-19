import { useEffect, useState } from "react";
import toast from "react-hot-toast";

import DataTable from "../components/DataTable";
import FormModal from "../components/FormModal";
import { borrowService } from "../services/borrowService";
import { formatDate } from "../utils/format";

export default function ReturnPage() {
  const [borrowSlips, setBorrowSlips] = useState([]);
  const [selectedSlip, setSelectedSlip] = useState(null);

  const loadData = async () => {
    const slips = await borrowService.list();
    setBorrowSlips(slips.filter((item) => item.trangThaiTra === "BORROWING"));
  };

  useEffect(() => {
    loadData().catch(() => toast.error("Không tải được dữ liệu trả sách."));
  }, []);

  return (
    <section className="space-y-5">
      <div className="rounded-3xl bg-white/90 p-6 shadow-panel dark:bg-slate-950/85">
        <h1 className="text-2xl font-bold text-slate-800 dark:text-white">Quản lý trả sách</h1>
        <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">Xử lý trả sách, cập nhật ghi chú và trạng thái thực tế của bản sao sách.</p>
      </div>
      <DataTable
        columns={[
          { key: "maPhieuMuon", label: "Mã phiếu" },
          { key: "reader", label: "Độc giả", render: (row) => row.reader?.hoTen || "-" },
          { key: "bookCopy", label: "Mã sách", render: (row) => row.bookCopy?.maSach || "-" },
          { key: "ngayMuon", label: "Ngày mượn", render: (row) => formatDate(row.ngayMuon) },
          { key: "tinhTrangMuon", label: "Tình trạng khi mượn" },
        ]}
        rows={borrowSlips}
        emptyMessage="Không có phiếu mượn nào chờ trả."
        actions={(row) => <button className="primary-button px-3 py-2" onClick={() => setSelectedSlip(row)}>Trả sách</button>}
      />
      <FormModal
        open={Boolean(selectedSlip)}
        title="Xử lý trả sách"
        fields={[
          { name: "ngayTra", label: "Ngày trả", type: "date", required: true },
          { name: "trangThaiTra", label: "Kết quả trả", type: "select", required: true, options: [{ value: "RETURNED", label: "Đã trả" }, { value: "LATE", label: "Trả trễ" }] },
          { name: "tinhTrangSachSauKhiTra", label: "Tình trạng sách sau khi trả", type: "select", required: true, options: [{ value: "AVAILABLE", label: "Sẵn sàng" }, { value: "DAMAGED", label: "Hư hỏng" }, { value: "LOST", label: "Thất lạc" }] },
          { name: "ghiChuTinhTrangSach", label: "Ghi chú tình trạng sách", type: "textarea", fullWidth: true },
        ]}
        initialValues={{ ngayTra: new Date().toISOString().slice(0, 10), trangThaiTra: "RETURNED", tinhTrangSachSauKhiTra: "AVAILABLE" }}
        onClose={() => setSelectedSlip(null)}
        onSubmit={async (formData) => {
          try {
            await borrowService.returnBook(selectedSlip.id, formData);
            toast.success("Xử lý trả sách thành công.");
            setSelectedSlip(null);
            loadData();
          } catch (error) {
            toast.error(error.response?.data?.detail || "Không xử lý được trả sách.");
          }
        }}
        submitLabel="Xác nhận trả"
      />
    </section>
  );
}
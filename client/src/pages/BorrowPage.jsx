import { useEffect, useState } from "react";
import toast from "react-hot-toast";

import DataTable from "../components/DataTable";
import FormModal from "../components/FormModal";
import { borrowService } from "../services/borrowService";
import { createResourceService } from "../services/resourceService";
import { formatDate, statusLabels } from "../utils/format";

const readerService = createResourceService("/readers");
const copyService = createResourceService("/book-copies");

export default function BorrowPage() {
  const [borrowSlips, setBorrowSlips] = useState([]);
  const [readers, setReaders] = useState([]);
  const [copies, setCopies] = useState([]);
  const [open, setOpen] = useState(false);

  const loadData = async () => {
    const [slips, readerData, copyData] = await Promise.all([borrowService.list(), readerService.list(), copyService.list()]);
    setBorrowSlips(slips);
    setReaders(readerData);
    setCopies(copyData.filter((item) => item.tinhTrang === "AVAILABLE"));
  };

  useEffect(() => {
    loadData().catch(() => toast.error("Không tải được dữ liệu mượn sách."));
  }, []);

  return (
    <section className="space-y-5">
      <div className="flex flex-col gap-4 rounded-3xl bg-white/90 p-6 shadow-panel md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Quản lý mượn sách</h1>
          <p className="mt-1 text-sm text-slate-500">Lập phiếu mượn và cập nhật trạng thái bản sao sách sang đang mượn.</p>
        </div>
        <button className="primary-button" onClick={() => setOpen(true)}>Tạo phiếu mượn</button>
      </div>
      <DataTable
        columns={[
          { key: "maPhieuMuon", label: "Mã phiếu" },
          { key: "reader", label: "Độc giả", render: (row) => row.reader?.hoTen || "-" },
          { key: "bookCopy", label: "Mã sách", render: (row) => row.bookCopy?.maSach || "-" },
          { key: "ngayMuon", label: "Ngày mượn", render: (row) => formatDate(row.ngayMuon) },
          { key: "trangThaiTra", label: "Trạng thái", render: (row) => statusLabels[row.trangThaiTra] || row.trangThaiTra },
        ]}
        rows={borrowSlips}
        emptyMessage="Chưa có phiếu mượn nào."
      />
      <FormModal
        open={open}
        title="Tạo phiếu mượn"
        fields={[
          { name: "maPhieuMuon", label: "Mã phiếu mượn", required: true },
          { name: "maDocGiaId", label: "Độc giả", type: "select", required: true, options: readers.map((item) => ({ value: item.id, label: `${item.maDocGia} - ${item.hoTen}` })) },
          { name: "maSachId", label: "Bản sao sách", type: "select", required: true, options: copies.map((item) => ({ value: item.id, label: `${item.maSach} - ${item.bookTitle?.tenDauSach || ""}` })) },
          { name: "ngayMuon", label: "Ngày mượn", type: "date", required: true },
          { name: "tinhTrangMuon", label: "Tình trạng khi mượn", required: true, fullWidth: true },
        ]}
        initialValues={{ ngayMuon: new Date().toISOString().slice(0, 10), tinhTrangMuon: "Sách nguyên vẹn" }}
        onClose={() => setOpen(false)}
        onSubmit={async (formData) => {
          try {
            await borrowService.borrow({ ...formData, maDocGiaId: Number(formData.maDocGiaId), maSachId: Number(formData.maSachId) });
            toast.success("Tạo phiếu mượn thành công.");
            setOpen(false);
            loadData();
          } catch (error) {
            toast.error(error.response?.data?.detail || "Không tạo được phiếu mượn.");
          }
        }}
        submitLabel="Lập phiếu"
      />
    </section>
  );
}
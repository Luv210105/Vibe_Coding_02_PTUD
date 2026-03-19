import { useEffect, useState } from "react";
import toast from "react-hot-toast";

import DataTable from "../components/DataTable";
import { reportService } from "../services/reportService";
import { formatDate } from "../utils/format";

export default function ReportsPage() {
  const [filters, setFilters] = useState({ fromDate: "", toDate: "" });
  const [topBooks, setTopBooks] = useState([]);
  const [unreturnedReaders, setUnreturnedReaders] = useState([]);

  const loadReports = async () => {
    try {
      const [topBooksData, unreturnedData] = await Promise.all([
        reportService.topBorrowedBooks(filters),
        reportService.unreturnedReaders(filters),
      ]);
      setTopBooks(topBooksData);
      setUnreturnedReaders(unreturnedData);
    } catch (error) {
      toast.error(error.response?.data?.detail || "Không tải được báo cáo.");
    }
  };

  useEffect(() => {
    loadReports();
  }, []);

  return (
    <section className="space-y-5">
      <div className="rounded-3xl bg-white/90 p-6 shadow-panel dark:bg-slate-950/85">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <h1 className="text-2xl font-bold text-slate-800 dark:text-white">Báo cáo thống kê</h1>
            <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">Theo dõi đầu sách được mượn nhiều và độc giả chưa trả sách.</p>
          </div>
          <div className="flex flex-col gap-3 md:flex-row">
            <label>
              <span className="field-label">Từ ngày</span>
              <input className="field-input" type="date" value={filters.fromDate} onChange={(e) => setFilters((prev) => ({ ...prev, fromDate: e.target.value }))} />
            </label>
            <label>
              <span className="field-label">Đến ngày</span>
              <input className="field-input" type="date" value={filters.toDate} onChange={(e) => setFilters((prev) => ({ ...prev, toDate: e.target.value }))} />
            </label>
            <button className="primary-button" onClick={loadReports}>Lọc báo cáo</button>
          </div>
        </div>
      </div>
      <div className="grid gap-5 xl:grid-cols-2">
        <div className="space-y-3">
          <h2 className="text-xl font-bold text-slate-800 dark:text-white">Top đầu sách được mượn nhiều</h2>
          <DataTable
            columns={[
              { key: "maDauSach", label: "Mã đầu sách" },
              { key: "tenDauSach", label: "Tên đầu sách" },
              { key: "totalBorrows", label: "Lượt mượn" },
            ]}
            rows={topBooks}
            emptyMessage="Chưa có dữ liệu báo cáo."
          />
        </div>
        <div className="space-y-3">
          <h2 className="text-xl font-bold text-slate-800 dark:text-white">Độc giả chưa trả sách</h2>
          <DataTable
            columns={[
              { key: "maDocGia", label: "Mã độc giả" },
              { key: "hoTen", label: "Họ tên" },
              { key: "maPhieuMuon", label: "Mã phiếu" },
              { key: "maSach", label: "Mã sách" },
              { key: "ngayMuon", label: "Ngày mượn", render: (row) => formatDate(row.ngayMuon) },
            ]}
            rows={unreturnedReaders}
            emptyMessage="Không có độc giả nào chưa trả sách."
          />
        </div>
      </div>
    </section>
  );
}
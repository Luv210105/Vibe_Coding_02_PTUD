import { useEffect, useState } from "react";

import StatCard from "../components/StatCard";
import { borrowService } from "../services/borrowService";
import { createResourceService } from "../services/resourceService";

const readerService = createResourceService("/readers");
const categoryService = createResourceService("/categories");
const titleService = createResourceService("/book-titles");
const copyService = createResourceService("/book-copies");

export default function DashboardPage() {
  const [stats, setStats] = useState({ readers: 0, categories: 0, titles: 0, copies: 0, slips: 0 });

  useEffect(() => {
    Promise.all([readerService.list(), categoryService.list(), titleService.list(), copyService.list(), borrowService.list()]).then(
      ([readers, categories, titles, copies, slips]) => {
        setStats({ readers: readers.length, categories: categories.length, titles: titles.length, copies: copies.length, slips: slips.length });
      }
    );
  }, []);

  return (
    <section className="space-y-6">
      <div className="rounded-3xl bg-gradient-to-r from-brand-700 to-brand-500 p-8 text-white shadow-panel">
        <p className="text-sm uppercase tracking-[0.22em] text-brand-100">Tổng quan thư viện</p>
        <h1 className="mt-3 text-3xl font-bold">Quản lý sách, độc giả và mượn trả trên một màn hình tập trung</h1>
      </div>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
        <StatCard label="Độc giả" value={stats.readers} hint="Số độc giả đã đăng ký" />
        <StatCard label="Chuyên ngành" value={stats.categories} hint="Nhóm tài liệu đang quản lý" />
        <StatCard label="Đầu sách" value={stats.titles} hint="Danh mục đầu sách hiện có" />
        <StatCard label="Bản sao" value={stats.copies} hint="Tổng số bản sách vật lý" />
        <StatCard label="Phiếu mượn" value={stats.slips} hint="Tất cả phiếu mượn trong hệ thống" />
      </div>
    </section>
  );
}
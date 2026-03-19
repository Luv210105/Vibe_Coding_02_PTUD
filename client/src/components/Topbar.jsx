import { statusLabels } from "../utils/format";

export default function Topbar({ user, onLogout }) {
  return (
    <header className="flex flex-col gap-4 rounded-3xl bg-white/80 p-5 shadow-panel backdrop-blur md:flex-row md:items-center md:justify-between">
      <div>
        <p className="text-sm font-medium uppercase tracking-[0.22em] text-brand-600">Thư viện đại học</p>
        <h2 className="mt-1 text-2xl font-bold text-slate-800">Xin chào, {user.fullName}</h2>
      </div>
      <div className="flex items-center gap-3">
        <div className="rounded-2xl bg-slate-100 px-4 py-2 text-sm text-slate-600">
          Vai trò: <span className="font-semibold text-slate-800">{statusLabels[user.role]}</span>
        </div>
        <button className="secondary-button" onClick={onLogout}>
          Đăng xuất
        </button>
      </div>
    </header>
  );
}
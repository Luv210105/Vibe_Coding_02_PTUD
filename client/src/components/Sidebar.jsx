import { NavLink } from "react-router-dom";

import { navigationItems } from "../utils/navigation";

export default function Sidebar({ role }) {
  const items = navigationItems.filter((item) => item.roles.includes(role));

  return (
    <aside className="w-full shrink-0 border-r border-white/50 bg-white/80 p-5 backdrop-blur xl:w-72">
      <div className="mb-8 rounded-3xl bg-brand-600 p-5 text-white shadow-panel">
        <p className="text-sm uppercase tracking-[0.24em] text-brand-100">University Library</p>
        <h1 className="mt-2 text-2xl font-bold leading-tight">Hệ thống quản lý thư viện</h1>
      </div>
      <nav className="space-y-2">
        {items.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `block rounded-2xl px-4 py-3 text-sm font-medium transition ${
                isActive ? "bg-brand-50 text-brand-700" : "text-slate-600 hover:bg-slate-100"
              }`
            }
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
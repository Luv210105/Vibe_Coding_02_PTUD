import { Outlet, useNavigate } from "react-router-dom";

import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import { useAuth } from "../hooks/useAuth";

export default function DashboardLayout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="min-h-screen xl:flex">
      <Sidebar role={user.role} />
      <main className="flex-1 p-4 md:p-6 xl:p-8">
        <Topbar
          user={user}
          onLogout={() => {
            logout();
            navigate("/login");
          }}
        />
        <div className="mt-6">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
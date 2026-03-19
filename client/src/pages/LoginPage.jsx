import { useState } from "react";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";

import { useAuth } from "../hooks/useAuth";

export default function LoginPage() {
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("Admin@123");
  const [submitting, setSubmitting] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSubmitting(true);
    try {
      await login({ username, password });
      navigate("/");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Đăng nhập thất bại.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <div className="grid w-full max-w-5xl overflow-hidden rounded-[2rem] bg-white shadow-2xl lg:grid-cols-[1.1fr_0.9fr]">
        <div className="bg-brand-700 p-10 text-white">
          <p className="text-sm uppercase tracking-[0.24em] text-brand-100">Library MVP</p>
          <h1 className="mt-4 text-4xl font-bold leading-tight">Hệ thống quản lý thư viện cho trường Đại học</h1>
          <p className="mt-6 max-w-md text-white/80">Quản lý độc giả, sách, mượn trả và báo cáo trên một giao diện tiếng Việt dễ dùng cho thủ thư và quản trị viên.</p>
        </div>
        <div className="p-8 md:p-10">
          <h2 className="text-2xl font-bold text-slate-800">Đăng nhập hệ thống</h2>
          <p className="mt-2 text-sm text-slate-500">Sử dụng tài khoản mặc định để kiểm thử nhanh.</p>
          <form className="mt-8 space-y-4" onSubmit={handleSubmit}>
            <label>
              <span className="field-label">Tên đăng nhập</span>
              <input className="field-input" value={username} onChange={(e) => setUsername(e.target.value)} required />
            </label>
            <label>
              <span className="field-label">Mật khẩu</span>
              <input className="field-input" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
            </label>
            <button className="primary-button w-full" disabled={submitting}>
              {submitting ? "Đang đăng nhập..." : "Đăng nhập"}
            </button>
          </form>
          <div className="mt-6 rounded-2xl bg-slate-50 p-4 text-sm text-slate-600">
            <p className="font-semibold text-slate-800">Tài khoản gợi ý</p>
            <p>`admin` / `Admin@123`</p>
            <p>`thuthu01` / `ThuThu@123`</p>
          </div>
        </div>
      </div>
    </div>
  );
}
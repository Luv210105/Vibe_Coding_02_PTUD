import { useEffect, useState } from "react";
import { Navigate, Route, Routes, useLocation } from "react-router-dom";

import { useAuth } from "./hooks/useAuth";
import DashboardLayout from "./layouts/DashboardLayout";
import BookCopiesPage from "./pages/BookCopiesPage";
import BookTitlesPage from "./pages/BookTitlesPage";
import BorrowPage from "./pages/BorrowPage";
import CategoriesPage from "./pages/CategoriesPage";
import ThemeToggle from "./components/ThemeToggle";
import DashboardPage from "./pages/DashboardPage";
import LoginPage from "./pages/LoginPage";
import ReadersPage from "./pages/ReadersPage";
import ReportsPage from "./pages/ReportsPage";
import ReturnPage from "./pages/ReturnPage";
import UsersPage from "./pages/UsersPage";

function ProtectedRoute({ children, roles }) {
  const { user, loading, isAuthenticated } = useAuth();
  const location = useLocation();

  if (loading) {
    return <div className="flex min-h-screen items-center justify-center text-slate-500 dark:text-slate-300">Đang tải...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  if (roles && !roles.includes(user.role)) {
    return <Navigate to="/" replace />;
  }

  return children;
}

export default function App() {
  const { isAuthenticated } = useAuth();
  const [theme, setTheme] = useState(() => localStorage.getItem("library_theme") || "light");

  useEffect(() => {
    document.documentElement.classList.toggle("dark", theme === "dark");
    localStorage.setItem("library_theme", theme);
  }, [theme]);

  const toggleTheme = () => setTheme((current) => (current === "dark" ? "light" : "dark"));

  return (
    <>
      <Routes>
        <Route path="/login" element={isAuthenticated ? <Navigate to="/" replace /> : <LoginPage />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <DashboardLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<DashboardPage />} />
          <Route path="readers" element={<ReadersPage />} />
          <Route path="categories" element={<CategoriesPage />} />
          <Route path="book-titles" element={<BookTitlesPage />} />
          <Route path="book-copies" element={<BookCopiesPage />} />
          <Route path="borrow" element={<BorrowPage />} />
          <Route path="return" element={<ReturnPage />} />
          <Route path="reports" element={<ReportsPage />} />
          <Route
            path="users"
            element={
              <ProtectedRoute roles={["ADMIN"]}>
                <UsersPage />
              </ProtectedRoute>
            }
          />
        </Route>
        <Route path="*" element={<Navigate to={isAuthenticated ? "/" : "/login"} replace />} />
      </Routes>
      <ThemeToggle theme={theme} onToggleTheme={toggleTheme} />
    </>
  );
}

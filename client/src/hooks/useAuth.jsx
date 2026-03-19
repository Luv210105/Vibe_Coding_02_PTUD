import { createContext, useContext, useEffect, useMemo, useState } from "react";
import toast from "react-hot-toast";

import { authService } from "../services/auth";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("library_token");
    if (!token) {
      setLoading(false);
      return;
    }
    authService
      .me()
      .then(setUser)
      .catch(() => {
        localStorage.removeItem("library_token");
        setUser(null);
      })
      .finally(() => setLoading(false));
  }, []);

  const value = useMemo(
    () => ({
      user,
      loading,
      isAuthenticated: Boolean(user),
      login: async (credentials) => {
        const response = await authService.login(credentials);
        localStorage.setItem("library_token", response.accessToken);
        setUser(response.user);
        toast.success("Đăng nhập thành công.");
        return response.user;
      },
      logout: () => {
        localStorage.removeItem("library_token");
        setUser(null);
        toast.success("Đã đăng xuất.");
      },
    }),
    [loading, user]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
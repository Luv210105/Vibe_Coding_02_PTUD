import api from "./api";

export const authService = {
  login: async (payload) => (await api.post("/auth/login", payload)).data,
  me: async () => (await api.get("/auth/me")).data,
};
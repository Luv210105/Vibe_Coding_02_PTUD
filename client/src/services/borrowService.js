import api from "./api";

export const borrowService = {
  list: async (keyword = "") => (await api.get("/borrow-slips", { params: keyword ? { keyword } : {} })).data,
  borrow: async (payload) => (await api.post("/borrow-slips/borrow", payload)).data,
  returnBook: async (id, payload) => (await api.post(`/borrow-slips/return/${id}`, payload)).data,
};
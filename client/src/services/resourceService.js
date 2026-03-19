import api from "./api";

export const createResourceService = (endpoint) => ({
  list: async (keyword = "") => (await api.get(endpoint, { params: keyword ? { keyword } : {} })).data,
  create: async (payload) => (await api.post(endpoint, payload)).data,
  update: async (id, payload) => (await api.put(`${endpoint}/${id}`, payload)).data,
  remove: async (id) => (await api.delete(`${endpoint}/${id}`)).data,
});
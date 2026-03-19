import api from "./api";

export const reportService = {
  topBorrowedBooks: async (params) => (await api.get("/reports/top-borrowed-books", { params })).data,
  unreturnedReaders: async (params) => (await api.get("/reports/unreturned-readers", { params })).data,
};
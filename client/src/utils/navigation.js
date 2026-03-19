export const navigationItems = [
  { path: "/", label: "Tổng quan", roles: ["ADMIN", "LIBRARIAN"] },
  { path: "/readers", label: "Độc giả", roles: ["ADMIN", "LIBRARIAN"] },
  { path: "/categories", label: "Chuyên ngành", roles: ["ADMIN", "LIBRARIAN"] },
  { path: "/book-titles", label: "Đầu sách", roles: ["ADMIN", "LIBRARIAN"] },
  { path: "/book-copies", label: "Bản sao sách", roles: ["ADMIN", "LIBRARIAN"] },
  { path: "/borrow", label: "Mượn sách", roles: ["ADMIN", "LIBRARIAN"] },
  { path: "/return", label: "Trả sách", roles: ["ADMIN", "LIBRARIAN"] },
  { path: "/reports", label: "Báo cáo", roles: ["ADMIN", "LIBRARIAN"] },
  { path: "/users", label: "Người dùng hệ thống", roles: ["ADMIN"] },
];
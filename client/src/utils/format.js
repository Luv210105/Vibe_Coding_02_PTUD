export const formatDate = (value) => {
  if (!value) return "-";
  return new Date(value).toLocaleDateString("vi-VN");
};

export const statusLabels = {
  AVAILABLE: "Sẵn sàng",
  BORROWED: "Đang mượn",
  DAMAGED: "Hư hỏng",
  LOST: "Thất lạc",
  BORROWING: "Chưa trả",
  RETURNED: "Đã trả",
  LATE: "Trả trễ",
  ADMIN: "Quản trị viên",
  LIBRARIAN: "Thủ thư",
};
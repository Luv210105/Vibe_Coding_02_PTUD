import enum


class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    LIBRARIAN = "LIBRARIAN"


class BookCopyStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    BORROWED = "BORROWED"
    DAMAGED = "DAMAGED"
    LOST = "LOST"


class ReturnStatus(str, enum.Enum):
    BORROWING = "BORROWING"
    RETURNED = "RETURNED"
    LATE = "LATE"

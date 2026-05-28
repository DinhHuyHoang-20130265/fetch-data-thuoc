"""Trích đúng các cột như hiển thị trên UI congbothuoc/index.

Mỗi cột map tới một field trong JSON item (field chính nằm trong các nhóm
lồng nhau; field top-level cùng tên thường để trống). Thứ tự cột giống UI.
"""

# (Nhãn cột trên UI, đường dẫn field trong item JSON)
COLUMNS = [
    ("Số GPLH", ("soDangKy",)),
    ("Tên thuốc", ("tenThuoc",)),
    ("Hoạt chất", ("thongTinThuocCoBan", "hoatChatChinh")),
    ("Số quyết định", ("thongTinDangKyThuoc", "soQuyetDinh")),
    ("Dạng bào chế", ("thongTinThuocCoBan", "dangBaoChe")),
    ("Tên công ty đăng ký", ("congTyDangKy", "tenCongTyDangKy")),
    ("Tên công ty sản xuất", ("congTySanXuat", "tenCongTySanXuat")),
    ("Số đăng ký cũ", ("soDangKyCu",)),
]


def _get(item: dict, path) -> str:
    """Lấy giá trị theo đường dẫn lồng nhau; None/thiếu -> ''."""
    cur = item
    for key in path:
        if not isinstance(cur, dict):
            return ""
        cur = cur.get(key)
    return "" if cur is None else cur


def flatten_all(items):
    """Trả về (header, rows) chỉ gồm các cột UI, đúng thứ tự UI."""
    header = [label for label, _ in COLUMNS]
    rows = [[_get(it, path) for _, path in COLUMNS] for it in items]
    return header, rows

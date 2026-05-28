"""Điểm vào: lấy toàn bộ SĐK thuốc -> làm phẳng -> ghi đè vào Google Sheet.

Cấu hình qua biến môi trường (đặt trong GitHub Secrets):
  GOOGLE_SERVICE_ACCOUNT_JSON  nội dung file JSON của service account
  GOOGLE_SHEET_ID              ID của Google Sheet đích
  WORKSHEET_NAME               tên tab (mặc định: SoDangKy)
"""

import os
import sys

from dav_client import DavClient
from flatten import flatten_all
from sheets_writer import write_snapshot


def main() -> int:
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    sheet_id = os.environ.get("GOOGLE_SHEET_ID")
    worksheet_name = os.environ.get("WORKSHEET_NAME", "SoDangKy")

    if not sa_json or not sheet_id:
        print(
            "Thiếu GOOGLE_SERVICE_ACCOUNT_JSON hoặc GOOGLE_SHEET_ID.",
            file=sys.stderr,
        )
        return 1

    items = DavClient().fetch_all()
    if not items:
        print("Không có dữ liệu trả về từ API.", file=sys.stderr)
        return 1

    header, rows = flatten_all(items)
    print(f"[main] làm phẳng xong: {len(rows)} dòng, {len(header)} cột")

    write_snapshot(sa_json, sheet_id, worksheet_name, header, rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

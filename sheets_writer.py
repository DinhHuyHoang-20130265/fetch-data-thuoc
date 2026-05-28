"""Ghi snapshot vào Google Sheet (ghi đè toàn bộ mỗi lần chạy)."""

import json

import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
ROW_CHUNK = 5000  # số dòng ghi mỗi request, tránh vượt giới hạn body


def _client_from_json(sa_json: str) -> gspread.Client:
    info = json.loads(sa_json)
    creds = Credentials.from_service_account_info(info, scopes=SCOPES)
    return gspread.authorize(creds)


def _col_a1(n: int) -> str:
    """Chỉ số cột 1-based -> chữ cái A1 (1->A, 27->AA)."""
    letters = ""
    while n > 0:
        n, rem = divmod(n - 1, 26)
        letters = chr(65 + rem) + letters
    return letters


def write_snapshot(sa_json: str, sheet_id: str, worksheet_name: str,
                   header: list, rows: list) -> None:
    gc = _client_from_json(sa_json)
    spreadsheet = gc.open_by_key(sheet_id)

    n_rows = len(rows) + 1  # + header
    n_cols = max(len(header), 1)

    try:
        ws = spreadsheet.worksheet(worksheet_name)
        ws.clear()
        ws.resize(rows=n_rows, cols=n_cols)
    except gspread.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(
            title=worksheet_name, rows=n_rows, cols=n_cols
        )

    last_col = _col_a1(n_cols)

    # Header ở dòng 1.
    ws.update(range_name=f"A1:{last_col}1", values=[header],
              value_input_option="RAW")

    # Dữ liệu ghi theo từng chunk, bắt đầu từ dòng 2.
    for i in range(0, len(rows), ROW_CHUNK):
        chunk = rows[i:i + ROW_CHUNK]
        start = 2 + i
        end = start + len(chunk) - 1
        ws.update(range_name=f"A{start}:{last_col}{end}", values=chunk,
                  value_input_option="RAW")
        print(f"[sheets] đã ghi dòng {start}-{end}")

    print(f"[sheets] hoàn tất: {len(rows)} dòng x {n_cols} cột -> '{worksheet_name}'")

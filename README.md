# fetch-data-thuoc

Lấy toàn bộ số đăng ký thuốc đang kích hoạt từ API công khai của Cục Quản lý Dược
(`dichvucong.dav.gov.vn`), làm phẳng JSON và ghi đè snapshot vào một Google Sheet.
Chạy tự động hằng ngày bằng GitHub Actions.

Đây là bản chuyển đổi từ extension trình duyệt "API to Excel" sang job Python tự động.

## Cấu trúc

| File | Vai trò |
|------|---------|
| `dav_client.py` | Lấy cookie XSRF-TOKEN rồi phân trang toàn bộ SĐK kích hoạt |
| `flatten.py` | Trích đúng 8 cột như UI `congbothuoc/index`, nhãn tiếng Việt |
| `sheets_writer.py` | Ghi đè dữ liệu vào Google Sheet (theo chunk) |
| `main.py` | Điều phối: fetch → flatten → ghi sheet |
| `.github/workflows/daily.yml` | Lịch chạy hằng ngày + chạy tay |

## Thiết lập GitHub Secrets

Vào repo trên GitHub → **Settings → Secrets and variables → Actions → New repository secret**, tạo 2 secret:

| Tên secret | Giá trị |
|------------|---------|
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Dán **toàn bộ nội dung** file JSON key của service account |
| `GOOGLE_SHEET_ID` | ID của Google Sheet (phần giữa `/d/` và `/edit` trong URL) |

Sau đó **chia sẻ Google Sheet** cho email của service account (dạng
`...@...iam.gserviceaccount.com`) với quyền **Editor**, nếu chưa làm.

Tên tab đích mặc định là `SoDangKy` (đổi ở biến `WORKSHEET_NAME` trong workflow).

## Lịch chạy

Cron `0 21 * * *` = 04:00 sáng giờ Việt Nam mỗi ngày. Đổi trong
`.github/workflows/daily.yml` nếu cần. Có thể chạy thủ công bằng nút
**Run workflow** (workflow_dispatch) trên tab Actions.

## Chạy thử dưới máy

```bash
pip install -r requirements.txt
export GOOGLE_SERVICE_ACCOUNT_JSON="$(cat service-account.json)"
export GOOGLE_SHEET_ID="<sheet-id>"
python main.py
```

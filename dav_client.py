"""Client cho API công khai của Cục Quản lý Dược (dichvucong.dav.gov.vn).

Luồng xác thực giống extension: GET trang chủ để site cấp cookie XSRF-TOKEN,
sau đó POST kèm header x-xsrf-token. Không cần đăng nhập.
"""

import time
import requests

BASE_URL = "https://dichvucong.dav.gov.vn/"
API_URL = (
    "https://dichvucong.dav.gov.vn/api/services/app/soDangKy/"
    "GetAllPublicServerPaging"
)
PAGE_SIZE = 2000


class DavClient:
    def __init__(self, page_size: int = PAGE_SIZE, timeout: int = 90):
        self.page_size = page_size
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": "Mozilla/5.0 (compatible; dav-sync/1.0)",
            }
        )

    def _refresh_token(self) -> None:
        """GET trang chủ để nhận cookie XSRF-TOKEN, rồi gắn vào header."""
        self.session.get(BASE_URL, timeout=self.timeout)
        token = self.session.cookies.get("XSRF-TOKEN")
        if not token:
            raise RuntimeError("Không lấy được XSRF-TOKEN từ cookie.")
        self.session.headers["x-xsrf-token"] = token

    def _post_page(self, skip_count: int) -> dict:
        payload = {
            "filterText": "",
            "SoDangKyThuoc": {},
            "KichHoat": True,
            "skipCount": skip_count,
            "maxResultCount": self.page_size,
            "sorting": None,
        }
        resp = self.session.post(API_URL, json=payload, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()["result"]

    def fetch_all(self):
        """Lấy toàn bộ số đăng ký đang kích hoạt, trả về list các item dict."""
        self._refresh_token()

        first = self._post_page(0)
        total = first["totalCount"]
        items = list(first["items"])
        print(f"[dav] totalCount={total}, đã lấy {len(items)}/{total}")

        skip = self.page_size
        while skip < total:
            for attempt in range(3):
                try:
                    page = self._post_page(skip)
                    break
                except requests.RequestException as exc:
                    if attempt == 2:
                        raise
                    wait = 2 ** attempt
                    print(f"[dav] lỗi trang skip={skip}: {exc} -> thử lại sau {wait}s")
                    time.sleep(wait)
                    self._refresh_token()
            items.extend(page["items"])
            print(f"[dav] đã lấy {len(items)}/{total}")
            skip += self.page_size

        return items

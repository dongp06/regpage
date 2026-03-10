from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Dict

import requests

from .ui.gradient import gradient
from .ui.progress import ProgressBar
from .ui.spinner import LoadingSpinner


DEFAULT_API_BASE_URL = "https://minhdong.site/api/v1/facebook"


@dataclass
class Stats:
    total: int = 0
    success: int = 0
    failed: int = 0
    skipped: int = 0


class FacebookPageManager:
    def __init__(self, api_key: str) -> None:
        base_url = os.getenv("API_BASE_URL") or DEFAULT_API_BASE_URL
        self.client = requests.Session()
        self.client.headers.update(
            {
                "X-API-Key": api_key,
                "Content-Type": "application/json",
            }
        )
        self.base_url = base_url.rstrip("/")
        self.stats: Stats = Stats()

    def _post(self, path: str, json: Dict) -> Dict:
        resp = self.client.post(f"{self.base_url}{path}", json=json, timeout=60)
        resp.raise_for_status()
        return resp.json()

    def reg_and_transfer(self, quantity: int, config: Dict[str, str]) -> None:
        cookie_goc = config["cookieGoc"]
        pass_goc = config["passGoc"]
        uid_nhan = config["uidNhan"]
        cookie_nhan = config["cookieNhan"]

        print("\n" + gradient("+----------------------------------------------------------+"))
        print(gradient("|   REG & TRANSFER PAGE AUTOMATION                         |"))
        print(gradient("+----------------------------------------------------------+") + "\n")
        print(f"So luong Page can tao: {quantity}")
        print(f"UID nhan: {uid_nhan}\n")

        self.stats = Stats(total=quantity, success=0, failed=0, skipped=0)
        progress_bar = ProgressBar(quantity, "Tien trinh")

        for i in range(1, quantity + 1):
            print(f"\n{'=' * 60}")
            print(gradient(f"[{i}/{quantity}] Bat dau quy trinh..."))
            print("=" * 60)

            spinner1 = LoadingSpinner("Đang tạo Page mới")
            try:
                spinner1.start()
                time.sleep(1.0)
                reg_res = self._post(
                    "/page/create-cookie",
                    {
                        "cookie": cookie_goc,
                        "use_random_name": True,
                        "use_random_avatar": True,
                        "use_random_bio": True,
                    },
                )

                if not reg_res.get("success"):
                    spinner1.fail(
                        f"Tao Page that bai: {reg_res.get('error') or 'Loi khong xac dinh'}"
                    )
                    self.stats.failed += 1
                    progress_bar.update(i, "[FAIL]")
                    continue

                new_page = {
                    "profile_plus_id": reg_res.get("profile_plus_id"),
                    "name": reg_res.get("name"),
                    "page_cookie": f"{cookie_goc}; i_user={reg_res.get('profile_plus_id')}",
                }

                spinner1.succeed(f"Tao Page thanh cong: {new_page['name']}")
                print(f"   Page ID: {new_page['profile_plus_id']}")

                transfer_success = self._process_single_page(
                    new_page, pass_goc, uid_nhan, cookie_nhan
                )

                if transfer_success:
                    self.stats.success += 1
                    progress_bar.update(i, "[OK]")
                else:
                    self.stats.failed += 1
                    progress_bar.update(i, "[FAIL]")

                if i < quantity:
                    delay_time = 120_000
                    spinner2 = LoadingSpinner(
                        f"Cho {delay_time // 1000}s truoc khi tiep tuc"
                    )
                    spinner2.start()
                    self._delay(delay_time / 1000.0)
                    spinner2.info("Tiep tuc...")

            except Exception as exc:
                spinner1.stop()
                print(f"Loi nghiem trong tai buoc {i}:", exc)
                self.stats.failed += 1
                progress_bar.update(i, "[FAIL]")

        self._display_final_report()

    def _process_single_page(
        self,
        page: Dict[str, str],
        pass_goc: str,
        uid_nhan: str,
        cookie_nhan: str,
    ) -> bool:
        profile_plus_id = page["profile_plus_id"]
        name = page["name"]
        page_cookie = page["page_cookie"]

        try:
            print("\n  [1/3] Gui loi moi Admin...")
            spinner1 = LoadingSpinner("  Đang xử lý lời mời")
            spinner1.start()
            add_res = self._post(
                "/page/add-permission-cookie",
                {
                    "cookie": page_cookie,
                    "target_user_id": uid_nhan,
                    "password": pass_goc,
                },
            )
            if not add_res.get("success"):
                spinner1.fail(f"Loi gui loi moi: {add_res.get('error')}")
                return False
            invite_id = add_res.get("invite_id")
            spinner1.succeed(f"Gui loi moi thanh cong (ID: {invite_id})")

            print("  [2/3] Chap nhan loi moi...")
            spinner2 = LoadingSpinner("  Nick nhận đang xử lý")
            spinner2.start()
            accept_res = self._post(
                "/page/accept-invitation-cookie",
                {
                    "cookie": cookie_nhan,
                    "profile_admin_invite_id": invite_id,
                    "user_id": profile_plus_id,
                    "accept": True,
                },
            )
            if not accept_res.get("success"):
                spinner2.fail(f"Loi chap nhan: {accept_res.get('error')}")
                return False
            spinner2.succeed("Chap nhan loi moi thanh cong")

            uid_goc = self._extract_uid(page_cookie)
            print("  [3/3] Go quyen nick goc...")
            spinner3 = LoadingSpinner(f"  Đang gỡ admin {uid_goc}")
            spinner3.start()
            remove_res = self._post(
                "/page/remove-admin-cookie",
                {
                    "cookie": page_cookie,
                    "admin_id": uid_goc,
                    "password": pass_goc,
                    "profile_plus_id": profile_plus_id,
                },
            )
            if remove_res.get("success"):
                spinner3.succeed("Go quyen thanh cong")
                print(f"\n  Hoan tat ban giao: {name}")
                return True
            spinner3.fail(f"Loi go quyen: {remove_res.get('error')}")
            return False

        except Exception as exc:
            print("  Loi trong qua trinh transfer:", exc)
            return False

    def _display_final_report(self) -> None:
        print("\n\n" + gradient("+----------------------------------------------------------+"))
        print(gradient("|                    BAO CAO KET QUA                       |"))
        print(gradient("+----------------------------------------------------------+"))
        success_rate = (
            (self.stats.success / self.stats.total) * 100 if self.stats.total else 0.0
        )
        print("\nThong ke:")
        print(f"   Tong so: {self.stats.total}")
        print(f"   Thanh cong: {self.stats.success}")
        print(f"   That bai: {self.stats.failed}")
        print(f"   Ty le thanh cong: {success_rate:.1f}%")
        print(f"\nThoi gian hoan thanh: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    @staticmethod
    def _extract_uid(cookie: str) -> str | None:
        marker = "c_user="
        idx = cookie.find(marker)
        if idx == -1:
            return None
        start = idx + len(marker)
        end = cookie.find(";", start)
        return cookie[start:end] if end != -1 else cookie[start:]

    @staticmethod
    def _delay(seconds: float) -> None:
        time.sleep(seconds)


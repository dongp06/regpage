from __future__ import annotations

import getpass
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import dotenv_values

from .ui.gradient import gradient


ENV_KEYS = {
    "API_KEY": "API_KEY",
    "API_BASE_URL": "API_BASE_URL",
    "SOURCE_COOKIE": "SOURCE_COOKIE",
    "SOURCE_PASSWORD": "SOURCE_PASSWORD",
    "TARGET_UID": "TARGET_UID",
    "TARGET_COOKIE": "TARGET_COOKIE",
}


@dataclass
class AccountConfig:
    cookie: str
    password: Optional[str] = None  # not needed for target
    uid: Optional[str] = None       # only for target


@dataclass
class AppConfig:
    api_key: str
    source_account: AccountConfig
    target_account: AccountConfig


class InteractiveCLI:
    def __init__(self) -> None:
        self.env_path = Path(__file__).resolve().parent.parent / ".env"

    def question(self, prompt: str) -> str:
        return input(prompt)

    def prompt(self, message: str, default_value: str = "") -> str:
        suffix = f" [{default_value}]" if default_value else ""
        answer = input(f"{message}{suffix}: ")
        answer = answer.strip()
        return answer or default_value

    def prompt_number(self, message: str, default_value: int = 1) -> int:
        raw = self.prompt(message, str(default_value))
        try:
            return int(raw)
        except ValueError:
            return default_value

    def confirm(self, message: str) -> bool:
        answer = input(f"{message} (y/n): ").strip().lower()
        return answer in {"y", "yes"}

    def prompt_password(self, message: str) -> str:
        return getpass.getpass(f"{message}: ")

    def close(self) -> None:
        # nothing to close for Python's input()
        pass

    def display_header(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")
        print(gradient("+----------------------------------------------------------+"))
        print(gradient("|                                                            |"))
        print(gradient("|     FACEBOOK PAGE REG & TRANSFER MANAGER v2.0             |"))
        print(gradient("|     Tao va ban giao Page tu dong                         |"))
        print(gradient("|                                                            |"))
        print(gradient("+----------------------------------------------------------+") + "\n")

    def display_menu(self) -> None:
        print("\n" + gradient("+----------------------------------------------------------+"))
        print(gradient("|   MENU CHINH                                              |"))
        print(gradient("+----------------------------------------------------------+"))
        print("  1. Reg & Transfer Page")
        print("  2. Quan ly cau hinh")
        print("  3. Xem huong dan")
        print("  4. Xem thong ke (Coming soon)")
        print("  5. Thoat\n")

    def display_config_menu(self) -> None:
        print("\n" + gradient("+----------------------------------------------------------+"))
        print(gradient("|   QUAN LY CAU HINH (.env)                                 |"))
        print(gradient("+----------------------------------------------------------+"))
        print("  1. Tao config moi (luu vao .env)")
        print("  2. Tai lai config tu .env")
        print("  3. Xem config hien tai")
        print("  4. Luu config vao .env")
        print("  5. Quay lai\n")

    def load_config(self) -> Optional[AppConfig]:
        if not self.env_path.exists():
            return None
        data = dotenv_values(self.env_path)
        api_key = data.get("API_KEY")
        source_cookie = data.get("SOURCE_COOKIE")
        source_password = data.get("SOURCE_PASSWORD")
        target_uid = data.get("TARGET_UID")
        target_cookie = data.get("TARGET_COOKIE")
        if not all([api_key, source_cookie, source_password, target_uid, target_cookie]):
            return None
        return AppConfig(
            api_key=api_key,
            source_account=AccountConfig(cookie=source_cookie, password=source_password),
            target_account=AccountConfig(cookie=target_cookie, uid=target_uid),
        )

    def _escape_env_value(self, value: str | None) -> str:
        if value is None:
            return '""'
        s = str(value).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        return f'"{s}"'

    def save_config(self, config: AppConfig) -> bool:
        try:
            api_base_url = os.getenv("API_BASE_URL") or "https://minhdong.site/api/v1/facebook"
            lines = [
                "# Facebook Page Reg & Transfer - cau hinh",
                f'{ENV_KEYS["API_KEY"]}={self._escape_env_value(config.api_key)}',
                f'{ENV_KEYS["API_BASE_URL"]}={self._escape_env_value(api_base_url)}',
                f'{ENV_KEYS["SOURCE_COOKIE"]}={self._escape_env_value(config.source_account.cookie)}',
                f'{ENV_KEYS["SOURCE_PASSWORD"]}={self._escape_env_value(config.source_account.password or "")}',
                f'{ENV_KEYS["TARGET_UID"]}={self._escape_env_value(config.target_account.uid or "")}',
                f'{ENV_KEYS["TARGET_COOKIE"]}={self._escape_env_value(config.target_account.cookie)}',
            ]
            self.env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            return True
        except Exception as exc:  # pragma: no cover - defensive
            print("Loi khi luu .env:", exc)
            return False

    @staticmethod
    def _mask_sensitive_data(value: str, show_length: int = 10) -> str:
        if not value or len(value) <= show_length:
            return value
        return value[:show_length] + "..."

    def display_config(self, config: AppConfig) -> None:
        print("\n" + gradient("+----------------------------------------------------------+"))
        print(gradient("|   CAU HINH HIEN TAI                                      |"))
        print(gradient("+----------------------------------------------------------+"))
        print(f"\nAPI Key: {self._mask_sensitive_data(config.api_key)}")
        print("\nNick goc (Tao Page):")
        print(f"   Cookie: {self._mask_sensitive_data(config.source_account.cookie, 20)}")
        password = config.source_account.password or ""
        print(f"   Password: {'*' * len(password)}")
        print("\nNick nhan (Nhan Page):")
        print(f"   UID: {config.target_account.uid}")
        print(
            f"   Cookie: {self._mask_sensitive_data(config.target_account.cookie, 20)}\n"
        )


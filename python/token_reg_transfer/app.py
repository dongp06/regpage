from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from ..cli import InteractiveCLI, TokenConfig
from ..manager import ApiError, TokenPageManager
from ..ui.gradient import gradient
from ..ui.progress import ProgressBar
from ..ui.spinner import LoadingSpinner


@dataclass
class BatchStats:
    total: int = 0
    success: int = 0
    failed: int = 0


def _parse_profile_ids(raw: str) -> list[str]:
    # Accept comma/space/newline separated values.
    parts: list[str] = []
    for chunk in raw.replace("\n", ",").replace(" ", ",").split(","):
        v = chunk.strip()
        if v:
            parts.append(v)
    # de-dup while preserving order
    seen: set[str] = set()
    out: list[str] = []
    for pid in parts:
        if pid in seen:
            continue
        seen.add(pid)
        out.append(pid)
    return out


def _load_token_config_from_env(cli: InteractiveCLI) -> TokenConfig | None:
    cfg = cli.load_token_config()
    return cfg


def run_batch_transfer(cli: InteractiveCLI, cfg: TokenConfig) -> None:
    print("\n" + gradient("╔════════════════════════════════════════════════════════════╗"))
    print(gradient("║   REG & TRANSFER PAGE (TOKEN)                            ║"))
    print(gradient("╚════════════════════════════════════════════════════════════╝") + "\n")

    raw_ids = cli.prompt(
        "Nhap PROFILE_ID list (cach nhau boi dau phay/space/newline)"
    )
    profile_ids = _parse_profile_ids(raw_ids)
    if not profile_ids:
        print("Khong co PROFILE_ID nao. Huy.")
        cli.question("Nhan Enter de tiep tuc...")
        return

    do_accept = cli.confirm("Co tu dong Accept Invitation khong? (can INVITEE_UID)")
    do_remove = cli.confirm("Co Remove Admin sau khi accept khong?")
    remove_admin_id = ""
    if do_remove:
        remove_admin_id = cli.prompt(
            "Admin ID can remove (mac dinh = TARGET_UID)", cfg.target_uid
        )

    print("\n" + gradient("+----------------------------------------------------------+"))
    print(gradient("|   XAC NHAN (TOKEN)                                       |"))
    print(gradient("+----------------------------------------------------------+"))
    print(f"So luong PROFILE_ID: {len(profile_ids)}")
    print(f"Target UID: {cfg.target_uid}")
    if do_accept:
        print(f"Invitee UID: {cfg.invitee_uid or '(CHUA CO)'}")
    if do_remove:
        print(f"Remove admin_id: {remove_admin_id}")
    print()

    if not cli.confirm("Bat dau?"):
        print("Da huy!")
        cli.question("Nhan Enter de tiep tuc...")
        return

    mgr = TokenPageManager(cfg.api_key, cfg.base_url)
    stats = BatchStats(total=len(profile_ids))
    progress = ProgressBar(stats.total, "Tien trinh")

    for i, profile_id in enumerate(profile_ids, start=1):
        print(f"\n{'=' * 60}")
        print(gradient(f"[{i}/{stats.total}] PROFILE_ID={profile_id}"))
        print("=" * 60)

        spinner = LoadingSpinner("Dang transfer full access...")
        try:
            spinner.start()
            out1 = mgr.add_full_access(cfg.token, profile_id, cfg.target_uid, cfg.password)
            spinner.succeed("Transfer full access OK")
            print(json.dumps(out1, indent=2, ensure_ascii=False))

            if do_accept:
                if not cfg.invitee_uid:
                    print("Bo qua accept: chua co INVITEE_UID trong config.")
                else:
                    spinner2 = LoadingSpinner("Dang accept invitation...")
                    spinner2.start()
                    out2 = mgr.accept_invitation(
                        cfg.token, profile_id, cfg.invitee_uid, accept=True
                    )
                    spinner2.succeed("Accept OK")
                    print(json.dumps(out2, indent=2, ensure_ascii=False))

            if do_remove:
                spinner3 = LoadingSpinner("Dang remove admin...")
                spinner3.start()
                out3 = mgr.remove_admin(
                    cfg.token,
                    profile_id,
                    remove_admin_id or cfg.target_uid,
                    cfg.password,
                )
                spinner3.succeed("Remove admin OK")
                print(json.dumps(out3, indent=2, ensure_ascii=False))

            stats.success += 1
            progress.update(i, "[OK]")

        except ApiError as exc:
            spinner.fail(f"FAIL: {exc}")
            if exc.status:
                print(f"HTTP: {exc.status}")
            if exc.data:
                print("Response:", json.dumps(exc.data, indent=2, ensure_ascii=False))
            stats.failed += 1
            progress.update(i, "[FAIL]")
        except Exception as exc:
            spinner.fail(f"FAIL: {exc}")
            stats.failed += 1
            progress.update(i, "[FAIL]")

    print("\n" + gradient("+----------------------------------------------------------+"))
    print(gradient("|   BAO CAO (TOKEN)                                        |"))
    print(gradient("+----------------------------------------------------------+"))
    print(f"\nTong so: {stats.total}")
    print(f"Thanh cong: {stats.success}")
    print(f"That bai: {stats.failed}\n")
    cli.question("Nhan Enter de tiep tuc...")


def main() -> None:
    root_env = Path(__file__).resolve().parents[2] / ".env"
    if root_env.exists():
        load_dotenv(dotenv_path=root_env)

    cli = InteractiveCLI()
    try:
        cli.display_header()
        cfg = _load_token_config_from_env(cli)
        if not cfg:
            print("\nChua co token config trong .env.")
            print("Vui long chay `python -m python.index` -> menu Token -> Cau hinh Token (6).")
            cli.question("\nNhan Enter de thoat...")
            return

        run_batch_transfer(cli, cfg)
    except KeyboardInterrupt:
        print("\n\nDa huy bang Ctrl+C. Tam biet!\n")
    finally:
        cli.close()


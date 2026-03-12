from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from .cli import InteractiveCLI, AppConfig, AccountConfig, TokenConfig
from .manager import FacebookPageManager, TokenPageManager, ApiError
from .ui.gradient import gradient
from .ui.spinner import LoadingSpinner


def create_new_config(cli: InteractiveCLI) -> AppConfig:
    print("\n" + gradient("+----------------------------------------------------------+"))
    print(gradient("|   TAO CAU HINH MOI                                       |"))
    print(gradient("+----------------------------------------------------------+") + "\n")

    api_key = cli.prompt("API Key")

    print("\nThong tin nick GOC (tao Page):")
    cookie_goc = cli.prompt("   Cookie")
    pass_goc = cli.prompt_password("   Password")

    print("\nThong tin nick NHAN (nhan Page):")
    uid_nhan = cli.prompt("   UID")
    cookie_nhan = cli.prompt("   Cookie")

    config = AppConfig(
        api_key=api_key,
        source_account=AccountConfig(cookie=cookie_goc, password=pass_goc),
        target_account=AccountConfig(cookie=cookie_nhan, uid=uid_nhan),
    )

    save_now = cli.confirm("\nLuu config nay vao .env?")
    if save_now:
        if cli.save_config(config):
            print("Da luu config vao .env!")

    return config


def handle_reg_and_transfer(
    cli: InteractiveCLI, manager: FacebookPageManager, config: AppConfig
) -> None:
    print("\n" + gradient("╔════════════════════════════════════════════════════════════╗"))
    print(gradient("║   REG & TRANSFER PAGE                                    ║"))
    print(gradient("╚════════════════════════════════════════════════════════════╝") + "\n")

    quantity = cli.prompt_number("So luong Page can tao", 1)

    print("\n" + gradient("+----------------------------------------------------------+"))
    print(gradient("|   XAC NHAN                                               |"))
    print(gradient("+----------------------------------------------------------+"))
    print(f"Se tao: {quantity} Page")
    print(f"Ban giao cho UID: {config.target_account.uid}\n")

    confirmed = cli.confirm("Bat dau?")
    if not confirmed:
        print("Da huy!")
        cli.question("Nhan Enter de tiep tuc...")
        return

    manager.reg_and_transfer(
        quantity,
        {
            "cookieGoc": config.source_account.cookie,
            "passGoc": config.source_account.password or "",
            "uidNhan": config.target_account.uid or "",
            "cookieNhan": config.target_account.cookie,
        },
    )
    cli.question("\nNhan Enter de tiep tuc...")


def display_guide() -> None:
    print("\n" + gradient("+----------------------------------------------------------+"))
    print(gradient("|   HUONG DAN SU DUNG                                      |"))
    print(gradient("+----------------------------------------------------------+") + "\n")
    print("QUY TRINH HOAT DONG:\n")
    print("1. Tao Page moi voi ten/avatar/bio ngau nhien")
    print("2. Gui loi moi Admin cho nick nhan")
    print("3. Nick nhan tu dong chap nhan")
    print("4. Nick goc tu dong go quyen")
    print("5. Lap lai cho den khi du so luong\n")
    print("CAU HINH:\n")
    print("- Sao chep .env.example thanh .env va dien gia tri")
    print("- Hoac chon menu 2 de tao/luu config vao .env")
    print("- Co the sua truc tiep file .env\n")
    print("THOI GIAN:\n")
    print("- Moi Page mat khoang 10-15 giay")
    print("- Delay 120 giay giua moi lan tao")
    print("- Tao 10 Page khoang 20+ phut\n")
    print("LUU Y:\n")
    print("- Khong tat chuong trinh khi dang chay")
    print("- Kiem tra cookie con han")
    print("- Khong tao qua nhieu cung luc (khuyen nghi < 20)")


def handle_token_operations(
    cli: InteractiveCLI, token_config: TokenConfig | None
) -> TokenConfig | None:
    import json as _json

    config = token_config
    running = True

    while running:
        cli.display_token_menu()
        choice = cli.prompt("Chon chuc nang (1-7)", "7")

        if choice in ("1", "2", "3", "4", "5"):
            if not config:
                print("\nChua co cau hinh Token! Chon 6 de tao config truoc.")
                cli.question("Nhan Enter de tiep tuc...")
                continue

            mgr = TokenPageManager(config.api_key, config.base_url)
            spinner = LoadingSpinner("Dang xu ly...")

            try:
                spinner.start()
                result = None

                if choice == "1":
                    result = mgr.add_limited_access(
                        config.token, config.profile_id, config.target_uid, config.password
                    )
                    spinner.succeed("Add Limited Access thanh cong!")
                elif choice == "2":
                    result = mgr.add_full_access(
                        config.token, config.profile_id, config.target_uid, config.password
                    )
                    spinner.succeed("Add Full Access thanh cong!")
                elif choice == "3":
                    result = mgr.remove_admin(
                        config.token, config.profile_id, config.target_uid, config.password
                    )
                    spinner.succeed("Remove Admin thanh cong!")
                elif choice == "4":
                    if not config.invitee_uid:
                        spinner.stop()
                        print("Chua co INVITEE_UID! Cap nhat config truoc (menu 6).")
                        cli.question("Nhan Enter de tiep tuc...")
                        continue
                    result = mgr.accept_invitation(
                        config.token, config.profile_id, config.invitee_uid, accept=True
                    )
                    spinner.succeed("Accept Invitation thanh cong!")
                elif choice == "5":
                    if not config.invitee_uid:
                        spinner.stop()
                        print("Chua co INVITEE_UID! Cap nhat config truoc (menu 6).")
                        cli.question("Nhan Enter de tiep tuc...")
                        continue
                    result = mgr.accept_invitation(
                        config.token, config.profile_id, config.invitee_uid, accept=False
                    )
                    spinner.succeed("Decline Invitation thanh cong!")

                if result is not None:
                    print("\nKet qua:")
                    print(_json.dumps(result, indent=2, ensure_ascii=False))

            except ApiError as exc:
                spinner.fail(f"Loi: {exc}")
                if exc.status:
                    print(f"  HTTP Status: {exc.status}")
                if exc.data:
                    print(f"  Response: {_json.dumps(exc.data, indent=2, ensure_ascii=False)}")
            except Exception as exc:
                spinner.fail(f"Loi: {exc}")

            cli.question("\nNhan Enter de tiep tuc...")

        elif choice == "6":
            config = handle_token_config_management(cli, config)
        elif choice == "7":
            running = False
        else:
            print("Lua chon khong hop le!")

    return config


def handle_token_config_management(
    cli: InteractiveCLI, current_config: TokenConfig | None
) -> TokenConfig | None:
    config = current_config
    managing = True
    while managing:
        cli.display_token_config_menu()
        choice = cli.prompt("Chon chuc nang (1-5)", "1")
        if choice == "1":
            config = create_new_token_config(cli)
        elif choice == "2":
            loaded = cli.load_token_config()
            if loaded:
                config = loaded
                print("Da tai lai token config tu .env thanh cong!")
            else:
                print(
                    "Thieu bien trong .env (API_KEY, TOKEN, PROFILE_ID, TARGET_UID, PASSWORD). "
                    "Kiem tra .env.example."
                )
            cli.question("Nhan Enter de tiep tuc...")
        elif choice == "3":
            if config:
                cli.display_token_config(config)
            else:
                print("\nChua co token config!")
            cli.question("Nhan Enter de tiep tuc...")
        elif choice == "4":
            if config:
                if cli.save_token_config(config):
                    print("Da luu token config vao .env")
            else:
                print("\nChua co token config de luu!")
            cli.question("Nhan Enter de tiep tuc...")
        elif choice == "5":
            managing = False
        else:
            print("Lua chon khong hop le!")
    return config


def create_new_token_config(cli: InteractiveCLI) -> TokenConfig:
    print("\n" + gradient("+----------------------------------------------------------+"))
    print(gradient("|   TAO CAU HINH TOKEN MOI                                 |"))
    print(gradient("+----------------------------------------------------------+") + "\n")

    api_key = cli.prompt("API Key")
    base_url = cli.prompt("Base URL", "https://minhdong.site")
    token = cli.prompt("Token (Facebook)")
    profile_id = cli.prompt("Profile ID (Page)")
    target_uid = cli.prompt("Target UID")
    password = cli.prompt("Password")
    invitee_uid = cli.prompt("Invitee UID (cho accept/decline, Enter de bo qua)", "")

    config = TokenConfig(
        api_key=api_key,
        base_url=base_url,
        token=token,
        profile_id=profile_id,
        target_uid=target_uid,
        password=password,
        invitee_uid=invitee_uid,
    )

    save_now = cli.confirm("\nLuu config nay vao .env?")
    if save_now:
        if cli.save_token_config(config):
            print("Da luu token config vao .env!")

    return config


def handle_config_management(
    cli: InteractiveCLI, current_config: AppConfig | None
) -> AppConfig | None:
    config = current_config
    managing = True
    while managing:
        cli.display_config_menu()
        choice = cli.prompt("Chon chuc nang (1-5)", "1")
        if choice == "1":
            config = create_new_config(cli)
        elif choice == "2":
            loaded = cli.load_config()
            if loaded:
                config = loaded
                print("Da tai lai config tu .env thanh cong!")
            else:
                print(
                    "Thieu bien trong .env (API_KEY, SOURCE_*, TARGET_*). "
                    "Kiem tra .env.example."
                )
            cli.question("Nhan Enter de tiep tuc...")
        elif choice == "3":
            if config:
                cli.display_config(config)
            else:
                print("\nChua co config!")
            cli.question("Nhan Enter de tiep tuc...")
        elif choice == "4":
            if config:
                if cli.save_config(config):
                    print("Da luu config vao .env")
            else:
                print("\nChua co config de luu!")
            cli.question("Nhan Enter de tiep tuc...")
        elif choice == "5":
            managing = False
        else:
            print("Lua chon khong hop le!")
    return config


def main() -> None:
    root_env = Path(__file__).resolve().parent.parent / ".env"
    if root_env.exists():
        load_dotenv(dotenv_path=root_env)

    cli = InteractiveCLI()
    config: AppConfig | None = None
    manager: FacebookPageManager | None = None
    token_config: TokenConfig | None = None

    try:
        try:
            cli.display_header()

            spinner = LoadingSpinner("Đang kiểm tra config")
            spinner.start()
            import time as _time

            _time.sleep(0.5)
            config = cli.load_config()
            token_config = cli.load_token_config()

            if config:
                spinner.succeed("Đã tải config từ file .env")
                manager = FacebookPageManager(config.api_key)
            else:
                spinner.info("Chua co config, can tao moi")

            running = True
            while running:
                cli.display_menu()
                choice = cli.prompt("Chon chuc nang (1-6)", "1")
                if choice == "1":
                    if not config:
                        print("\nChua co cau hinh Cookie! Vui long tao config truoc (menu 4).")
                        cli.question("Nhan Enter de tiep tuc...")
                        continue
                    if not manager:
                        manager = FacebookPageManager(config.api_key)
                    handle_reg_and_transfer(cli, manager, config)
                elif choice == "2":
                    token_config = handle_token_operations(cli, token_config)
                elif choice == "3":
                    if not token_config:
                        print("\nChua co cau hinh Token! Vui long tao config truoc (menu 2 -> 6).")
                        cli.question("Nhan Enter de tiep tuc...")
                        continue
                    from .token_reg_transfer.app import run_batch_transfer

                    run_batch_transfer(cli, token_config)
                elif choice == "4":
                    config = handle_config_management(cli, config)
                    if config:
                        manager = FacebookPageManager(config.api_key)
                elif choice == "5":
                    display_guide()
                    cli.question("\nNhan Enter de tiep tuc...")
                elif choice == "6":
                    running = False
                    print("\nCam on ban da su dung! Tam biet!\n")
                else:
                    print("Lua chon khong hop le!")
        except KeyboardInterrupt:
            print("\n\nDa huy bang Ctrl+C. Tam biet!\n")
    finally:
        cli.close()


if __name__ == "__main__":
    main()

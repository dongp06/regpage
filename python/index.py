from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from .cli import InteractiveCLI, AppConfig, AccountConfig
from .manager import FacebookPageManager
from .ui.gradient import gradient


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
    # load .env from project root so API_BASE_URL etc. are visible
    root_env = Path(__file__).resolve().parent.parent / ".env"
    if root_env.exists():
        load_dotenv(dotenv_path=root_env)

    cli = InteractiveCLI()
    config: AppConfig | None = None
    manager: FacebookPageManager | None = None

    try:
        try:
            cli.display_header()
            from .ui.spinner import LoadingSpinner

            spinner = LoadingSpinner("Đang kiểm tra config")
            spinner.start()
            import time as _time

            _time.sleep(0.5)
            config = cli.load_config()
            if config:
                spinner.succeed("Đã tải config từ file .env")
                manager = FacebookPageManager(config.api_key)
            else:
                spinner.info("Chua co config, can tao moi")

            running = True
            while running:
                cli.display_menu()
                choice = cli.prompt("Chon chuc nang (1-5)", "1")
                if choice == "1":
                    if not config:
                        print("\nChua co cau hinh! Vui long tao config truoc.")
                        cli.question("Nhan Enter de tiep tuc...")
                        continue
                    if not manager:
                        manager = FacebookPageManager(config.api_key)
                    handle_reg_and_transfer(cli, manager, config)
                elif choice == "2":
                    config = handle_config_management(cli, config)
                    if config:
                        manager = FacebookPageManager(config.api_key)
                elif choice == "3":
                    display_guide()
                    cli.question("\nNhan Enter de tiep tuc...")
                elif choice == "4":
                    print("\nTinh nang dang phat trien...\n")
                    cli.question("Nhan Enter de tiep tuc...")
                elif choice == "5":
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


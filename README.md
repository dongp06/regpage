# Facebook Page Reg & Transfer Manager

CLI tương tác để **tạo** và **bàn giao** Facebook Page tự động (tạo Page → mời Admin → chấp nhận → gỡ quyền nick gốc).

## Yêu cầu

- **Node.js** >= 14.0.0
- Tài khoản Facebook (nick gốc tạo Page, nick nhận nhận Page)
- API Key từ dịch vụ hỗ trợ (ví dụ: minhdong.site)

## Cài đặt

```bash
npm install
```

## Cấu hình (.env)

Ứng dụng đọc cấu hình **hoàn toàn từ file `.env`** (không dùng config.json).

1. Sao chép file mẫu:

```bash
cp .env.example .env
```

2. Mở `.env` và điền giá trị:

| Biến | Mô tả |
|------|--------|
| `API_KEY` | API key từ nhà cung cấp (bắt buộc) |
| `API_BASE_URL` | URL API (mặc định: `https://minhdong.site/api/v1/facebook`) |
| `SOURCE_COOKIE` | Cookie nick gốc (dùng để tạo Page) |
| `SOURCE_PASSWORD` | Mật khẩu nick gốc |
| `TARGET_UID` | UID nick nhận Page |
| `TARGET_COOKIE` | Cookie nick nhận |

Có thể tạo/sửa config qua menu **2. Quản lý cấu hình** trong CLI (giá trị sẽ được ghi vào `.env`).

## Chạy chương trình

```bash
npm start
```

Hoặc:

```bash
node app/index.js
```

## Menu chính

| Số | Chức năng |
|----|-----------|
| 1 | Reg & Transfer Page – Tạo và bàn giao Page theo số lượng |
| 2 | Quản lý cấu hình – Tạo/load/xem/lưu config vào .env |
| 3 | Xem hướng dẫn |
| 4 | Xem thống kê (Coming soon) |
| 5 | Thoát |

## Quy trình hoạt động

1. Tạo Page mới với tên/avatar/bio ngẫu nhiên.
2. Gửi lời mời Admin cho nick nhận.
3. Nick nhận tự động chấp nhận.
4. Nick gốc tự động gỡ quyền (chỉ còn nick nhận làm Admin).
5. Lặp lại cho đến đủ số lượng (có delay 120s giữa mỗi Page).

## Lưu ý

- Không tắt chương trình khi đang chạy (đặc biệt lúc đang tạo/bàn giao).
- Kiểm tra cookie còn hạn trước khi chạy.
- Không nên tạo quá nhiều Page cùng lúc (khuyến nghị < 20).
- Mỗi Page khoảng 10–15 giây; delay 120 giây giữa mỗi lần tạo.

## Cấu trúc thư mục

```
regpage/
├── app/
│   ├── index.js      # Entry, load dotenv
│   ├── app.js        # Logic menu & flow chính
│   ├── cli.js        # Interactive CLI, đọc/ghi .env
│   ├── manager.js    # Gọi API Facebook
│   └── ui/
│       ├── gradient.js
│       ├── progress.js
│       └── spinner.js
├── .env              # Cấu hình (không commit)
├── .env.example      # Mẫu biến môi trường
├── package.json
└── README.md
```

## Bảo mật

- **Không commit** file `.env` lên Git (chứa cookie, mật khẩu, API key).
- File `.env` đã được thêm vào `.gitignore`.

## License

MIT

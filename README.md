# Facebook Page Reg & Transfer Manager (Python)

CLI tương tác để:

- **Reg & Transfer (Cookie)**: tạo Page → mời admin → nick nhận chấp nhận → gỡ quyền nick gốc.
- **Admin permissions (Token)**: add/remove/accept/decline quyền admin theo từng action.
- **Reg & Transfer (Token) [Batch]**: chạy batch theo danh sách `PROFILE_ID` (folder riêng).

> Repo vẫn còn bản NodeJS cũ trong `app/` (xem mục **NodeJS (legacy)**).

## Docs

Xem docs riêng tại `docs/README.md`.

## Yêu cầu

- **Python**: 3.10+ (khuyến nghị 3.11/3.12)
- **API_KEY** từ dịch vụ backend bạn đang dùng (ví dụ: `minhdong.site`)
- Tài khoản Facebook / cookie / token tuỳ chế độ bạn chạy

## Cài đặt (Python)

Tại thư mục project:

```bash
cd d:/regpage
pip install -r python/requirements.txt
```

## Cấu hình `.env`

Tool đọc cấu hình từ file `.env` ở **gốc project** (`d:/regpage/.env`).

Tạo `.env` từ mẫu:

```bash
cd d:/regpage
cp .env.example .env
```

### Biến cho chế độ Cookie (Reg & Transfer Page)

| Biến | Bắt buộc | Mô tả |
|------|----------|------|
| `API_KEY` | ✅ | API key |
| `API_BASE_URL` | ❌ | Base URL cookie API (mặc định: `https://minhdong.site/api/v1/facebook`) |
| `SOURCE_COOKIE` | ✅ | Cookie nick gốc (tạo Page) |
| `SOURCE_PASSWORD` | ✅ | Password nick gốc |
| `TARGET_UID` | ✅ | UID nick nhận |
| `TARGET_COOKIE` | ✅ | Cookie nick nhận |

### Biến cho chế độ Token (Admin permissions / Batch)

| Biến | Bắt buộc | Mô tả |
|------|----------|------|
| `API_KEY` | ✅ | API key |
| `BASE_URL` | ✅ | Base host cho token API (vd: `https://minhdong.site`) |
| `TOKEN` | ✅ | Facebook token |
| `PROFILE_ID` | ✅ (tool action đơn) | Profile/Page ID dùng cho menu Token action (một lần) |
| `TARGET_UID` | ✅ | UID target (admin_id) |
| `PASSWORD` | ✅ | Password (backend yêu cầu để add/remove admin) |
| `INVITEE_UID` | ❌ | UID người được mời (dùng accept/decline) |

> **Batch Token**: tool sẽ hỏi bạn nhập **danh sách `PROFILE_ID` khi chạy**, không đọc list từ `.env`.

## Chạy chương trình (Python)

### Cách 1: Chạy tool tổng (khuyến nghị)

```bash
cd d:/regpage
python -m python.index
```

Menu chính (Python):

| Số | Chức năng |
|----|-----------|
| 1 | Reg & Transfer Page (Cookie) |
| 2 | Quản lý quyền Admin (Token) |
| 3 | Reg & Transfer Page (Token) [Batch] |
| 4 | Quản lý cấu hình Cookie (`.env`) |
| 5 | Xem hướng dẫn |
| 6 | Thoát |

### Cách 2: Chạy Batch Token bằng folder riêng

```bash
cd d:/regpage
python -m python.token_reg_transfer
```

Batch sẽ:

- chạy `transfer_full` cho từng `PROFILE_ID`
- tuỳ chọn `accept_invitation`
- tuỳ chọn `remove_admin`
- in JSON response + báo cáo OK/FAIL

## Token actions tương đương code demo JS

Trong menu **2. Quản lý quyền Admin (Token)**, các action map như sau:

- `Add Limited Access Admin` → `POST /api/v1/facebook/page/transfer` (`admin_type=limited_access`)
- `Add Full Access Admin` → `POST /api/v1/facebook/page/transfer_full`
- `Remove Admin` → `POST /api/v1/facebook/page/remove_admin` (`admin_type=full_access`)
- `Accept/Decline Invitation` → `POST /api/v1/facebook/page/accept_invitation` (`accept=true/false`)

## Troubleshooting

### `KeyboardInterrupt` / bấm Ctrl+C

- Bản Python đã bắt `KeyboardInterrupt` để **thoát gọn**, không in traceback.

### Thiếu biến môi trường / load config bị null

- Kiểm tra `.env` có đủ các biến theo chế độ bạn chạy.
- `python.index` có menu để tạo/lưu config vào `.env`:
  - Cookie config: **menu 4**
  - Token config: vào **menu 2 → 6**

### Lỗi HTTP từ backend

- Tool sẽ in:
  - **HTTP status**
  - **response JSON** (field `error`/`message` nếu có)
- Kiểm tra `API_KEY`, `BASE_URL`/`API_BASE_URL`, token/cookie còn sống.

## Cấu trúc thư mục (Python)

```
regpage/
├── python/
│   ├── index.py                  # Tool tổng (menu chính)
│   ├── cli.py                    # CLI + đọc/ghi .env
│   ├── manager.py                # Cookie manager + Token manager
│   ├── ui/                       # gradient/spinner/progress
│   └── token_reg_transfer/       # Folder riêng: batch token reg&transfer
│       ├── __main__.py
│       └── app.py
├── .env
├── .env.example
└── README.md
```

## NodeJS (legacy)

Nếu bạn vẫn muốn chạy bản NodeJS cũ:

```bash
npm install
npm start
```

Entry: `app/index.js`

## Bảo mật

- **Không commit** file `.env` (chứa cookie/token/password/API key).
- Repo đã ignore `.env` trong `.gitignore`.

## License

MIT

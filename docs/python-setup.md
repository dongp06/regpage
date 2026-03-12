# Cài đặt & cấu hình (Python)

## Yêu cầu

- Python 3.10+ (khuyến nghị 3.11/3.12)
- `API_KEY` từ backend bạn dùng

## Cài dependency

Tại thư mục project:

```bash
cd d:/regpage
pip install -r python/requirements.txt
```

## Tạo file `.env`

Tool đọc `.env` ở **gốc project**: `d:/regpage/.env`.

Tạo từ mẫu:

```bash
cd d:/regpage
cp .env.example .env
```

> Nếu bạn dùng PowerShell/CMD, có thể tự copy file thủ công trong Explorer (copy `.env.example` → rename thành `.env`).

## Biến môi trường

### Cookie mode (Reg & Transfer Page)

| Biến | Bắt buộc | Mô tả |
|------|----------|------|
| `API_KEY` | ✅ | API key |
| `API_BASE_URL` | ❌ | Base URL cookie API (mặc định: `https://minhdong.site/api/v1/facebook`) |
| `SOURCE_COOKIE` | ✅ | Cookie nick gốc |
| `SOURCE_PASSWORD` | ✅ | Password nick gốc |
| `TARGET_UID` | ✅ | UID nick nhận |
| `TARGET_COOKIE` | ✅ | Cookie nick nhận |

### Token mode (Admin permissions / Batch)

| Biến | Bắt buộc | Mô tả |
|------|----------|------|
| `API_KEY` | ✅ | API key |
| `BASE_URL` | ✅ | Base host token API (vd: `https://minhdong.site`) |
| `TOKEN` | ✅ | Facebook token |
| `PROFILE_ID` | ✅ (tool action đơn) | Profile/Page ID |
| `TARGET_UID` | ✅ | UID target (admin_id) |
| `PASSWORD` | ✅ | Password dùng cho add/remove |
| `INVITEE_UID` | ❌ | UID người được mời (accept/decline) |


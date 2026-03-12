# Reg & Transfer Page (Cookie)

## Mục tiêu

Tự động tạo Page và bàn giao quyền admin cho nick nhận:

1. Tạo Page mới (random name/avatar/bio)
2. Gửi lời mời admin
3. Nick nhận chấp nhận
4. Gỡ quyền admin nick gốc

## Chạy

Trong tool tổng:

```bash
cd d:/regpage
python -m python.index
```

Chọn menu **1**.

## Cấu hình cần có

Xem danh sách biến trong [Cài đặt & cấu hình](./python-setup.md).

Tối thiểu cần:

- `API_KEY`
- `SOURCE_COOKIE`
- `SOURCE_PASSWORD`
- `TARGET_UID`
- `TARGET_COOKIE`

## Lưu ý

- Không nên tạo quá nhiều cùng lúc (khuyến nghị < 20)
- Có delay 120s giữa mỗi Page
- Cookie hết hạn sẽ gây lỗi từ backend


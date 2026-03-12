# Reg & Transfer Page (Token) [Batch]

Tool này phù hợp khi bạn có **nhiều `PROFILE_ID`** và muốn chạy tự động theo danh sách.

## Chạy (2 cách)

### Cách 1: Trong tool tổng

```bash
cd d:/regpage
python -m python.index
```

Chọn menu **3**.

### Cách 2: Chạy module riêng (folder riêng)

```bash
cd d:/regpage
python -m python.token_reg_transfer
```

## Cách nhập danh sách `PROFILE_ID`

Tool sẽ hỏi bạn nhập danh sách `PROFILE_ID` theo dạng:

- cách nhau bởi dấu phẩy: `123,456,789`
- hoặc space
- hoặc xuống dòng

Tool sẽ tự remove trùng.

## Flow batch

Mỗi `PROFILE_ID`:

1. `transfer_full` (add full access admin cho `TARGET_UID`)
2. (tuỳ chọn) `accept_invitation` (cần `INVITEE_UID`)
3. (tuỳ chọn) `remove_admin` (mặc định remove `TARGET_UID`, có thể nhập admin_id khác)

## Cấu hình cần có

Xem [Cài đặt & cấu hình](./python-setup.md) (phần Token mode).


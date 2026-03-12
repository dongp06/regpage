# Admin permissions (Token)

## Chạy

```bash
cd d:/regpage
python -m python.index
```

Chọn menu **2**.

## Các action

Các action tương đương code demo JS:

- **Add Limited Access Admin**
  - `POST /api/v1/facebook/page/transfer`
  - body gồm `token`, `profile_id`, `admin_id`, `password`, `admin_type=limited_access`
- **Add Full Access Admin**
  - `POST /api/v1/facebook/page/transfer_full`
  - body gồm `token`, `profile_id`, `admin_id`, `password`
- **Remove Admin**
  - `POST /api/v1/facebook/page/remove_admin`
  - body gồm `token`, `profile_id`, `admin_id`, `password`, `admin_type=full_access`
- **Accept / Decline Invitation**
  - `POST /api/v1/facebook/page/accept_invitation`
  - body gồm `token`, `profile_id`, `invitee_id`, `accept=true/false`

## Cấu hình cần có

Xem [Cài đặt & cấu hình](./python-setup.md) (phần Token mode).


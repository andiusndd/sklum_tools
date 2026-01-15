# Hướng Dẫn Quản Trị Hệ Thống License (Admin Guide)

Đây là hướng dẫn dành cho Admin (Bạn) để quản lý key bản quyền trên Supabase.

## 1. Truy cập Database
1.  Truy cập: [supabase.com](https://supabase.com/dashboard)
2.  Chọn project `sklum-license-db`.
3.  Ở thanh bên trái, chọn **Table Editor** (icon hình bảng tính/spreadsheet).
4.  Chọn bảng `licenses`.

## 2. Tạo License Mới (Cấp Key cho khách)
Khi có khách mua hàng, bạn cần tạo key cho họ.

**Cách làm thủ công:**
1.  Trong bảng `licenses`, bấm **Insert New Row** (hoặc nút "Insert").
2.  Điền thông tin:
    *   `key`: Nhập mã bản quyền (ví dụ: `SKLUM-DUONG-001`). *Nên random chuỗi dài để bảo mật.*
    *   `status`: Mặc định là `active` (không cần sửa).
    *   `hwid`: **ĐỂ TRỐNG** (NULL). *Khách hàng sẽ tự điền vào đây khi họ kích hoạt lần đầu.*
    *   `email`: (Tùy chọn) Email khách hàng để dễ quản lý.
3.  Bấm **Save**.

**Kết quả:** Key `SKLUM-DUONG-001` đã sẵn sàng sử dụng.

## 3. Reset License (Mở khóa máy)
Khi khách đổi máy tính hoặc cài lại Win, họ sẽ bị lỗi "Key locked to another machine". Bạn cần reset cho họ.

**Cách làm:**
1.  Tìm dòng chứa Key của khách (dùng Search hoặc Filter).
2.  Nhìn cột `hwid`.
3.  **Xóa nội dung ô `hwid`** (set về NULL hoặc Empty).
4.  Bấm **Save**.

**Kết quả:** Key trở về trạng thái như mới. Khách nhập lại trên máy mới sẽ thành công (và key sẽ lock vào máy mới đó).

## 4. Khóa License (Ban Key)
Nếu phát hiện khách share key trái phép hoặc refund.

**Cách làm:**
1.  Tìm dòng chứa Key đó.
2.  Sửa cột `status` từ `active` thành `banned`.
3.  Bấm **Save**.

**Kết quả:** Khách không thể kích hoạt được nữa.

## 5. (Nâng Cao) Tự động hóa qua API
Sau này nếu bán nhiều, bạn không thể add thủ công. Bạn có thể dùng Zapier/n8n kết nối với Webhook của Gumroad/SePay.
*   Khi có đơn hàng mới -> Gọi API vào Supabase -> Insert dòng mới.
*   *(Tính năng này thuộc về Roadmap tương lai)*

---
**Mẹo:** Bạn có thể chạy lệnh SQL để tạo nhanh nhiều key:
```sql
INSERT INTO licenses (key) VALUES 
('KEY-001'),
('KEY-002'),
('KEY-003');
```
Vào mục **SQL Editor** để chạy lệnh này.

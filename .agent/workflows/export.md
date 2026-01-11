---
description: Export addon package with version-named folder
---

# /export Command Workflow

Khi nhận được `/export` hoặc `@[/export]`, Agent sẽ thực hiện quy trình đóng gói addon.

## Quy trình xử lý

// turbo-all

0.  **Pre-flight Check**:
    Khuyến nghị hoặc tự động chạy `/test` để đảm bảo code không có lỗi cú pháp trước khi đóng gói.
    `> Verifying codebase with /test...`

1.  **Đọc phiên bản hiện tại**: Lấy version từ `bl_info["version"]` trong `__init__.py`.

2.  **Tạo Python script export**: Tạo file `_export_addon.py` tạm thời để thực hiện export.

3.  **Script sẽ thực hiện**:
    - Tạo thư mục tạm `SKLUMToolz_temp/SKLUMToolz/` 
    - **QUAN TRỌNG**: Blender sử dụng tên thư mục làm tên module Python. Thư mục bên trong ZIP phải là `SKLUMToolz`.
    - **TỰ ĐỘNG PHÁT HIỆN** và copy:
        - Tất cả file `.py` và `.md` ở root
        - Thư mục `core/`
        - Tất cả thư mục bắt đầu với `panel_*`
        - File `README.md`, `STRUCTURE.md`, `update-log.md`
    - **Không cần cập nhật script** khi thêm panel mới!
    - Loại trừ các file không cần thiết:
        - `.git/`, `.gemini/`, `.agent/`
        - `__pycache__/`, `*.pyc`
        - `dataIDP.json` (cache)
        - `presets.json` (user data)
    - Nén thành file ZIP: `SKLUMToolz_v{major}.{minor}.{patch}.zip`
    - Dọn dẹp thư mục tạm

4.  **Chạy script**: `python _export_addon.py`

5.  **Dọn dẹp**: Xóa file `_export_addon.py` sau khi hoàn thành.

6.  **Báo cáo kết quả**: Thông báo đường dẫn file ZIP.

## Ví dụ sử dụng

```
/export
```

Kết quả: 
- File ZIP: `SKLUMToolz_v2.6.5.zip` (trong thư mục hiện tại)
- Bên trong ZIP: thư mục `SKLUMToolz/` (sẵn sàng cài đặt vào Blender)
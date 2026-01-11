---
description: Export addon package with version-named folder
---

# /export Command Workflow

Khi nhận được `/export` hoặc `@[/export]`, Agent sẽ thực hiện quy trình đóng gói addon.

## Quy trình xử lý

// turbo-all

1.  **Đọc phiên bản hiện tại**: Lấy version từ `bl_info["version"]` trong `__init__.py`.

2.  **Tạo thư mục export**:
    - Đường dẫn: `../SKLUMToolz_v{major}.{minor}.{patch}/`
    - Ví dụ: `SKLUMToolz_v2.5.5/`

3.  **Copy các file/thư mục cần thiết**:
    - `__init__.py`
    - `README.md`
    - `STRUCTURE.md`
    - `UPDATE-LOG.md`
    - `core/`
    - `panel_checker_tools/`
    - `panel_import_export/`
    - `panel_jpg_converter/`
    - `panel_auto_rename/`

4.  **Loại trừ các file không cần thiết**:
    - `.git/`
    - `.gemini/`
    - `.agent/`
    - `__pycache__/`
    - `*.pyc`
    - `dataIDP.json` (cache)
    - `presets.json` (user data)

5.  **Nén thành file ZIP**:
    - Tạo file `SKLUMToolz_v{major}.{minor}.{patch}.zip`
    - Sử dụng PowerShell: `Compress-Archive -Path "SKLUMToolz_v*" -DestinationPath "SKLUMToolz_v*.zip"`

6.  **Báo cáo kết quả**: Thông báo đường dẫn thư mục và file zip đã tạo.

## Ví dụ sử dụng

```
/export
```

Kết quả: 
- Thư mục: `../SKLUMToolz_v2.5.5/`
- File ZIP: `../SKLUMToolz_v2.5.5.zip` (sẵn sàng upload)

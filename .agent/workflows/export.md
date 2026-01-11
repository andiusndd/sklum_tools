---
description: Export addon package with version-named folder
---

# /export Command Workflow

Khi nhận được `/export` hoặc `@[/export]`, Agent sẽ thực hiện quy trình đóng gói addon.

## Quy trình xử lý

// turbo-all

1.  **Đọc phiên bản hiện tại**: Lấy version từ `bl_info["version"]` trong `__init__.py`.

2.  **Tạo thư mục export**:
    - Tạo thư mục tạm: `../SKLUMToolz/` (KHÔNG có version trong tên thư mục!)
    - **QUAN TRỌNG**: Blender sử dụng tên thư mục làm tên module Python. Nếu thư mục có tên khác `SKLUMToolz`, addon sẽ báo lỗi "No module named".

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
    - Tên file ZIP CÓ VERSION: `SKLUMToolz_v{major}.{minor}.{patch}.zip`
    - Bên trong ZIP chứa thư mục `SKLUMTool/` (KHÔNG có version)

6.  **Dọn dẹp**: Xóa thư mục tạm `../SKLUMTool/` sau khi nén xong.

7.  **Báo cáo kết quả**: Thông báo đường dẫn file ZIP.

## Ví dụ sử dụng

```
/export
```

Kết quả: 
- File ZIP: `../SKLUMToolz_v2.5.5.zip`
- Bên trong ZIP: thư mục `SKLUMToolz/` (sẵn sàng cài đặt)
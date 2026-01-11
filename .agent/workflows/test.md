---
description: Perform pre-export checks (syntax, structure) with smart context detection
---

# /test Command Workflow

Workflow này thực hiện kiểm tra cú pháp và cấu trúc dự án. Nó hỗ trợ chế độ "Smart Scan" để chỉ kiểm tra các file vừa thay đổi.

## Quy trình xử lý

// turbo-all

1.  **Tạo Script Kiểm tra**:
    - Tạo file `_test_addon.py` với logic:
        - **Git Detection**: Tự động phát hiện các file `.py` đã thay đổi (staged, unstaged, untracked).
        - **Smart Scan**: Nếu tìm thấy file thay đổi, chỉ test syntax (`py_compile`) trên danh sách đó.
        - **Full Scan**: Nếu không có thay đổi (hoặc được yêu cầu `--full`), test toàn bộ dự án.
        - **Structure Check**: Luôn kiểm tra sự tồn tại của `__init__.py` và `blender_manifest.toml`.

2.  **Thực thi**:
    - Chạy mặc định (Smart): `python _test_addon.py`
    - Chạy Full (nếu cần thiết): `python _test_addon.py --full`

3.  **Xử lý kết quả**:
    - Nếu Exit Code = 0: ✅ Pass.
    - Nếu Exit Code = 1: ❌ Fail. Dừng quy trình và báo lỗi cho user.

## Ví dụ

User sửa file `operators.py`.
Agent chạy `/test`:
```
🔍 Testing SKLUMToolz addon...
   Mode: Smart Scan (1 changed files)
📊 Summary: Tested 1 Python files
✅ All tests passed!
```

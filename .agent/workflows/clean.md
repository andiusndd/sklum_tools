---
description: Clean build artifacts and temporary files (Keep latest ZIP)
---

# /clean Command Workflow

Workflow này dùng để dọn dẹp các file rác và build artifacts để project gọn gàng.

## Quy trình xử lý

// turbo-all

1.  **Tạo Script Dọn dẹp**:
    - Tạo file `_clean_project.py` với logic:
        - Quét và xóa toàn bộ thư mục `__pycache__` (đệ quy).
        - Xóa thư mục tạm: `SKLUMToolz_temp`, `build`, `dist`.
        - **ZIP Files**: Tìm tất cả file ZIP bắt đầu bằng `SKLUMToolz_`. Giữ lại file mới nhất (theo thời gian sửa đổi), xóa tất cả file cũ hơn.

2.  **Thực thi**:
    - Chạy: `python _clean_project.py`

3.  **Xóa Script**:
    - Tự xóa file `_clean_project.py` sau khi hoàn tất.

4.  **Đồng bộ Git (Push)**:
    - Sau khi dọn dẹp, đẩy trạng thái sạch sẽ của project lên GitHub.
    ```powershell
    git add -A; git commit -m "Clean up project and build artifacts"; git push github_repo main
    ```

## Ví dụ

```
/clean
```
Output:
- Deleted: .../__pycache__
- Deleted: SKLUMToolz_v2.5.0.zip
- ✨ Keeping latest: SKLUMToolz_v2.6.15.zip

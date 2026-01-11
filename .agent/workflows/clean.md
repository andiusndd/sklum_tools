---
description: Clean build artifacts and temporary files
---

# /clean Command Workflow

Workflow này giúp dọn dẹp các file rác, file tạm và cache để giữ dự án gọn gàng.

## Quy trình xử lý

// turbo-all

1.  **Tạo Script Cleaner**: Tạo file `_clean_project.py`.

    ```python
    import os
    import shutil

    def clean_project(root_dir):
        print(f"🧹 CLeaning project in: {root_dir}")
        deleted_count = 0
        
        # Extensions to remove
        extensions = {'.pyc', '.zip', '.log'}
        # Directories to remove
        dirs_to_remove = {'__pycache__', 'SKLUMToolz_temp'}
        # Specific files to remove
        files_to_remove = {'_audit_addon.py', '_export_addon.py', '_clean_project.py'}

        for root, dirs, files in os.walk(root_dir):
            
            # Remove Directories
            for d in list(dirs):
                if d in dirs_to_remove:
                    path = os.path.join(root, d)
                    try:
                        shutil.rmtree(path)
                        print(f"   Deleted Dir: {d}")
                        deleted_count += 1
                    except Exception as e:
                        print(f"❌ Failed to delete dir {d}: {e}")
                    dirs.remove(d) # Stop walking into it

            # Remove Files
            for f in files:
                _, ext = os.path.splitext(f)
                if ext in extensions or f in files_to_remove or f.startswith('_temp_'):
                    path = os.path.join(root, f)
                    try:
                        os.remove(path)
                        print(f"   Deleted File: {f}")
                        deleted_count += 1
                    except Exception as e:
                        print(f"❌ Failed to delete file {f}: {e}")

        print(f"✨ Clean complete. Removed {deleted_count} items.")

    if __name__ == "__main__":
        clean_project(os.getcwd())
    ```

2.  **Chạy Cleanup**: `python _clean_project.py`

3.  **Hoàn tất**: Script tự xóa chính nó (hoặc bị xóa bởi bước cuối cùng nếu cấu hình).

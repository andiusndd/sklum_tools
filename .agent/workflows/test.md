---
description: Perform pre-export checks (syntax, structure, manifest)
---

# /test Command Workflow

Khi nhận được `/test` hoặc `@[/test]`, Agent sẽ thực hiện kiểm tra toàn diện codebase (Audit).

## Quy trình xử lý

// turbo-all

1.  **Tạo Script Audit**: Tạo file `_audit_addon.py` để kiểm tra:
    -   Cú pháp Python (`py_compile`).
    -   Sự tồn tại của `blender_manifest.toml` (Bắt buộc cho Blender 4.2+).
    -   Kiểm tra các rule cấm (ví dụ: icon cũ).

    ```python
    import os
    import py_compile
    import sys
    
    # Configuration
    INVALID_ICONS = ["WIRE", "BOUNDS", "ORIENTATION_EXTERNAL", "PARENT_DEFORMED"] # Legacy blacklist
    MANIFEST_FILE = "blender_manifest.toml"

    def check_syntax(start_path):
        print(f"Checking syntax in {start_path}...")
        has_error = False
        count = 0
        for root, dirs, files in os.walk(start_path):
            if '.git' in dirs: dirs.remove('.git')
            if '__pycache__' in dirs: dirs.remove('__pycache__')
            
            for file in files:
                if file.endswith('.py') and not file.startswith('_'): 
                    full_path = os.path.join(root, file)
                    # 1. Check Syntax
                    try:
                        py_compile.compile(full_path, doraise=True)
                        count += 1
                    except Exception as e:
                        print(f"❌ Syntax Error in {file}: {e}")
                        has_error = True
                        continue
                    
                    # 2. Check Blacklist Content
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        for icon in INVALID_ICONS:
                            if f"icon='{icon}'" in content or f'icon="{icon}"' in content:
                                print(f"❌ '{icon}' (deprecated) found in {file}")
                                has_error = True
                    except: pass

        print(f"✅ Scanning {count} python files... Done.")
        return has_error

    def check_manifest(cwd):
        print("Checking blender_manifest.toml...")
        manifest_path = os.path.join(cwd, MANIFEST_FILE)
        if not os.path.exists(manifest_path):
            print(f"❌ Missing {MANIFEST_FILE}")
            return True
        return False

    if __name__ == "__main__":
        cwd = os.getcwd()
        failed = False
        
        if check_manifest(cwd): failed = True
        if check_syntax(cwd): failed = True
        
        if failed:
            print("\n⛔ AUDIT FAILED. Fix errors before exporting.")
            sys.exit(1)
        else:
            print("\n✨ AUDIT PASSED. Ready for export.")
    ```

2.  **Chạy Audit**: `python _audit_addon.py`

3.  **Dọn dẹp**: Xóa file `_audit_addon.py` sau khi hoàn tất (nếu thành công).

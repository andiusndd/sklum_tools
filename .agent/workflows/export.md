---
description: Export addon package using manifest-defined patterns
---

# /export Command Workflow

Khi nhận được `/export` hoặc `@[/export]`, Agent sẽ thực hiện quy trình đóng gói addon dựa trên `blender_manifest.toml`.

## Quy trình xử lý

// turbo-all

1.  **Git Push**:
    Đồng bộ mã nguồn trước khi đóng gói.
    ```powershell
    git add -A; git commit -m "Save state before export"; git push github_repo main
    ```

2.  **Pre-flight Check**:
    Khuyến nghị hoặc tự động chạy `/test` để đảm bảo code không có lỗi cú pháp trước khi đóng gói.
    `> Verifying codebase with /test...`

    ```python
    import os
    import zipfile
    import shutil
    import re
    import sys
    import tomllib
    import fnmatch

    def get_manifest_data():
        manifest_path = "blender_manifest.toml"
        if not os.path.exists(manifest_path):
            return {}
        try:
            with open(manifest_path, "rb") as f:
                return tomllib.load(f)
        except:
            return {}

    def should_exclude(path, patterns):
        """Check if path matches any of the exclude patterns."""
        # Normalize path to use forward slashes for matching
        path = path.replace(os.sep, '/')
        for pattern in patterns:
            # Handle directory patterns ending with /
            if pattern.endswith('/'):
                p = pattern.rstrip('/')
                if path == p or path.startswith(p + '/'):
                    return True
            # Handle glob patterns
            if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
                return True
        return False

    def export_addon():
        cwd = os.getcwd()
        manifest = get_manifest_data()
        version = manifest.get("version", "X.X.X")
        exclude_patterns = manifest.get("paths_exclude_pattern", [])
        
        zip_name = f"SKLUMToolz_v{version}.zip"
        temp_dir = "SKLUMToolz_temp"
        addon_dir = os.path.join(temp_dir, "SKLUMToolz")

        print(f"📦 Exporting {zip_name} (Manifest-Aware)...")

        if os.path.exists(temp_dir): shutil.rmtree(temp_dir)
        os.makedirs(addon_dir)

        count = 0
        for root, dirs, files in os.walk(cwd):
            # Calculate relative path from root
            rel_root = os.path.relpath(root, cwd)
            if rel_root == ".": rel_root = ""
            
            # Prune excluded directories to speed up walk
            for d in list(dirs):
                d_rel_path = os.path.normpath(os.path.join(rel_root, d))
                if should_exclude(d_rel_path, exclude_patterns):
                    dirs.remove(d)

            # Copy files
            for file in files:
                f_rel_path = os.path.normpath(os.path.join(rel_root, file))
                
                # Manifest is ALWAYS included
                if file == "blender_manifest.toml" and rel_root == "":
                    pass
                elif should_exclude(f_rel_path, exclude_patterns):
                    continue

                target_dir = os.path.join(addon_dir, rel_root)
                if not os.path.exists(target_dir): os.makedirs(target_dir)
                
                shutil.copy2(os.path.join(root, file), os.path.join(target_dir, file))
                count += 1

        # Zip it
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    src = os.path.join(root, file)
                    rel = os.path.relpath(src, temp_dir)
                    zipf.write(src, rel)
        
        shutil.rmtree(temp_dir)
        print(f"✅ Exported {count} files to {zip_name} (based on manifest)")

    if __name__ == "__main__":
        export_addon()
    ```

5.  **Xác minh**:
    ```powershell
    Test-Path "SKLUMToolz_v*.zip"
    ```

6.  **Báo cáo**: Thông báo file ZIP đã sẵn sàng.
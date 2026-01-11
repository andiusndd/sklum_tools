---
description: Automated release pipeline (Version -> Log -> Audit -> Export)
---

# /release Command Workflow

Workflow này tự động hóa toàn bộ quy trình phát hành phiên bản mới.

## Quy trình xử lý

1.  **Thu thập thông tin**:
    Agent hỏi người dùng:
    - `VERSION_TYPE`: `major` | `minor` | `patch` (hoặc số version cụ thể e.g. `2.7.0`)
    - `CHANGELOG`: Nội dung thay đổi ngắn gọn.

2.  **Tạo Script Helper**: Tạo `_release_helper.py` để cập nhật version và log.

    ```python
    import os
    import re
    import sys
    from datetime import datetime

    MANIFEST_FILE = "blender_manifest.toml"
    INIT_FILE = "__init__.py"

    def update_manifest_version(version_input):
        if not os.path.exists(MANIFEST_FILE):
            print(f"❌ {MANIFEST_FILE} not found!")
            sys.exit(1)

        with open(MANIFEST_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regex for TOML version: version = "1.0.0"
        match = re.search(r'version\s*=\s*[\"|\'](\d+)\.(\d+)\.(\d+)[\"|\']', content)
        if not match:
             print("❌ Cannot find version in manifest")
             sys.exit(1)

        major, minor, patch = map(int, match.groups())

        if version_input == 'major': major += 1; minor = 0; patch = 0
        elif version_input == 'minor': minor += 1; patch = 0
        elif version_input == 'patch': patch += 1
        else: # Specific
            try:
                parts = version_input.split('.')
                major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
            except:
                print("❌ Invalid version format")
                sys.exit(1)

        new_version_str = f"{major}.{minor}.{patch}"
        
        # 1. Update Manifest
        new_content = re.sub(r'version\s*=\s*[\"|\']\d+\.\d+\.\d+[\"|\']', f'version = "{new_version_str}"', content)
        with open(MANIFEST_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"   Updated {MANIFEST_FILE} -> {new_version_str}")
        return major, minor, patch

    def sync_init_file(major, minor, patch):
        # Keeps legacy __init__.py in sync for backward compatibility
        if not os.path.exists(INIT_FILE): return
        
        with open(INIT_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_tuple = f'"version": ({major}, {minor}, {patch})'
        new_content = re.sub(r'"version":\s*\(\d+,\s*\d+,\s*\d+\)', new_tuple, content)
        
        with open(INIT_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"   Synced {INIT_FILE}")

    def update_log(version_str, changelog):
        log_path = "UPDATE-LOG.md"
        today = datetime.now().strftime("%Y-%m-%d")
        header = f"## [{version_str}] - {today}\n"
        entry = f"{header}{changelog}\n\n"
        
        try:
             with open(log_path, 'r', encoding='utf-8') as f:
                old_content = f.read()
             
             lines = old_content.splitlines(keepends=True)
             insert_idx = 4
             if len(lines) > 4: lines.insert(insert_idx, entry)
             else: lines.append(entry)
            
             with open(log_path, 'w', encoding='utf-8') as f:
                 f.writelines(lines)
        except Exception as e:
            print(f"⚠️ Could not update log: {e}")

    if __name__ == "__main__":
        if len(sys.argv) < 3:
            print("Usage: python _release_helper.py <type> <notes>")
            sys.exit(1)
        
        v_type = sys.argv[1]
        notes = sys.argv[2]
        
        major, minor, patch = update_manifest_version(v_type)
        sync_init_file(major, minor, patch)
        update_log(f"{major}.{minor}.{patch}", notes)
        
        print(f"✅ Released v{major}.{minor}.{patch}")
    ```

3.  **Thực thi Release Pipeline**:

    -   **Bước 1: Cleanup (`/clean`)**
        Agent chạy quy trình dọn dẹp để đảm bảo package sạch sẽ.
        `> Running /clean...`

    -   **Bước 2: Update Version & Log**
        Chạy script helper: `python _release_helper.py <VERSION_TYPE> <CHANGELOG>`
        Xóa script helper sau khi xong.

    -   **Bước 3: Audit (`/test`)**
        Agent chạy quy trình Audit.
        `> Running /test...`
        **CRITICAL**: Nếu Audit thất bại, DỪNG LẠI NGAY LẬP TỨC.

    -   **Bước 4: Export (`/export`)**
        Nếu Audit thành công, chạy quy trình Export.
        `> Running /export...`
        
    -   **Hoàn tất**: Thông báo file ZIP cuối cùng.

## Ví dụ
```
/release
> Input: patch
> Input: "Fix bug UI crash"
```
-> Tự động tăng patch -> update log -> audit -> export zip.

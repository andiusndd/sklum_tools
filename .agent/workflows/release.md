---
description: Automated release pipeline (Version -> Log -> Clean -> Test -> Export)
---

# /release Command Workflow

Workflow này tự động hóa toàn bộ quy trình phát hành phiên bản mới, kết nối các workflow con (`/clean`, `/test`, `/export`) thành một chuỗi hoàn chỉnh.

## Tự động hỏi từng bước

Nếu user gửi `/release` thiếu tham số, hãy hỏi:

1. **VERSION_TYPE**: `major` | `minor` | `patch` (hoặc số cụ thể).
2. **CHANGELOG**: Nội dung thay đổi ngắn gọn để ghi vào log.

## Quy trình xử lý

// turbo-all

1.  **Dọn dẹp môi trường (Cleanup)**:
    - Thực thi workflow `clean.md` để xóa rác và cache cũ.
    - `python _clean_project.py`

2.  **Cập nhật Phiên bản & Log**:
    - Tạo và chạy script `_release_helper.py` (như mẫu bên dưới) để:
        - Tăng version trong `blender_manifest.toml` và `__init__.py`.
        - Chèn nội dung changelog vào đầu file `UPDATE-LOG.md`.
    - Sau đó xóa script helper.

3.  **Đồng bộ Git**:
    - Push phiên bản mới lên GitHub.
    ```powershell
    git add -A; git commit -m "Bump version to new release"; git push github_repo main
    ```

4.  **Kiểm tra chất lượng (Audit/Test)**:
    - Thực thi workflow `test.md`.
    - Chạy `python _test_addon.py`.
    - **CRITICAL**: Nếu bước này báo lỗi (Exit code 1), **DỪNG QUY TRÌNH NGAY**. Yêu cầu user sửa lỗi (gợi ý dùng `/fix`).

5.  **Đóng gói (Export)**:
    - Nếu Audit OK, thực thi workflow `export.md`.
    - Chạy `python _export_addon.py`.

6.  **Báo cáo**:
    - Thông báo version mới.
    - Đường dẫn file ZIP đã tạo.

### Mẫu Script Helper (_release_helper.py)

```python
import os
import re
import sys
from datetime import datetime

MANIFEST_FILE = "blender_manifest.toml"
INIT_FILE = "__init__.py"

def update_manifest_version(version_input):
    if not os.path.exists(MANIFEST_FILE): sys.exit(1)

    with open(MANIFEST_FILE, 'r', encoding='utf-8') as f: content = f.read()

    match = re.search(r'version\s*=\s*[\"|\'](\d+)\.(\d+)\.(\d+)[\"|\']', content)
    if not match: sys.exit(1)

    major, minor, patch = map(int, match.groups())

    if version_input == 'major': major += 1; minor = 0; patch = 0
    elif version_input == 'minor': minor += 1; patch = 0
    elif version_input == 'patch': patch += 1
    else: 
        try:
            parts = version_input.split('.')
            major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
        except: sys.exit(1)

    new_version_str = f"{major}.{minor}.{patch}"
    
    new_content = re.sub(r'version\s*=\s*[\"|\']\d+\.\d+\.\d+[\"|\']', f'version = "{new_version_str}"', content)
    with open(MANIFEST_FILE, 'w', encoding='utf-8') as f: f.write(new_content)
        
    return major, minor, patch

def sync_init_file(major, minor, patch):
    if not os.path.exists(INIT_FILE): return
    with open(INIT_FILE, 'r', encoding='utf-8') as f: content = f.read()
    new_tuple = f'"version": ({major}, {minor}, {patch})'
    new_content = re.sub(r'"version":\s*\(\d+,\s*\d+,\s*\d+\)', new_tuple, content)
    with open(INIT_FILE, 'w', encoding='utf-8') as f: f.write(new_content)

def update_log(version_str, changelog):
    log_path = "UPDATE-LOG.md"
    today = datetime.now().strftime("%Y-%m-%d")
    header = f"## [{version_str}] - {today}\n"
    entry = f"{header}### Released\n- {changelog}\n\n"
    
    try:
         with open(log_path, 'r', encoding='utf-8') as f: lines = f.readlines()
         # Insert after header or at suitable position (e.g., line 4)
         insert_idx = 0
         for i, line in enumerate(lines):
             if line.strip() == "": insert_idx = i + 1; break
         if insert_idx == 0 and len(lines) > 2: insert_idx = 4
         
         lines.insert(insert_idx, entry)
         with open(log_path, 'w', encoding='utf-8') as f: f.writelines(lines)
    except: pass

if __name__ == "__main__":
    v_type = sys.argv[1]
    notes = sys.argv[2]
    maj, min, pat = update_manifest_version(v_type)
    sync_init_file(maj, min, pat)
    update_log(f"{maj}.{min}.{pat}", notes)
    print(f"✅ Released v{maj}.{min}.{pat}")
```

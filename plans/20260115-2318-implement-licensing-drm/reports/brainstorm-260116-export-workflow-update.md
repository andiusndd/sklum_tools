# Cập Nhật Quy Trình Export (Tích Hợp DRM)

Để tạo ra file ZIP chuẩn chứa tính năng DRM, chúng ta cần cập nhật workflow `/export` với 2 thay đổi nhỏ nhưng quan trọng:

1.  **Loại bỏ file rác:** Script export hiện tại đã loại bỏ các folder không cần thiết (`.gemini`, `.agent`, `server_backend`). Điều này là tốt.
2.  **(Tùy chọn) Obfuscation:** Nếu bạn muốn giấu code license, cần tích hợp **PyArmor**. Tuy nhiên, nếu chưa cài PyArmor, chúng ta sẽ để chế độ `USE_PYARMOR = False` như mặc định.

## Phân tích Workflow Hiện Tại
Workflow `/export` hiện tại (trong `.agent/workflows/export.md`) sử dụng một script python nội tuyến (`_export_addon.py`) để đóng gói.

## Kế hoạch Cập Nhật
Tôi sẽ cập nhật nội dung của file workflow `.agent/workflows/export.md` để:
1.  Bao gồm logic loại trừ `server_backend` (vì code server không nên nằm trong addon của khách).
2.  Chuẩn hóa cấu trúc ZIP (có thư mục cha `SKLUMToolz` bên trong).

**Nội dung script Python mới trong workflow:**
```python
    def export_addon():
        # ... (setup paths) ...
        
        # Walk and copy
        for root, dirs, files in os.walk(cwd):
            # EXCLUDE LIST
            if '.git' in dirs: dirs.remove('.git')
            if 'server_backend' in dirs: dirs.remove('server_backend') # KICK OUT SERVER CODE
            if 'sklum-license-backend' in dirs: dirs.remove('sklum-license-backend')
            # ... (rest is same) ...
```

## Câu hỏi cho User
Bạn có muốn tôi sửa trực tiếp file `.agent/workflows/export.md` để cập nhật logic loại trừ thư mục Server code không?
(Hiện tại workflow cũ có thể vô tình đóng gói cả folder `server_backend` vào ZIP nếu không filter kỹ).

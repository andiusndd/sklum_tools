# Cấu trúc Dự án SKLUM Tools

Tài liệu này mô tả tổ chức mã nguồn sau khi refactor theo từng panel UI.

## Tổng quan

```
SKLUMToolz/
├── __init__.py
├── README.md
├── STRUCTURE.md
├── update-log.md
├── core/
├── panel_checker_tools/
├── panel_import_export/
├── panel_jpg_converter/
├── panel_auto_rename/
├── panel_object_setting/
└── presets.json (tự động tạo nếu chưa có)
```

- **`__init__.py`**: Điểm vào của add-on. Đăng ký lần lượt `core` và các module panel.
- **`core/`**: Chứa hằng số, tiện ích dùng chung, preferences và global scene properties.
- **Các thư mục `panel_*`**: Mỗi thư mục tương ứng một panel trong Sidebar của Blender, gom toàn bộ operator, UI list, panel và logic liên quan.

## Chi tiết thư mục

### `core/`
- `constants.py`: Các hằng số chung (tên add-on, default settings, mapping texture,...).
- `utils.py`: Hàm hỗ trợ (message box, kiểm tra origin, truy vấn material).
- `preferences.py`: Đăng ký `AddonPreferences` và các tùy chọn chung (đường dẫn CSV).
- `properties.py`: Đăng ký các Scene properties toàn cục dùng cho nhiều panel.
- `__init__.py`: Gom và đăng ký lần lượt các file trên.

### `panel_checker_tools/`
- `check_all/`: Operator tổng hợp `Check All`.
- `rename_uvmap/`: UI List và operator liên quan tới rename/reset UVMap.
- `hard_edges/`: Operator chọn cạnh cứng.
- `color_space/`: Danh sách và công cụ kiểm tra/fix Color Space.
- `active_point/`: Kiểm tra origin, group to empty, apply transforms.
- `seam_sharp/`: Kiểm tra/điều chỉnh seam và cạnh sharp.
- `grid_checker/`: Operator kiểm tra mặt tam giác/N-gon.
- `panel.py`: Panel UI tổng hợp.
- `__init__.py`: Đăng ký tất cả module thành phần theo thứ tự.

### `panel_import_export/`
- `operators.py`: Import vật liệu GLB, export FBX/GLB, pack/unpack/clean textures.
- `panel.py`: Panel UI cho nhóm tính năng Import/Export.
- `__init__.py`: Đăng ký panel và operators.

### `panel_jpg_converter/`
- `utils.py`: Kiểm tra cài đặt Pillow.
- `operators.py`: Chuyển đổi PNG → JPG hàng loạt hoặc theo ảnh.
- `panel.py`: Panel điều khiển chuyển đổi.
- `__init__.py`: Đăng ký utils/operators/panel.

### `panel_auto_rename/`
- `utils.py`: Quản lý cache CSV, preset, helper cho panel.
- `properties.py`: `PropertyGroup` cho settings và danh sách rename.
- `ui_list.py`: UIList hiển thị danh sách phần tử rename.
- `menus.py`: Menus chọn preset.
- `operators.py`: Logic thêm/xóa/làm rõ danh sách và đổi tên hàng loạt.
- `handlers.py`: Handler load file để nạp cache CSV.
- `panel.py`: Panel UI chính.
- `__init__.py`: Đăng ký tất cả module con.

### `panel_object_setting/` [NEW]
- `properties.py`: Lưu trữ trạng thái UI (rename string, origin settings, location).
- `operators.py`: Các thao tác với Object (Selection, Transform, Origin, Shading, Material, Parent).
- `ui.py`: Thiết kế giao diện bảng điều khiển tích hợp.
- `__init__.py`: Đăng ký properties, operators và UI.

## Quy ước đăng ký

Mỗi module con cung cấp `register()`/`unregister()` của riêng mình. `__init__.py` chính chỉ cần gọi danh sách modules theo thứ tự, đảm bảo unregister theo thứ tự ngược lại.

## Tài liệu liên quan

- `README.md`: Hướng dẫn cài đặt, mô tả tính năng add-on.

# SKLUM Tools - Update Log

Tất cả các thay đổi quan trọng đối với dự án SKLUM Tools sẽ được ghi lại trong file này.

## [v2.6.15] - 2026-01-11
### Fixed
- **Import/Export Panel**: Sửa lỗi `ImportError` do import sai `PropertyGroup` từ `bpy.props` thay vì `bpy.types`.

## [v2.6.14] - 2026-01-11
### Fixed
- **Import/Export Panel**: Sửa lỗi `AttributeError` khi tạo Box do chưa đăng ký property settings.

## [v2.6.13] - 2026-01-11
### Added
- **Import/Export Panel**: Thêm tính năng **Tạo Box** nhanh.
  - Cho phép nhập kích thước X, Y, Z.
  - Tự động tạo Box, áp dụng scale, đặt gốc tọa độ (Origin) tại mặt đáy.
  - Đưa đối tượng về vị trí (0, 0, 0).

## [v2.6.12] - 2026-01-11
### Improved
- **UI/UX**: Tất cả các panel SKLUM giờ mặc định ở trạng thái đóng (collapsed) khi mở Blender.
  - Thêm `bl_options = {'DEFAULT_CLOSED'}` vào `panel_checker_tools` và `panel_object_setting`.
  - Giúp giao diện gọn gàng hơn, người dùng chỉ mở panel cần thiết.

## [v2.6.11] - 2026-01-11
### Fixed
- **panel_object_setting**: Sửa lỗi `AttributeError` khi nhấn nút "Hiển thị" (Display) trong nhóm Materials.
  - Lỗi xảy ra do operator `wm.properties_context_change` không hoạt động khi gọi từ 3D Viewport.
  - Thay thế bằng logic tìm Properties Editor area và chuyển context trực tiếp.
  - Thêm thông báo thân thiện nếu không tìm thấy Properties Editor.

## [v2.6.10] - 2026-01-11
### Improved
- **UI & Localization**: Việt hóa toàn bộ panel Object Setting.
- **Toggles**: 
  - Nút **Random Color** và **Flat Color** giờ có thể bật/tắt (toggle) thay vì chỉ bật.
  - Sửa lỗi nút **Render** hiển thị ngược trạng thái.
- **New Feature**: Thêm nhóm **Trục điều khiển (Gizmos)** để bật/tắt nhanh Move/Rotate/Scale.

## [v2.6.9] - 2026-01-11
### Improved
- **Custom Origin UI**: Cải thiện giao diện trực quan hơn.
  - Thêm nhãn X, Y, Z cho từng hàng tùy chọn.
  - Sử dụng button set thay cho dropdown để thao tác nhanh.
  - Đổi tên các tùy chọn thành: Trái/Giữa/Phải, Trước/Giữa/Sau, Dưới/Giữa/Trên.

## [v2.6.8] - 2026-01-11
### Fixed
- **Custom Origin**: Sửa lỗi thiếu tùy chọn và tính toán sai.
  - Thêm 3 dropdown riêng biệt cho X, Y, Z (Min/Center/Max).
  - Nút "Set Origin" to rõ, dễ thao tác.
  - Logic tính toán dựa trên Bounding Box chuẩn xác hơn.

## [v2.6.7] - 2026-01-11
### Changed
- **UI Object Setting**: Cải thiện giao diện, chuyển sang bố cục dọc thoáng hơn.
  - Các nhóm chức năng (Rename, Select, Transform...) có tiêu đề riêng.
  - Nút bấm được sắp xếp lại dạng Grid/Row, hiển thị rõ ràng hơn.
- **Workflow**: Cập nhật quy trình Export hỗ trợ cấu trúc Legacy/Extensions Hybrid.

## [2.6.6] - 2026-01-11
### UI Overhaul
- **panel_object_setting**: Thiết kế lại toàn bộ giao diện theo chuẩn "Pixel-Perfect Split Layout".
- Căn chỉnh thẳng hàng labels và controls (tỉ lệ 40/60).
- Tối ưu hóa không gian cho các nhóm nút Shading, Materials, Custom Origin.
- Sử dụng icon chính xác cho từng mục (Rename, Transform, Type...).

## [2.6.5] - 2026-01-11
### Fixed
- **panel_object_setting**: Sửa lỗi UI layout - xóa property `location_axis` bị đặt sai vị trí trong phần Apply Transform.
- **panel_object_setting**: Hoàn thiện logic đặt origin cho BOTTOM (đáy bounding box) và HEAD (đỉnh bounding box) sử dụng cursor placement chính xác.
- **panel_object_setting**: Implement đầy đủ chức năng CUSTOM origin với khả năng tùy chỉnh vị trí Z (Bottom/Center/Top) và XY (Center/Origin) theo properties.

## [2.6.4] - 2026-01-11
### Fixed
- Sửa lỗi `TypeError` nghiêm trọng trên Blender 4.2 do sử dụng tên icon không tồn tại (`ORIENTATION_EXTERNAL`, `PARENT_DEFORMED`).
- Thay thế bằng các icon hợp lệ (`NORMALS_FACE`, `ORIENTATION_PARENT`) giúp panel hiển thị ổn định trên mọi phiên bản Blender 4.x.

## [2.6.3] - 2026-01-11
### Fixed
- Đại tu toàn bộ logic vẽ UI (draw method) cho module Object Setting.
- Sử dụng `prop_enum` cho các nút bấm trạng thái chuyên biệt (Random, Flat Color) để đảm bảo hiển thị đúng kiểu nút bấm thay vì dropdown.
- Thêm cơ chế kiểm tra lỗi phân mảnh (modular safety checks) để dù một phần Viewport gặp lỗi, các nhóm chức năng khác (Rename, Origin, Transform...) vẫn hiển thị đầy đủ 100%.

## [2.6.2] - 2026-01-11
### Fixed
- Đồng bộ tên panel thành `SKLUM - Object Setting` cho nhất quán với hệ thống.
- Sửa lỗi UI crash khiến phần lớn các nút chức năng không hiển thị: Thêm cơ chế kiểm tra an toàn (safe access) khi truy cập thuộc tính Viewport.

## [2.6.1] - 2026-01-11
### Fixed
- Bổ sung các nút chức năng còn thiếu trong module `panel_object_setting`:
    - Thêm nút `Display` và `Rename` cho nhóm Materials.
    - Chuẩn hóa nhãn và icon cho nhóm `Display Overlay` (Normal, Wireframes, Random, Flat Color, Origins, render).
    - Cải thiện layout để giống 100% so với thiết kế mẫu.

## [2.6.0] - 2026-01-11
### Added
- Thêm module mới `panel_object_setting`: Bảng điều khiển quản lý đối tượng toàn diện.
    - Nhóm `Display Overlay`: Tùy chỉnh nhanh chế độ hiển thị Viewport (Wireframes, Face Orientation, Origins...).
    - Nhóm `Object Display`: Chỉnh chế độ hiển thị riêng cho Object (Wire, Bounds, Name, X-ray...).
    - Nhóm `Object`:
        - Rename: Đổi tên hàng loạt.
        - Select By Type: Chọn nhanh mesh, light, camera, empty...
        - Apply Transform: Scale, Rotation, All.
        - Quick Origin: Đặt trọng tâm vào Bottom, Center, Head.
        - Custom Origin: Đặt trọng tâm tùy chỉnh theo trục.
        - Shading: FlipNormal, AutoSmooth, Mark/Clear Sharp.
        - Materials: Quản lý nhanh vật liệu (Remove).
        - Location & Parent: Di chuyển theo trục và thiết lập quan hệ cha con.
        - Make Single User: Tách dữ liệu độc lập.

## [2.5.9] - 2026-01-11
### Added
- Hỗ trợ hiển thị đa socket trên nhãn node: Nếu một texture được cắm vào nhiều đầu vào (ví dụ: Metallic và Roughness), nhãn của node sẽ hiển thị tất cả các tên socket đó, ngăn cách bằng khoảng trắng (e.g., `METALLIC ROUGHNESS`).
- Cải tiến hàm trace: Có khả năng thu thập toàn bộ các điểm kết nối thay vì chỉ dừng lại ở điểm đầu tiên.

## [2.5.8] - 2026-01-11
### Added
- Trường hợp đặc biệt cho nhóm RMA: Các texture cắm vào Roughness, Metallic, hoặc Occlusion sẽ được đặt tên file kết thúc bằng `_RMA`.
- Tách biệt logic đặt tên file và nhãn node: Nhãn node vẫn giữ đúng tên socket (e.g., `METALLIC`, `ROUGHNESS`) để người dùng dễ phân biệt, trong khi file vật lý được gộp chung hậu tố `_RMA`.

## [2.5.7] - 2026-01-11
### Refactored
- Chuẩn hóa hoàn toàn logic đổi tên texture: Tất cả các loại texture (bao gồm cả Normal Map) giờ đây đều được xử lý đồng nhất dựa trên vị trí kết nối (Socket).
- Loại bỏ các trường hợp kiểm tra đặc biệt cho loại Node, đảm bảo tính nhất quán tuyệt đối theo vị trí cắm dây.

## [2.5.6] - 2026-01-11
### Fixed
- Ưu tiên tuyệt đối logic Trace (vị trí cắm) để đổi tên texture. Khắc phục lỗi khi Normal node cắm vào các socket không phải Normal (ví dụ: Transmission Weight).
- Node label giờ luôn phản ánh chính xác socket đích (e.g., "TRANSMISSION", "METALLIC").

## [2.5.5] - 2026-01-11
### Added
- Hàm `_trace_to_principled_bsdf()` để trace kết nối texture qua các node trung gian.
- Mở rộng `TEXTURE_TYPE_MAPPING` với tất cả các socket của Principled BSDF (Transmission, Coat, Sheen, Emission, Thin Film...).

### Fixed
- Sửa lỗi đổi tên texture không nhận diện được khi cắm gián tiếp vào Principled BSDF (ví dụ: Transmission > Weight).
- Node texture giờ được đổi tên label (e.g., "TRANSMISSION") cùng với file texture.

## [2.5.4] - 2026-01-11
### Added
- Thêm file `update-log.md` để theo dõi lịch sử cập nhật.
- Bổ sung tài liệu phân tích dự án chi tiết.

### Changed
- Cập nhật `README.md` với cấu trúc mới và hướng dẫn chi tiết hơn.
- Cập nhật `STRUCTURE.md` để đồng bộ với tổ chức file hiện tại.
- Tối ưu hóa mô tả các tính năng chính trong tài liệu.

## [2.5.2] - Trước đó
### Added
- Triển khai tính năng **Auto Rename** dựa trên file CSV (IDP).
- Thêm công cụ **Check All** hỗ trợ QA nhanh.
- Tích hợp **JPG Converter** (PNG to JPG).
- Hỗ trợ xuất file GLB với nén Draco.

## [1.0.0] - Khởi tạo
- Khởi tạo dự án với các tính năng cơ bản về kiểm tra Mesh và Material.

# SKLUM Tools - Update Log

Tất cả các thay đổi quan trọng đối với dự án SKLUM Tools sẽ được ghi lại trong file này.

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

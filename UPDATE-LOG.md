# SKLUM Tools - Update Log

Tất cả các thay đổi quan trọng đối với dự án SKLUM Tools sẽ được ghi lại trong file này.

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

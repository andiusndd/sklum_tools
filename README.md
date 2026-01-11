# SKLUM Tools – Blender Add-on

**Tác giả:** AndiuS  
**Phiên bản:** 2.5.4  
**Blender:** 4.2.0+  
**Nguồn:** [https://github.com/andiusndd/sklum_tools](https://github.com/andiusndd/sklum_tools)

SKLUM Tools cung cấp bộ tiện ích kiểm tra chất lượng mô hình (QA), tự động hoá đổi tên và hỗ trợ quy trình import/export dành cho pipeline sản xuất chuyên nghiệp.

## Mục lục
- [SKLUM Tools – Blender Add-on](#sklum-tools--blender-add-on)
  - [Mục lục](#mục-lục)
  - [Cài đặt](#cài-đặt)
  - [Tính năng nổi bật](#tính-năng-nổi-bật)
  - [Cấu trúc dự án](#cấu-trúc-dự-án)
  - [Lịch sử cập nhật](#lịch-sử-cập-nhật)
  - [Đóng góp \& phát triển](#đóng-góp--phát-triển)
  - [Giấy phép](#giấy-phép)

## Cài đặt
1. Tải file `.zip` từ trang Releases.
2. Mở Blender > `Edit → Preferences → Add-ons` > `Install...` và chọn file `.zip`.
3. Tìm kiếm và kích hoạt add-on **SKLUM Tools**.

Add-on xuất hiện tại `3D Viewport → Sidebar → SKLUM Tools`.

## Tính năng nổi bật
*   **Check All:** Tổng hợp kiểm tra UV, seam/sharp, color space, modifier, vertex group... kết quả hiển thị trực quan thông qua mã màu và biểu tượng cảnh báo.
*   **Auto Rename:** Quản lý tên Object/Material/Texture hàng loạt thông qua file CSV (IDP). Hỗ trợ hệ thống Preset mạnh mẽ để tùy chỉnh hậu tố (suffix).
*   **Checker Tools:**
    *   **Color Space:** Tự động sửa Color Space cho Texture (sRGB cho Diffuse, Non-Color cho RMA/Normal).
    *   **Active Point:** Chuẩn hóa Origin về tâm và hỗ trợ Group-to-Empty nhanh chóng.
    *   **Grid Checker:** Phát hiện các mặt lỗi (Triangles/N-gons) không mong muốn.
*   **Import/Export:** 
    *   Export FBX/GLB với cấu hình tối ưu cho Engine.
    *   Hỗ trợ Draco Compression và tùy chỉnh định dạng ảnh cho GLB.
    *   Tính năng Pack/Unpack và Purge dữ liệu thừa.
*   **JPG Converter:** Chuyển đổi texture PNG sang JPG để tối ưu dung lượng (Yêu cầu thư viện Pillow).

## Cấu trúc dự án
Chi tiết về tổ chức mã nguồn có thể xem tại [STRUCTURE.md](STRUCTURE.md).
- **`core/`**: Hằng số, tiện ích và các Scene properties dùng chung.
- **`panel_*/`**: Các module panel riêng biệt cho từng nhóm tính năng.

## Lịch sử cập nhật
Xem chi tiết các thay đổi qua từng phiên bản tại [update-log.md](update-log.md).

## Đóng góp & phát triển
1. Clone repo và mở thư mục `SKLUMToolz/`.
2. Mọi operator/panel mới nên được đặt trong module panel phù hợp để đảm bảo tính modular.
3. Khi sửa cấu trúc, cập nhật `STRUCTURE.md` và `README.md`.

## Giấy phép
Xem thông tin chi tiết trong repository GitHub.

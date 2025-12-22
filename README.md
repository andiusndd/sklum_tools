# SKLUM Tools – Blender Add-on

**Tác giả:** AndiuS  
**Phiên bản:** 2.5.1  
**Blender:** 4.2.0+  
**Nguồn:** [https://github.com/andius/SKLUM_Tools](https://github.com/andius/SKLUM_Tools)

SKLUM Tools cung cấp bộ tiện ích kiểm tra chất lượng mô hình, tự động hoá đổi tên và hỗ trợ quy trình import/export dành cho pipeline sản xuất.

## Cài đặt
1. Tải file `.zip` từ trang Releases.
2. Blender > `Edit → Preferences → Add-ons` > `Install...` và chọn file `.zip`.
3. Đánh dấu kích hoạt add-on **SKLUM Tools**.

Add-on xuất hiện tại `3D Viewport → Sidebar → SKLUM Tools`.

## Cấu trúc chính
- **`core/`** – Hằng số, tiện ích, preferences và Scene properties dùng chung.
- **`panel_checker_tools/`** – Panel "Checker & Tools" (Check All, rename/reset UV, hard edges, color space, active point, seam/sharp, grid checker).
- **`panel_import_export/`** – Import vật liệu GLB, export FBX/GLB, pack/unpack texture, purge dữ liệu.
- **`panel_jpg_converter/`** – Chuyển đổi PNG → JPG hàng loạt hoặc riêng lẻ.
- **`panel_auto_rename/`** – Tự động đổi tên object/material theo dữ liệu CSV và preset.
- **`legacy/`** – Lưu bản mã nguồn cũ (không còn được đăng ký). Xem `legacy/README.md` để tham khảo.

Chi tiết module xem thêm `STRUCTURE.md`.

## Tính năng nổi bật
- **Check All:** Tổng hợp kiểm tra UV, seam/sharp, color space, modifier, vertex group… và hiển thị kết quả với cảnh báo rõ ràng.
- **Rename & UVMap:** Danh sách các đối tượng, đổi tên nhanh, reset tên UVMap.
- **Hard Edges:** Chọn cạnh vượt ngưỡng góc, hỗ trợ soát lỗi bevel.
- **Color Space:** Kiểm tra/fix tự động màu sắc texture theo chuẩn sRGB/Non-Color.
- **Active Point:** Kiểm tra origin, tự động sửa về tâm, group về Empty và apply transform.
- **Seam & Sharp:** Mark seam từ UV, chuyển Sharp → Seam, xoá seam/sharp.
- **Grid Checker:** Tô sáng tam giác hoặc N-gon vượt chuẩn.
- **Import/Export:** Xuất FBX/GLB với cấu hình chuẩn, thêm tùy chọn Export .GLB nén (Draco + format ảnh tùy chỉnh), nhập vật liệu GLB và quản lý texture pack/unpack.
- **JPG Converter:** Chuyển đổi PNG sang JPG với chất lượng 95/65/35%.
- **Auto Rename:** Đọc CSV IDP, đổi tên object/material/texture theo preset, cập nhật cache tự động khi mở file.

## Dữ liệu phụ trợ
- `presets.json` – Lưu preset tên model/material/mesh.
- `dataIDP.json` – Cache từ CSV (được tạo khi load IDP).

## Đóng góp & phát triển
1. Clone repo và mở thư mục `SKLUMToolz/` trong Blender (`Edit → Preferences → File Paths → Scripts` nếu cần add-on từ local).
2. Mọi operator/panel mới nên được đặt trong module panel phù hợp.
3. Khi sửa cấu trúc, cập nhật `STRUCTURE.md` và README.

## Giấy phép
Xem thông tin chi tiết trong repository GitHub.

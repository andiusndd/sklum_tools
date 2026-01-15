---
description: Workflow to implement new features or changes
---

# /update Command Workflow

Khi nhận được prompt bắt đầu bằng `/update` hoặc `@[/update]`, Agent sẽ thực hiện theo quy trình sau:

## Tự động hỏi từng bước

Nếu user chỉ gửi `/update` hoặc `@[/update]` **MÀ KHÔNG CÓ NỘI DUNG ĐI KÈM**, Agent phải **HỎI LẦN LƯỢT** từng trường theo thứ tự sau:

1. **Bước 1**: Hỏi về `CONTEXT` - "Bạn đang gặp vấn đề gì? (Mô tả lỗi hoặc yêu cầu)"
2. **Bước 2**: Hỏi về `PRIORITY` - "Mức độ ưu tiên là gì? (critical / normal / low)"
3. **Bước 3**: Hỏi về `CORE` - "Có module/chức năng nào KHÔNG ĐƯỢC SỬA không? (Nhấn Enter để bỏ qua)"
4. **Bước 4**: Hỏi về `ACTION` - "Bạn muốn tôi làm gì cụ thể?"
5. **Bước 5**: Hỏi về `EXPECTED_RESULT` - "Kết quả mong đợi sau khi sửa là gì?"

Sau khi thu thập đủ thông tin, Agent tự động tiến hành quy trình xử lý.

---

## Cấu trúc Prompt đầy đủ

```
/update
UPDATE: v[phiên_bản]
PRIORITY: [critical/normal/low]
CORE: [Nguyên tắc cốt lõi không được vi phạm]
CONTEXT: [Mô tả vấn đề hoặc lỗi đang gặp]
ACTION: [Yêu cầu sửa đổi cụ thể]
EXPECTED_RESULT: [Kết quả mong đợi sau khi sửa]
```

## Quy trình xử lý

// turbo-all

1.  **Tạo Backup (Git Commit)**: Trước khi thực hiện bất kỳ thay đổi nào, Agent phải tạo một commit với message mô tả trạng thái hiện tại (ví dụ: `git commit -am "Backup before update vX.X.X"`). Điều này đảm bảo có thể rollback nếu cần.

2.  **Đọc và phân tích prompt**: Xác định rõ:
    - `UPDATE`: Phiên bản mục tiêu.
    - `PRIORITY`: Mức độ ưu tiên (`critical` cần xử lý ngay, `normal` xử lý theo thứ tự, `low` có thể hoãn).
    - `CORE`: Nguyên tắc bất khả xâm phạm.
    - `CONTEXT`: Bối cảnh và mô tả lỗi.
    - `ACTION`: Hành động cần thực hiện.
    - `EXPECTED_RESULT`: Tiêu chí để xác minh thành công.

3.  **Tuân thủ CORE**: **KHÔNG BAO GIỜ** sửa đổi bất kỳ code nào nằm ngoài phạm vi được đề cập trong `CONTEXT` và `ACTION`. Nếu một chức năng đang hoạt động ổn định và không được nhắc đến, hãy để yên.

4.  **Thực hiện ACTION**: Tiến hành sửa lỗi hoặc thêm tính năng theo yêu cầu.

5.  **Xác minh (VERIFICATION)**: So sánh kết quả thực tế với `EXPECTED_RESULT`. Đối với Blender Addon, điều này bao gồm:
    - Đảm bảo addon vẫn đăng ký được mà không có lỗi.
    - Kiểm tra chức năng được sửa hoạt động đúng như mong đợi.

6.  **Cập nhật tài liệu**:
    - Cập nhật phiên bản trong `__init__.py` (biến `version` trong `bl_info`).
    - Cập nhật phiên bản trong `core/constants.py` (biến `ADDON_VERSION`).
    - Ghi lại thay đổi vào `UPDATE-LOG.md` theo format: `## [vX.X.X] - YYYY-MM-DD`.

7.  **Tự học (Self-Learning)**: Nếu lỗi xảy ra do một pattern xấu trong code, hãy tạo hoặc cập nhật rule trong `.gemini/rules/` để phòng tránh lỗi tương tự.

8.  **Xác minh cuối cùng**:
    Khuyến nghị chạy `/test` để đảm bảo bản cập nhật không làm hỏng cấu trúc dự án.

## Ví dụ sử dụng

```
/update
UPDATE: v2.5.5
PRIORITY: critical
CORE: Không sửa đổi panel_import_export và panel_jpg_converter.
CONTEXT: Hàm `get_idp_info` trong `panel_auto_rename/utils.py` trả về None khi model_id có khoảng trắng ở đầu/cuối.
ACTION: Chuẩn hóa model_id bằng `.strip()` trước khi tra cứu trong cache.
EXPECTED_RESULT: Hàm `get_idp_info("  ABC123  ")` trả về đúng dữ liệu cho "abc123".
```
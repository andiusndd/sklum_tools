---
description: Workflow to fix errors from a previous update and re-export
---

# /fix Command Workflow

Workflow này chuyên dùng để sửa nhanh các lỗi phát sinh (hotfix) sau một quy trình cập nhật.

## Tự động hỏi từng bước

Nếu user chỉ gửi `/fix` hoặc `@[/fix]` **MÀ KHÔNG CÓ NỘI DUNG ĐI KÈM**, Agent phải **HỎI LẦN LƯỢT** từng trường theo thứ tự sau:

1. **Bước 1**: Hỏi về `ERROR_MSG` - "Vui lòng cung cấp thông báo lỗi hoặc mô tả vấn đề bạn đang gặp phải."
2. **Bước 2**: Hỏi về `PRIORITY` - "Mức độ ưu tiên là gì? (critical / normal)" (Mặc định: critical)
3. **Bước 3**: Hỏi về `PLAN` - "Giải pháp dự kiến là gì?" (Nếu user có ý tưởng, nếu không Agent tự đề xuất)

## Cấu trúc Prompt đầy đủ

```
/fix
ERROR_MSG: [Thông báo lỗi / traceback]
PRIORITY: [critical]
PLAN: [Giải pháp đề xuất - optional]
```

## Quy trình xử lý

// turbo-all

1.  **Thu thập Bối cảnh (Quick Context)**:
    - **QUAN TRỌNG**: Đọc ngay `UPDATE-LOG.md` hoặc `task.md` để xem lần `/update` gần nhất đã thay đổi những gì.
    - Giả định rằng lỗi hiện tại liên quan trực tiếp đến những thay đổi đó.
    - Không cần scan toàn bộ dự án, tập trung vào các file vừa sửa đổi.

2.  **Phân tích Lỗi (Analyze)**:
    - Đối chiếu Traceback với code vừa sửa ở bước 1.
    - Xác định nhanh nguyên nhân (thường là typo, import sai, hoặc logic chưa cover hết edge case).

3.  **Lập kế hoạch (Plan)**:
    - Xác định file cần vá.
    - Đưa ra giải pháp nhanh gọn (Hotfix).
    - *Bỏ qua bước tạo `implementation_plan.md` trừ khi vấn đề quá phức tạp.*

4.  **Lưu trữ tri thức (Learn)**:
    - Nếu lỗi này là do thói quen code xấu (ví dụ: quên import), cập nhật Rule ngay.

5.  **Thực hiện sửa lỗi (Execute)**:
    - Sửa code trực tiếp.
    - Đảm bảo tính toàn vẹn của logic cũ.

6.  **Hoàn thiện (Finalize)**:
    - **Giữ nguyên version** (không tăng version số) để tránh lạm phát version cho lỗi nhỏ.
    - Cập nhật dòng log của version hiện tại trong `UPDATE-LOG.md` (Update mục Fixed/Changed).
    - `git add -A; git commit -m "Fix: [mô tả ngắn]"; git push github_repo main`

7.  **Tự động Export**:
    - **BẮT BUỘC** gọi script `_export_addon.py` để tạo bản vá ngay lập tức.

## Ví dụ sử dụng

User: `/fix`
ERROR: `AttributeError: ...`

Agent:
1. **Context**: Check Log -> Vừa thêm tính năng "Create Box". -> File liên quan: `operators.py`.
2. **Analyze**: Lỗi dòng 40. Biến chưa được khai báo.
3. **Execute**: Khai báo biến.
4. **Finalize**: Commit & Export zip.

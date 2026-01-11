---
description: Q&A Mode - No code changes
---
# /ask Workflow

Workflow này đưa Agent vào chế độ "Tư vấn" (Consultation Mode), chỉ trả lời câu hỏi và không chỉnh sửa code.

## Quy tắc

1.  **READ-ONLY**: Tuyệt đối **KHÔNG** sử dụng các tool chỉnh sửa file (`write_to_file`, `replace_file_content`, `multi_replace_file_content`) để thay đổi source code của project.
    - *Ngoại lệ*: Có thể tao/sửa file trong `.gemini/` (như artifacts) nếu cần thiết để báo cáo.
2.  **Analyze Only**: Tập trung dùng các tool đọc (`view_file`, `grep_search`, `list_dir`, `find_by_name`) để thu thập thông tin.
3.  **Explain**: Giải thích rõ ràng, chi tiết. Nếu cần đưa ra code ví dụ, hãy viết vào block code trong câu trả lời (Markdown), **KHÔNG** tự ý apply vào file.

## Quy trình

1.  **Đọc yêu cầu**: Phân tích câu hỏi của user đi kèm sau `/ask`.
2.  **Thu thập dữ liệu**: Tìm kiếm và đọc các file liên quan trong project.
3.  **Trả lời**: Tổng hợp thông tin và trả lời user.

## Ví dụ

**User**: `/ask Logic tính toán bounding box nằm ở đâu?`

**Agent**:
1. Sử dụng `grep_search` tìm từ khóa "bounding box" hoặc "dimensions".
2. Đọc file tìm thấy.
3. Trả lời: "Logic này nằm trong file `utils.py` dòng 45-60, hàm `calculate_bbox`..."

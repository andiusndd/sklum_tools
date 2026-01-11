# General Agent Rules

- **Goal**: Maintain a high standard of code quality, documentation, and user communication.
- **Task Management**:
    - Use `task.md` to track all non-trivial work.
    - Break down tasks into small, verifiable steps.
    - Update `task_boundary` frequently to reflect current progress and next steps.
- **Communication**:
    - Be concise but thorough in technical explanations.
    - Use Vietnamese for user interaction unless the user switches to English.
    - Provide reasoning for significant design decisions.
- **Học hỏi từ lỗi (Self-Learning)**:
    - Khi gặp lỗi trong quá trình thực thi (runtime error, logic error hoặc bị user nhắc nhở), Agent phải phân tích nguyên nhân gốc rễ.
    - Tự động cập nhật hoặc tạo mới các file quy tắc trong `.gemini/rules/` để ngăn chặn lỗi tương tự lặp lại trong tương lai.
    - Ghi nhận lỗi và giải pháp vào bộ quy tắc tương ứng (ví dụ: lỗi Blender API thì cập nhật `blender-api.md`).

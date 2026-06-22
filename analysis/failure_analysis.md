# Failure Analysis — Lab 18

**Nhóm:** Cá nhân
**Thành viên:** Nguyễn Thành Đạt

## RAGAS Scores

| Metric | Production Score |
|--------|------------------|
| Faithfulness | 0.7667 |
| Answer Relevancy | 0.7203 |
| Context Precision | 0.9500 |
| Context Recall | 0.8833 |

## Bottom-5 Failures

### #1
- **Question:** Bao lâu phải đổi mật khẩu một lần?
- **Worst metric:** faithfulness (0.00)
- **Error Tree:** Output sai (bịa thêm thông tin) → Context đúng nhưng nhiễu → Root cause: LLM tự hallucinate do prompt chưa đủ chặt chẽ, hoặc sinh ra câu trả lời nằm ngoài context.
- **Suggested fix:** Tighten prompt, giảm nhiệt độ (temperature=0.0) để LLM bám sát nội dung văn bản.

### #2
- **Question:** Một nhân viên Senior có 9 năm thâm niên được nghỉ bao nhiêu ngày phép năm và lương trong khoảng nào?
- **Worst metric:** answer_relevancy (0.00)
- **Error Tree:** Output không khớp câu hỏi → Context có thể chứa thông tin rời rạc → Root cause: Câu hỏi phức hợp (hỏi cả phép năm và lương), LLM Generator không tổng hợp đủ ý để trả lời trọn vẹn cả hai vế.
- **Suggested fix:** Cải thiện Prompt Template để hướng dẫn LLM phân rã câu hỏi nhiều vế và trả lời từng ý một.

### #3
- **Question:** Nhân viên tạm ứng 15 triệu, sau 20 ngày mới thanh toán. Bị phạt bao nhiêu?
- **Worst metric:** faithfulness (0.00)
- **Error Tree:** Output sai → Context có chứa thông tin thanh toán tạm ứng nhưng LLM tự suy diễn mức phạt → Root cause: LLM bị hallucination khi gặp tình huống tính toán ngày tháng/tiền phạt mà trong context không ghi rõ mức phạt cụ thể.
- **Suggested fix:** Thêm chỉ thị bắt buộc vào Prompt: "Nếu văn bản không có thông tin về tiền phạt, tuyệt đối không tự tính toán hay bịa ra con số".

### #4
- **Question:** Lương thử việc của nhân viên Junior mức cao nhất là bao nhiêu?
- **Worst metric:** faithfulness (0.00)
- **Error Tree:** Output sai số liệu → Root cause: LLM tự hallucinate hoặc nhầm lẫn giữa bảng lương Junior và Senior.
- **Suggested fix:** Sử dụng Structure-Aware Chunking tốt hơn cho bảng lương, đồng thời dùng Reranker mạnh hơn.

### #5
- **Question:** Nếu cần mua một chiếc laptop 30 triệu cho nhân viên mới, ai phê duyệt và cần gì từ phòng CNTT?
- **Worst metric:** faithfulness (0.50)
- **Error Tree:** Output sai một phần (trả lời được 1 vế) → Context thiếu thông tin phê duyệt → Root cause: Quy trình duyệt mua sắm nằm ở 2 đoạn văn khác nhau (trang trước và trang sau) nên chunking làm đứt mạch văn bản.
- **Suggested fix:** Áp dụng Hierarchical Chunking (gọi child chunk, trả về parent chunk) để LLM có trọn vẹn quy trình mua sắm.

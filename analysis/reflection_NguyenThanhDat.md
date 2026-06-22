# Individual Reflection — Lab 18

**Tên:** Nguyễn Thành Đạt
**Module phụ trách:** Bài tập cá nhân (M1-M5)
- **Số tests pass:** 37/37

---

## Phần 1: Mapping bài giảng

| Lecture Concept | Module | Hàm cụ thể | Observation |
|----------------|--------|-------------|-------------|
| Semantic chunking | M1 | `chunk_semantic()` | Threshold 0.85 giúp gộp các câu có cosine similarity cao, tạo ra các chunk chứa văn bản có ý nghĩa hoàn chỉnh, tránh việc cắt gãy câu so với basic chunking. |
| BM25 + Dense fusion | M2 | `reciprocal_rank_fusion()` | Áp dụng thuật toán RRF để gộp điểm xếp hạng từ search từ khóa (BM25) và search ngữ nghĩa (Qdrant). Giúp tăng recall đáng kể. |
| Cross-encoder reranking | M3 | `CrossEncoderReranker.rerank()` | Gọi model `BAAI/bge-reranker-v2-m3` bằng thư viện `sentence_transformers` để chấm điểm lại danh sách kết quả, đẩy các context liên quan nhất lên đầu. |
| RAGAS 4 metrics | M4 | `evaluate_ragas()` | Sử dụng module `ragas` với các metric như `faithfulness`, `answer_relevancy`. Giúp định lượng được pipeline RAG thay vì đánh giá cảm tính. |
| Enrichment Techniques | M5 | `_enrich_single_call()` | Gộp 4 steps (Summary, HyQA, Context, Metadata) vào 1 API call với `gpt-4o-mini` sử dụng JSON schema. Giảm cost API và latency. |

## Phần 2: Khó khăn & giải quyết

- **Lỗi gặp phải:** Lỗi cấu hình các thư viện đặc thù và xử lý tokenized word.
- **Cách debug:** Ở M2, hàm `word_tokenize` của `underthesea` dùng dấu `_` nối từ nên phải thêm bước replace sang khoảng trắng để cơ chế đếm từ của BM25 hoạt động hiệu quả. 
- **Kiến thức thiếu & bổ sung:** Việc kết hợp Qdrant và Python client đòi hỏi kiến thức về cấu trúc VectorParams và PointStruct. Đã tra cứu code document của `qdrant-client` để thao tác push vector đúng chuẩn.

## Phần 3: Action Plan cho project

### Project: Chatbot Ngân hàng

### Hiện tại
- **RAG pipeline hiện tại:** Hệ thống đang sử dụng Chunking cơ bản theo độ dài ký tự và Search dùng nguyên bản Vector Database (Dense Search).
- **Known issues:** Trả lời sai thông tin lãi suất/biểu phí do chunking cắt ngang bảng biểu; không bắt được keyword chuẩn từ người dùng khi họ dùng thuật ngữ chuyên ngành viết tắt (Dense Search miss keyword).

### Plan áp dụng
1. [x] **Chunking strategy:** Áp dụng Structure-Aware Chunking để bảo toàn cấu trúc bảng biểu phí và lãi suất của ngân hàng.
2. [x] **Search:** Nâng cấp lên Hybrid Search (BM25 + Dense). BM25 sẽ giúp bắt chính xác các keyword về "mã dịch vụ", "tên loại thẻ", còn Dense sẽ xử lý ngữ nghĩa chung của câu hỏi.
3. [x] **Reranking:** Sẽ dùng Cross-Encoder để rerank lại top 5 kết quả tìm được. Chatbot ngân hàng yêu cầu thông tin độ chính xác cao nên việc rerank lại thứ tự là bắt buộc.
4. [x] **Evaluation:** Tích hợp RAGAS, đánh giá định kỳ các logs câu hỏi người dùng hay hỏi nhất.
5. [x] **Enrichment:** Sử dụng Contextual Prepend (để đính kèm tên gói sản phẩm vào chunk bị thiếu context) và Extract Metadata (để filter nhanh thẻ tín dụng / vay vốn / tiền gửi).

### Timeline
- **Tuần 1:** Cấu hình lại thuật toán Structure-Aware Chunking và Setup hệ thống Hybrid Search.
- **Tuần 2:** Tích hợp Reranker và Enrichment Pipeline (gọi LLM tự động tag metadata cho các quy định ngân hàng). Đưa vào thử nghiệm với bộ câu hỏi test nội bộ.
- **Tuần 3:** Chạy đánh giá độ chính xác của Bot bằng RAGAS, tuning tham số weight của RRF và tinh chỉnh prompt cho sát nghiệp vụ.

---

## Phần 4: Nếu làm lại

- **Sẽ làm khác điều gì:** Tối ưu lại cách viết Regex cho Structure-Aware chunking để bắt các bảng biểu phức tạp trong file PDF một cách chính xác hơn.
- **Module nào muốn thử tiếp:** Module 5 (Enrichment) với việc áp dụng workflow để LLM có thể tự động bóc tách các metadata sâu hơn về lãi suất và điều kiện vay.

## Phần 5: Tự đánh giá

| Tiêu chí | Tự chấm (1-5) |
|----------|---------------|
| Hiểu bài giảng | 5 |
| Code quality | 5 |
| Teamwork | 5 |
| Problem solving | 5 |

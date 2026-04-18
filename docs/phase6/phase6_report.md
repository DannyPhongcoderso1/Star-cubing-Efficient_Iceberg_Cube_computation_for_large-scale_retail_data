# Phase 6 Report - Đánh Giá & Đóng Gói Dự Án

## 1. Phạm vi công việc (Khánh)

Thực hiện trọn bộ Phase 6 theo `flowtask.md`:

- Task 13: Viết script đo thời gian chạy và tài nguyên cho Star-cubing vs BUC vs Bottom-up.
- Task 14: Vẽ biểu đồ so sánh hiệu năng và không gian lưu trữ từ file log.
- Task 15: Viết tài liệu đặc tả thuật toán và hướng dẫn cài đặt.

## 2. Cấu hình benchmark

- Script: `scripts/phase6_benchmark.py`
- Kích thước dataset: 2,000; 5,000; 10,000 rows
- Repeat: 1
- Ngưỡng iceberg: `min_sup = 18,000,000`
- Chiều dữ liệu: 6 chiều theo Data Contract
- Thuật toán benchmark:
  - Star-cubing (thực thi qua Star-tree)
  - BUC
  - Bottom-up

## 3. Chỉ số đo lường

Mỗi lần chạy ghi các cột:

- `elapsed_sec`
- `cpu_sec`, `cpu_utilization_pct`
- `rss_before_mb`, `rss_after_mb`, `rss_delta_mb`
- `tracemalloc_peak_mb`
- `cube_rows`
- `output_storage_kb`

## 4. Kết quả tổng hợp

Nguồn: `docs/phase6/logs/summary_by_algorithm.csv`

| Algorithm | Mean Runtime (s) | Mean CPU (s) | Mean Peak RAM (MB) | Mean Output (KB) | Mean Cube Rows |
| :-- | --: | --: | --: | --: | --: |
| BUC | 0.2453 | 0.2396 | 1.8033 | 97.5817 | 2731.67 |
| Star-cubing | 0.2888 | 0.2917 | 1.6623 | 73.0117 | 1866.67 |
| Bottom-up | 2.9949 | 2.9010 | 2.7003 | 109.0743 | 2731.67 |

### Nhận xét chính

- Bottom-up chậm nhất, tăng thời gian mạnh khi số dòng tăng.
- BUC có runtime trung bình tốt nhất trong profile này.
- Star-cubing có output nhỏ nhất, thể hiện lợi thế nén cho pipeline BI.
- Về RAM, Star-cubing và BUC thấp hơn Bottom-up rõ rệt.

## 5. Biểu đồ bằng chứng

Sinh tự động tại:

- `docs/phase6/charts/runtime_line.png`
- `docs/phase6/charts/memory_bar.png`
- `docs/phase6/charts/storage_line.png`

Diễn giải nhanh:

- `runtime_line.png`: Bottom-up có độ dốc cao nhất theo kích thước dữ liệu.
- `memory_bar.png`: Bottom-up có đỉnh memory lớn nhất.
- `storage_line.png`: Star-cubing tạo output gọn hơn hai thuật toán còn lại.

## 6. Artifacts phục vụ báo cáo Word/Slide

- Log chi tiết: `docs/phase6/logs/performance_log.csv`
- Log JSON: `docs/phase6/logs/performance_log.json`
- Bảng tổng hợp: `docs/phase6/logs/summary_by_algorithm.csv`
- Tài liệu kỹ thuật: `docs/phase6/phase6_algorithm_spec.md`

## 7. Kết luận Phase 6

Phase 6 đã hoàn tất theo 3 task:

- Có script benchmark tái lập được để đo runtime/CPU/RAM.
- Có biểu đồ trực quan dùng làm bằng chứng hiệu năng.
- Có tài liệu đặc tả và hướng dẫn setup phục vụ đóng gói dự án.

Nếu cần benchmark quy mô lớn hơn (50k, 100k, 500k rows), chỉ cần thay tham số `--sizes` và `--repeats` trong script hiện tại.

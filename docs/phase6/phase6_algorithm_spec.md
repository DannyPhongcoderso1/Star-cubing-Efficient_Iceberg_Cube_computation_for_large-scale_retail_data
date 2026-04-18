# Phase 6 - Đặc Tả Thuật Toán & Hướng Dẫn Cài Đặt

## Mục tiêu

Tài liệu này đóng vai trò Task 15 cho nhóm Khánh:

- Đặc tả cách benchmark 3 hướng tiếp cận: Star-cubing (Star-tree), BUC, Bottom-up.
- Chuẩn hóa quy trình cài đặt/chạy để tái lập số liệu thực nghiệm.
- Mô tả luồng dữ liệu từ input tổng hợp đến log/charts dùng cho báo cáo Word.

## Data Contract dùng cho benchmark

- Dữ liệu đầu vào: số nguyên đã mã hóa theo đúng thứ tự chiều.
- Thứ tự chiều: `Time_Period`, `Region`, `City`, `Category`, `Customer_Type`, `Payment_Method`.
- Measure:
  - `total_sales` (float) dùng làm điều kiện iceberg.
  - `count_txn` (int) dùng làm chỉ số số giao dịch.
- Ngưỡng cắt tỉa: `min_sup` áp dụng duy nhất trên `total_sales`.
- Giá trị roll-up: dùng chuỗi `'ALL'`.

## Thiết kế giải thuật trong Phase 6

### 1) Star-cubing (Star-tree)

- Dữ liệu nạp vào cây tiền tố theo thứ tự chiều.
- Tại mỗi node cộng dồn `total_sales` và `count_txn`.
- Khi tổng hợp, các prefix hoặc value hỗ trợ thấp được cuộn thành `'ALL'`.
- Ưu điểm trong benchmark: kết quả có xu hướng nén tốt, output nhỏ hơn.

### 2) BUC

- Chia dữ liệu theo chiều hiện tại, đệ quy xuống chiều tiếp theo.
- Mỗi mức có thêm nhánh roll-up `'ALL'`.
- Nhánh `total_sales < min_sup` bị prune ngay để giảm không gian tìm kiếm.
- Ưu điểm trong benchmark: runtime ổn trên dataset vừa, tận dụng pruning theo phân vùng.

### 3) Bottom-up

- Mỗi transaction sinh toàn bộ tổ hợp cuboid (`2^d`, với `d = 6`).
- Gom nhóm toàn cục bằng key tuple và lọc theo `min_sup` ở cuối.
- Nhược điểm: nhiều trạng thái trung gian, tốn thời gian và RAM hơn khi dữ liệu lớn dần.

## Luồng thực thi benchmark

1. Script tạo dữ liệu synthetic theo Data Contract, có tương quan nghiệp vụ:
   - VIP có xác suất cao mua Electronics.
2. Chạy lần lượt 3 thuật toán trên cùng một batch dữ liệu.
3. Đo các metric:
   - `elapsed_sec`
   - `cpu_sec`, `cpu_utilization_pct`
   - `rss_before_mb`, `rss_after_mb`, `rss_delta_mb`
   - `tracemalloc_peak_mb`
   - `cube_rows`, `output_storage_kb`
4. Ghi log vào `docs/phase6/logs`.
5. Vẽ chart vào `docs/phase6/charts`.

## Hướng dẫn cài đặt

### Yêu cầu môi trường

- Python >= 3.14 (hoặc 3.10+ nếu tương thích dependency).
- Pip package manager.

### Cài dependency

```bash
pip install -r requirements.txt
```

### Chạy benchmark mặc định

```bash
python scripts/phase6_benchmark.py --sizes 2000,5000,10000 --repeats 1 --min-sup 18000000
```

### Chạy benchmark mở rộng

```bash
python scripts/phase6_benchmark.py --sizes 5000,10000,20000 --repeats 2 --min-sup 25000000 --seed 20260418
```

## Đầu ra chuẩn dùng cho báo cáo

- `docs/phase6/logs/performance_log.csv`
- `docs/phase6/logs/performance_log.json`
- `docs/phase6/logs/summary_by_algorithm.csv`
- `docs/phase6/charts/runtime_line.png`
- `docs/phase6/charts/memory_bar.png`
- `docs/phase6/charts/storage_line.png`

## Kết luận kỹ thuật ngắn

- Với profile hiện tại, Bottom-up là baseline đơn giản nhưng chậm và tốn bộ nhớ nhất.
- BUC và Star-tree đều hiệu quả hơn rõ rệt về runtime.
- Star-tree có lợi thế nén kết quả đầu ra, phù hợp mục tiêu Iceberg Cube read-heavy cho BI.

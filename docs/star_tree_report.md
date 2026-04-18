# Star-tree Report

## Mục tiêu

Tài liệu này mô tả cách triển khai Star-tree cho bài toán Iceberg Cube trên dữ liệu bán lẻ đã được tiền xử lý và nạp toàn bộ vào RAM.

## Thiết kế cấu trúc dữ liệu

- Mỗi node được cài bằng `__slots__` để loại bỏ `__dict__` và giảm overhead bộ nhớ.
- `StarNode` lưu đúng 5 thuộc tính bắt buộc: `attr_name`, `attr_value`, `children`, `total_sales`, `count_txn`.
- `children` là một dictionary ánh xạ từ giá trị chiều sang node con, giúp truy cập O(1) theo từng bước chèn.
- `StarTree` giữ node gốc, thứ tự chiều chuẩn hóa và ngưỡng `min_sup` để phục vụ pruning.

## Luồng chèn giao dịch

Khi gọi `insert_transaction`, cây đi từ gốc xuống lá theo đúng thứ tự chiều đã cho. Ở mỗi node:

- `total_sales` được cộng dồn bằng doanh thu của giao dịch.
- `count_txn` được cộng dồn bằng số lượng giao dịch.
- Bảng đếm tổng theo từng chiều được cập nhật để xác định giá trị nào có hỗ trợ toàn cục thấp.
- Nếu tổng doanh thu tích lũy của prefix hiện tại nhỏ hơn `min_sup`, prefix đó được đánh dấu là low-support để sau này khi sinh cube sẽ được nén thành `'ALL'`.

Thiết kế này cho phép cây vừa là cấu trúc nén vừa là nơi giữ đủ thông tin tổng hợp cho bước xuất cube.

## Simultaneous Aggregation

Hàm `simultaneous_aggregation` duyệt các leaf path theo DFS, sau đó:

1. Nén các prefix yếu thành `'ALL'`.
2. Nén các giá trị có hỗ trợ toàn cục thấp thành `'ALL'` ở đúng chiều (không xóa các chiều phía sau).
3. Mở rộng mỗi path lá thành toàn bộ tổ hợp roll-up hợp lệ.
4. Gộp kết quả bằng key tuple để tránh trùng cuboid giữa nhiều leaf.
5. Lọc ra các cuboids có `total_sales >= min_sup`.

Với 6 chiều, số tổ hợp tối đa cho một leaf là $2^6 = 64$, đủ nhỏ để giữ code đơn giản và dễ kiểm thử.

## Hướng dẫn sử dụng

Ví dụ tối thiểu để xây cây, nạp dữ liệu và lấy danh sách cuboid:

```python
from src.algorithm.star_tree import StarTree

tree = StarTree(min_sup=100.0)

transactions = [
	[0, 1, 2, 1, 0, 3],
	[0, 1, 2, 1, 1, 2],
]
sales_values = [120.0, 80.0]
count_values = [1, 1]

for transaction, sales, count in zip(transactions, sales_values, count_values):
	tree.insert_transaction(transaction, sales=sales, count=count)

cube_rows = tree.simultaneous_aggregation()
```

Ghi chú:

- Mỗi `transaction` phải đủ 6 chiều theo đúng thứ tự trong hợp đồng dữ liệu.
- Có thể truyền `dimension_names` khi khởi tạo nếu muốn đổi tên chiều.
- Kết quả trả về là danh sách dictionary, sẵn sàng map ngược để nạp vào DB.

## Tối ưu hóa bộ nhớ

- Dùng `__slots__` cho `StarNode` để giảm đáng kể memory overhead trên mỗi node.
- Không lưu chuỗi trung gian trong quá trình duyệt đệ quy; chỉ giữ path hiện tại bằng list ngắn hạn.
- Không in log trong vòng lặp lớn hay traversal đệ quy.
- Kết quả cube được gom trong dictionary theo key chuẩn hóa, tránh giữ dữ liệu trùng lặp.

## Chiến lược kiểm thử

Pytest bao phủ các kịch bản chính:

- Khởi tạo cây và kiểm tra node gốc dùng slots.
- Nhánh có doanh thu đủ lớn vẫn được giữ nguyên ở output.
- Nhánh có doanh thu thấp được nén thành `'ALL'` khi tổng hợp cube.
- Dữ liệu synthetic hàng nghìn dòng vẫn được nạp và tổng hợp thành công.

## Ghi chú triển khai

Triển khai này ưu tiên tính đúng đắn, tính ổn định và khả năng kiểm thử trước. Nếu cần nâng cấp cho dữ liệu lớn hơn nữa, bước tiếp theo là tách riêng chỉ mục support theo từng chiều và tối ưu chiến lược sinh cuboid để giảm số trạng thái trung gian.
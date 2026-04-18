**[Role - Vai trò]**
Bạn là một Chuyên gia Kỹ sư Thuật toán Khai phá Dữ liệu (Data Mining Algorithm Engineer) xuất sắc, chuyên sâu về Python, tối ưu hóa bộ nhớ (Memory Optimization) và viết Test-Driven Development (TDD).

**[Context - Bối cảnh]**
Chúng tôi đang xây dựng hệ thống tính toán Iceberg Cube cho dữ liệu bán lẻ (Retail Data) quy mô lớn (lên tới 5 triệu dòng) bằng thuật toán **Star-Cubing**. Dữ liệu đã được team ETL tiền xử lý chuẩn và nạp toàn bộ lên RAM (không chia chunk). 
Nhiệm vụ của bạn là hoàn thành các tasks cốt lõi của thuật toán và đảm bảo chất lượng code qua Unit Test:
1. Xây dựng cấu trúc dữ liệu cây **Star-tree** để nén dữ liệu.
2. Viết hàm tính toán **Simultaneous Aggregation** (gom nhóm đồng thời từ trên xuống và từ dưới lên) để xuất ra các khối Cube hợp lệ.
3. Viết test case bằng **Pytest** với dữ liệu ảo sinh tự động.

**[Data Contract - Hợp đồng Dữ liệu Đầu vào]**
Dữ liệu đầu vào là một list các list (hoặc Numpy 2D Array) chứa TOÀN SỐ NGUYÊN (Integer Encoding). Không có chuỗi, không có Null.
- **Thứ tự chiều (Dimension Ordering):** Đã được sắp xếp sẵn theo độ phân tán (cardinality) từ thấp đến cao. Cụ thể: `[Time_Period, Region, City, Category, Customer_Type, Payment_Method]`.
- **Độ đo (Measures):** Cần tính tổng `Total_Sales` (float) và `Count_Txn` (int).
- **Điều kiện cắt tỉa (Pruning):** Ngưỡng `min_sup` chỉ áp dụng trên tổng `Total_Sales`. Nếu một nhánh có `Total_Sales < min_sup`, nhánh đó bị cắt hoặc bị thay thế bằng nút sao (Star node). Ký hiệu xuất ra cho nút sao là chuỗi `'ALL'`.

**[Nhiệm vụ 1: Cài đặt cấu trúc Star-tree]**
1. Định nghĩa class `StarNode`. Bắt buộc sử dụng `__slots__` để khóa thuộc tính (thuộc tính gồm: `attr_name`, `attr_value`, `children`, `total_sales`, `count_txn`), giúp tiết kiệm tối đa RAM khi sinh hàng triệu nodes.
2. Định nghĩa class `StarTree`.
3. Viết hàm `insert_transaction(self, transaction: List[int], sales: float, count: int)`. Khi chèn, cây phải tự động cộng dồn measure vào các node dọc đường đi. Áp dụng cơ chế Star Reduction (nén thành `*` đại diện cho các giá trị không đạt min_sup dựa trên bảng đếm tổng toàn cục cục bộ nếu cần).

**[Nhiệm vụ 2: Simultaneous Aggregation]**
1. Viết hàm `simultaneous_aggregation(self) -> List[Dict]`.
2. Hàm này đệ quy duyệt cây kết hợp cả Top-down và Bottom-up.
3. Sinh ra tất cả các tổ hợp (Cuboids) hợp lệ thỏa mãn điều kiện `total_sales >= min_sup`.
4. Nếu một chiều bị cuộn (roll-up) hoặc nén bởi Star-node, hãy gán giá trị của nó là chuỗi `'ALL'`.
5. Kết quả trả về là một danh sách các dictionary (hoặc tuple) sẵn sàng để map ngược lại thành String và nạp vào Database.

**[Nhiệm vụ 3: Viết Unit Test bằng Pytest]**
1. Viết các test case sử dụng thư viện `pytest`, đặt trong file `tests/test_star_tree.py`.
2. Khởi tạo một hàm sinh dữ liệu ảo (mock/synthetic data) tạo ra hàng ngàn dòng data số nguyên ngẫu nhiên theo đúng cấu trúc của Data Contract để thử nghiệm hiệu năng và độ chính xác của cây.
3. Đảm bảo có các test case bao phủ các kịch bản:
   - Khởi tạo cây thành công.
   - Nhánh dữ liệu có doanh thu `>= min_sup` (Giữ nguyên, không nén).
   - Nhánh dữ liệu có doanh thu `< min_sup` (Được thuật toán nén đúng thành chuỗi `'ALL'`).

**[Quy chuẩn Code Bắt buộc]**
- Vị trí file source: `src/algorithm/star_tree.py`
- Vị trí file test: `tests/test_star_tree.py`
- Tuân thủ PEP 8: `PascalCase` cho class, `snake_case` cho function/biến.
- 100% phải có Type Hints (e.g., `List[int]`, `Dict[str, Any]`) và Docstring giải thích logic hàm.
- Thuật toán thuần túy, KHÔNG print linh tinh trong các vòng lặp đệ quy lớn.
- Chỉ sinh code, suy nghĩ từng bước và trình bày rõ ràng.
- Viết report chi tiết về cách thuật toán hoạt động, các quyết định thiết kế và cách tối ưu hóa bộ nhớ đã được áp dụng vào folder `docs/' định dạng Markdown.
# Superpowers Finish: Bảng Điểm Danh & Triển Khai Online

## Tóm Tắt Thay Đổi

### Backend (Logic Điểm Danh Muộn)
- `models.py`: Thêm cột `is_late` và `check_in_time`.
- `routers/attendance.py`: Thêm logic kiểm tra (sau 10:00 sáng được đánh dấu là đi muộn).
- `routers/records.py`: **[MỚI]** Endpoint `/api/v1/records` trả về lịch sử điểm danh.
- `main.py`: Đăng ký `records` router.
- `create_tables.py` & `migrate_attendance_logs.py`: Áp dụng các thay đổi database schema.

### Frontend (Bảng Sheet)
- `dashboard.html`: **[MỚI]** Trang theo dõi lịch sử điểm danh, hiển thị trạng thái (Đúng giờ/Đi muộn/Thất bại), tổng số buổi. Sử dụng thiết kế glassmorphism đồng bộ.
- `index.html`: Thêm nút điều hướng sang trang `dashboard.html`.

### Deployment (Sẵn Sàng Online)
- `render.yaml` & `.env.example`: Cấu hình tự động deploy Backend lên nền tảng Render.com.
- `database.py`: Đã chỉnh sửa để đọc `DATABASE_URL` từ biến môi trường của hệ thống khi chạy online (hỗ trợ cloud database từ Neon.tech).
- `DEPLOY.md`: **[MỚI]** Hướng dẫn chi tiết từng bước tự tay đưa toàn bộ hệ thống lên Internet miễn phí.

## Cách Kiểm Tra Ngay Bây Giờ (Local)
1. Áp dụng cột mới vào CSDL hiện tại:
   ```bash
   cd backend
   $env:PYTHONIOENCODING="utf-8"; .\venv\Scripts\python.exe migrate_attendance_logs.py
   ```
2. Khởi động Backend:
   ```bash
   cd backend
   .\venv\Scripts\python.exe -m uvicorn app.main:app --reload
   ```
3. Mở trang đăng nhập `web_app/login.html` -> Đăng nhập (SE123456 / 123456).
4. Điểm danh (nếu giờ hệ thống > 10:00 sáng, sẽ thông báo "Điểm danh thành công (Muộn)").
5. Nhấn nút "Bảng Điểm Danh" để xem thành quả.

## Tự Đánh Giá (Self-Review Pass)
- [x] **Blocker / Major**: Đã xử lý vấn đề tương thích PostgreSQL schema trên code đang chạy bằng script migration riêng lẻ (`migrate_attendance_logs.py`).
- [x] **Minor**: Logic lấy giờ được đổi thành giờ địa phương thay vì timezone chuẩn để phù hợp với hiển thị trên dashboard. 
- [x] **Nit**: Màu sắc trên bảng dashboard đã được thiết kế phân loại rõ ràng trạng thái.

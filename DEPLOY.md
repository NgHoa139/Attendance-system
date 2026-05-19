# Hướng Dẫn Triển Khai Hệ Thống Điểm Danh Online Miễn Phí

Hệ thống của bạn có thể chạy online 100% miễn phí bằng cách sử dụng 3 dịch vụ: Neon (Database), Render (Backend) và Netlify (Frontend).

## Bước 1: Khởi tạo Database trên Neon.tech (PostgreSQL Miễn Phí)
1. Truy cập [Neon.tech](https://neon.tech/) và đăng ký tài khoản (dùng Google hoặc GitHub).
2. Tạo một project mới (ví dụ: `attendance-db`).
3. Trong màn hình Dashboard, tìm phần **Connection Details**.
4. Copy chuỗi kết nối **Connection String** (nó trông giống như `postgres://user:pass@ep-cool-snowflake...neon.tech/neondb`).
5. **Lưu chuỗi này lại** (đây là `DATABASE_URL` của bạn).

## Bước 2: Đẩy Code Lên GitHub
Cả Render và Netlify đều triển khai dễ dàng nhất qua GitHub.
1. Tạo một repository mới trên GitHub (ví dụ: `attendance-system`).
2. Mở Terminal/PowerShell tại thư mục `Project` của bạn và chạy:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/TÊN_CỦA_BẠN/attendance-system.git
   git push -u origin main
   ```

## Bước 3: Triển Khai Backend Lên Render.com
1. Truy cập [Render.com](https://render.com/) và đăng nhập bằng GitHub.
2. Bấm nút **New** -> Chọn **Web Service**.
3. Kết nối với repository `attendance-system` bạn vừa tạo.
4. Render sẽ tự động đọc file `backend/render.yaml` (bạn có thể cần trỏ Root Directory là `backend`).
5. Trong phần **Environment Variables**, thêm các biến sau:
   - `DATABASE_URL`: Dán chuỗi kết nối Neon bạn đã copy ở Bước 1.
   - `SECRET_KEY`: Bất kỳ chuỗi ngẫu nhiên nào.
   - `AES_KEY`: `my_aes_secret_key_32_bytes_lengt` (Hoặc đổi trên cả frontend/backend nếu muốn bảo mật).
   - `AES_IV`: `my_aes_16bytes_i` (Hoặc đổi).
6. Bấm **Create Web Service**. 
7. Chờ vài phút để Render cài đặt và chạy. Khi xong, bạn sẽ có URL của backend (ví dụ: `https://attendance-api-xyz.onrender.com`).

## Bước 4: Cập Nhật URL Backend Cho Frontend
1. Mở các file `web_app/app.js`, `web_app/login.js` và `web_app/dashboard.html`.
2. Sửa dòng cấu hình URL từ `localhost` sang URL Render của bạn:
   ```javascript
   // Đổi từ:
   const API_BASE_URL = "http://localhost:8000/api/v1";
   
   // Thành:
   const API_BASE_URL = "https://attendance-api-xyz.onrender.com/api/v1";
   ```
3. Lưu các file và đẩy thay đổi lên GitHub:
   ```bash
   git add web_app/
   git commit -m "Update API URL for production"
   git push
   ```

## Bước 5: Triển Khai Frontend Lên Netlify
1. Truy cập [Netlify.com](https://www.netlify.com/) và đăng nhập.
2. Bạn có 2 cách rất dễ:
   - **Cách 1 (Kéo thả):** Bấm vào "Add new site" -> "Deploy manually". Mở thư mục `Project`, nắm kéo thả thư mục `web_app` vào vùng cài đặt của Netlify. Xong!
   - **Cách 2 (Qua GitHub):** Bấm "Import from Git" -> Chọn repository `attendance-system` -> Phần **Base directory** nhập `web_app` -> Bấm Deploy.
3. Netlify sẽ cung cấp cho bạn một URL công khai (ví dụ: `https://fpt-attendance.netlify.app`).

## Hoàn Tất! 🎉
Bây giờ bất kỳ sinh viên nào cũng có thể truy cập URL Netlify của bạn bằng điện thoại hoặc máy tính để đăng nhập và thực hiện điểm danh.

Dữ liệu sẽ được lưu an toàn trên Neon Cloud Database!

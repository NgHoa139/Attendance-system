import psycopg2
import bcrypt
from datetime import datetime, timedelta

import os

print("Starting insert_dummy.py...")

# Connect to database (Neon if DATABASE_URL is set, else localhost)
db_url = os.getenv("DATABASE_URL")
print(f"Using DATABASE_URL: {'Yes' if db_url else 'No (using localhost)'}")
if db_url:
    conn = psycopg2.connect(db_url)
else:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="attendance_db",
        user="postgres",
        password="hoa13092005"
    )
cursor = conn.cursor()

# Hash mật khẩu mặc định cho sinh viên test
hashed_password = bcrypt.hashpw("123456".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Thêm User
try:
    cursor.execute("""
    INSERT INTO users (id, student_code, device_uuid, full_name, hashed_password)
    VALUES ('f9e0eb9b-0000-4000-8000-000000000000', 'SE123456', 'WEB-BROWSER-UUID-12345', 'Nguyễn Văn Test', %s)
    ON CONFLICT (student_code) DO UPDATE SET hashed_password = EXCLUDED.hashed_password;
    """, (hashed_password,))
    print("User inserted/updated.")
except Exception as e:
    print("User insert error:", e)

# Thêm Session
# base_bssid dùng làm base_ip cho web, set thành 127.0.0.1
try:
    cursor.execute("""
    INSERT INTO sessions (id, name, start_time, end_time, base_lat, base_lon, base_bssid)
    VALUES ('2441a18c-3965-4f32-bb9f-6821d3f9e9ba', 'Lớp Nhập môn Lập trình', 
            %s, %s, 21.013, 105.526, '127.0.0.1')
    ON CONFLICT (id) DO NOTHING;
    """, (datetime.now() - timedelta(hours=1), datetime.now() + timedelta(hours=1)))
    print("Session inserted.")
except Exception as e:
    print("Session insert error:", e)

conn.commit()
cursor.close()
conn.close()
print("Dummy data inserted successfully.")

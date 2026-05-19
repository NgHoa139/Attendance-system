import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="attendance_db",
    user="postgres",
    password="hoa13092005"
)

cursor = conn.cursor()

print("Đang tạo extension uuid-ossp...")
cursor.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

print("Đang tạo bảng users...")
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_code VARCHAR(20) UNIQUE NOT NULL,
    device_uuid VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    hashed_password VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
""")

print("Đang tạo bảng sessions...")
cursor.execute("""
CREATE TABLE IF NOT EXISTS sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    base_lat DOUBLE PRECISION NOT NULL,
    base_lon DOUBLE PRECISION NOT NULL,
    base_bssid VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
""")

print("Đang tạo bảng attendance_logs...")
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    session_id UUID REFERENCES sessions(id),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(20) NOT NULL,
    lat DOUBLE PRECISION,
    lon DOUBLE PRECISION,
    bssid VARCHAR(50),
    check_in_time TIMESTAMP WITH TIME ZONE,
    is_late BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()
cursor.close()
conn.close()

print("")
print("========================================")
print("  Tạo bảng database THÀNH CÔNG!")
print("  - users")
print("  - sessions")
print("  - attendance_logs")
print("========================================")

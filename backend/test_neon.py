import psycopg2
import bcrypt
from datetime import datetime, timedelta

db_url = "postgresql://neondb_owner:npg_Otx98CWnbdLI@ep-cold-dew-aqjf2kqz.c-8.us-east-1.aws.neon.tech/neondb?sslmode=require"
print("Connecting to Neon...")
try:
    conn = psycopg2.connect(db_url, connect_timeout=10)
    cursor = conn.cursor()
    print("Connected successfully!")
    
    hashed_password = bcrypt.hashpw("123456".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    print("Hashing done. Inserting user...")
    
    cursor.execute("""
    INSERT INTO users (id, student_code, device_uuid, full_name, hashed_password)
    VALUES ('f9e0eb9b-0000-4000-8000-000000000000', 'SE123456', 'WEB-BROWSER-UUID-12345', 'Nguyễn Văn Test', %s)
    ON CONFLICT (student_code) DO UPDATE SET hashed_password = EXCLUDED.hashed_password;
    """, (hashed_password,))
    print("User inserted/updated.")
    
    cursor.execute("""
    INSERT INTO sessions (id, name, start_time, end_time, base_lat, base_lon, base_bssid)
    VALUES ('2441a18c-3965-4f32-bb9f-6821d3f9e9ba', 'Lớp Nhập môn Lập trình', 
            %s, %s, 21.013, 105.526, '127.0.0.1')
    ON CONFLICT (id) DO NOTHING;
    """, (datetime.now() - timedelta(hours=1), datetime.now() + timedelta(hours=1)))
    print("Session inserted.")
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Dummy data inserted successfully to NEON.")
except Exception as e:
    print(f"Error: {e}")

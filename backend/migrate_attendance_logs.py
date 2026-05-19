import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="attendance_db",
    user="postgres",
    password="hoa13092005"
)
cursor = conn.cursor()

print("Adding check_in_time and is_late columns to attendance_logs table...")
try:
    cursor.execute("ALTER TABLE attendance_logs ADD COLUMN IF NOT EXISTS check_in_time TIMESTAMP WITH TIME ZONE;")
    cursor.execute("ALTER TABLE attendance_logs ADD COLUMN IF NOT EXISTS is_late BOOLEAN DEFAULT FALSE;")
    conn.commit()
    print("Done! Columns added successfully.")
except Exception as e:
    print(f"Error: {e}")
finally:
    cursor.close()
    conn.close()

import psycopg2
import os

db_url = "postgresql://neondb_owner:npg_Otx98CWnbdLI@ep-cold-dew-aqjf2kqz.c-8.us-east-1.aws.neon.tech/neondb?sslmode=require"
try:
    conn = psycopg2.connect(db_url, connect_timeout=10)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM attendance_logs;")
    conn.commit()
    cursor.close()
    conn.close()
    print("All attendance logs cleared successfully.")
except Exception as e:
    print(f"Error: {e}")

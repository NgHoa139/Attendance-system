import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="attendance_db",
    user="postgres",
    password="hoa13092005"
)
cursor = conn.cursor()

print("Adding hashed_password column to users table...")
cursor.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS hashed_password VARCHAR(255);")
conn.commit()
print("Done! Column added successfully.")

cursor.close()
conn.close()

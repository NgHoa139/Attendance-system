from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Lấy URL từ biến môi trường (khi deploy), mặc định dùng localhost (khi test)
DATABASE_URL_ENV = os.getenv("DATABASE_URL")
if DATABASE_URL_ENV:
    # SQLAlchemy 1.4+ requires postgresql:// instead of postgres://
    if DATABASE_URL_ENV.startswith("postgres://"):
        DATABASE_URL_ENV = DATABASE_URL_ENV.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URL = DATABASE_URL_ENV
else:
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:hoa13092005@localhost/attendance_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

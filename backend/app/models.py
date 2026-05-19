from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_code = Column(String(20), unique=True, index=True, nullable=False)
    device_uuid = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Session(Base):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    base_lat = Column(Float, nullable=False)
    base_lon = Column(Float, nullable=False)
    base_bssid = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class AttendanceLog(Base):
    __tablename__ = "attendance_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"))
    timestamp = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    bssid = Column(String(50), nullable=True)
    check_in_time = Column(DateTime, nullable=True)
    is_late = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

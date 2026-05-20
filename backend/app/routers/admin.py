from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import bcrypt
import jwt
import os

from ..database import get_db
from ..models import AdminUser, User, AttendanceLog

router = APIRouter()

# Secret key for JWT. In production, use a strong env variable
JWT_SECRET = os.getenv("JWT_SECRET", "super_secret_jwt_key_for_admin_only")
JWT_ALGORITHM = "HS256"

class AdminLoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(hours=1))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

# Custom Dependency to extract JWT from Authorization header
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/admin/login")

def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
        
    admin = db.query(AdminUser).filter(AdminUser.username == username).first()
    if not admin:
        raise HTTPException(status_code=401, detail="Admin not found")
    return admin

@router.post("/admin/login", response_model=TokenResponse)
def login(request: AdminLoginRequest, db: Session = Depends(get_db)):
    admin = db.query(AdminUser).filter(AdminUser.username == request.username).first()
    if not admin or not bcrypt.checkpw(request.password.encode('utf-8'), admin.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Sai tài khoản hoặc mật khẩu")
        
    access_token = create_access_token(data={"sub": admin.username}, expires_delta=timedelta(hours=4))
    return {"access_token": access_token, "token_type": "bearer"}


class UserStatResponse(BaseModel):
    student_code: str
    full_name: str
    total_hours: float
    total_sessions: int

@router.get("/admin/users", response_model=List[UserStatResponse])
def get_users_stats(admin: AdminUser = Depends(get_current_admin), db: Session = Depends(get_db)):
    users = db.query(User).all()
    results = []
    for u in users:
        logs = db.query(AttendanceLog).filter(AttendanceLog.user_id == u.id).all()
        successful_logs = [log for log in logs if log.status in ("ON_TIME", "LATE")]
        
        total_hours = 0.0
        unique_days = set()
        
        for log in successful_logs:
            unique_days.add(log.timestamp.date())
            if log.check_in_time and getattr(log, 'check_out_time', None):
                delta = log.check_out_time - log.check_in_time
                total_hours += round(delta.total_seconds() / 3600.0, 2)
        
        results.append(UserStatResponse(
            student_code=u.student_code,
            full_name=u.full_name,
            total_hours=round(total_hours, 2),
            total_sessions=len(unique_days)
        ))
    return results

class LogResponse(BaseModel):
    student_code: str
    full_name: str
    date: str
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None
    working_hours: float
    is_late: bool
    status: str

@router.get("/admin/logs", response_model=List[LogResponse])
def get_all_logs(admin: AdminUser = Depends(get_current_admin), db: Session = Depends(get_db)):
    logs = db.query(AttendanceLog).filter(
        AttendanceLog.status.in_(["ON_TIME", "LATE"])
    ).order_by(AttendanceLog.timestamp.desc()).limit(100).all()
    
    results = []
    for log in logs:
        user = db.query(User).filter(User.id == log.user_id).first()
        if not user: continue
        
        t = log.check_in_time if log.check_in_time else log.timestamp
        date_str = t.strftime("%d/%m/%Y")
        
        hours = 0.0
        if log.check_in_time and getattr(log, 'check_out_time', None):
            delta = log.check_out_time - log.check_in_time
            hours = round(delta.total_seconds() / 3600.0, 2)
            
        results.append(LogResponse(
            student_code=user.student_code,
            full_name=user.full_name,
            date=date_str,
            check_in_time=log.check_in_time,
            check_out_time=getattr(log, 'check_out_time', None),
            working_hours=hours,
            is_late=log.is_late or False,
            status=log.status
        ))
    return results

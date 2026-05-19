from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ..database import get_db
from ..models import AttendanceLog, User

router = APIRouter()

class RecordResponse(BaseModel):
    date: str
    check_in_time: Optional[datetime] = None
    is_late: bool
    status: str

@router.get("/records", response_model=List[RecordResponse])
def get_attendance_records(student_code: str = Query(...), db: Session = Depends(get_db)):
    """
    Lấy lịch sử điểm danh của một sinh viên cụ thể.
    """
    user = db.query(User).filter(User.student_code == student_code).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy sinh viên.")

    logs = db.query(AttendanceLog).filter(
        AttendanceLog.user_id == user.id
    ).order_by(AttendanceLog.timestamp.desc()).all()

    result = []
    for log in logs:
        # Lấy ngày từ check_in_time nếu có, không thì từ timestamp
        t = log.check_in_time if log.check_in_time else log.timestamp
        date_str = t.strftime("%Y-%m-%d")
        result.append(RecordResponse(
            date=date_str,
            check_in_time=log.check_in_time,
            is_late=log.is_late or False,
            status=log.status
        ))

    return result

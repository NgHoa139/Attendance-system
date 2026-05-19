from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import bcrypt
from pydantic import BaseModel

from ..database import get_db
from ..models import User

router = APIRouter()


class LoginRequest(BaseModel):
    student_code: str
    password: str


class LoginResponse(BaseModel):
    student_code: str
    full_name: str
    device_uuid: str
    session_id: str


@router.post("/auth/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Xác thực sinh viên bằng mã sinh viên và mật khẩu.
    Trả về thông tin cần thiết để frontend lưu vào localStorage.
    """
    # 1. Tìm user theo mã sinh viên
    user = db.query(User).filter(User.student_code == request.student_code).first()

    # 2. Kiểm tra user tồn tại và mật khẩu hợp lệ
    if not user or not user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mã sinh viên hoặc mật khẩu không đúng."
        )

    password_match = bcrypt.checkpw(
        request.password.encode('utf-8'),
        user.hashed_password.encode('utf-8')
    )
    if not password_match:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mã sinh viên hoặc mật khẩu không đúng."
        )

    # 3. Lấy session mới nhất đang hoạt động (cho demo)
    # Trong thực tế, sinh viên sẽ chọn session hoặc có thể fetch sau khi đăng nhập
    from ..models import Session as ClassSession
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
    active_session = db.query(ClassSession).first()

    session_id = str(active_session.id) if active_session else "2441a18c-3965-4f32-bb9f-6821d3f9e9ba"

    # 4. Trả về thông tin đăng nhập
    return LoginResponse(
        student_code=user.student_code,
        full_name=user.full_name,
        device_uuid=user.device_uuid,
        session_id=session_id
    )

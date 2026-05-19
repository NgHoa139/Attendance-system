from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
import bcrypt
from pydantic import BaseModel

from ..database import get_db
from ..models import User, Session as ClassSession

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

@router.get("/auth/seed")
def seed_database(db: Session = Depends(get_db)):
    import bcrypt
    from datetime import datetime, timedelta
    
    # 1. Thêm/Cập nhật User
    hashed_pwd = bcrypt.hashpw("123456".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = db.query(User).filter(User.student_code == 'SE123456').first()
    if not user:
        user = User(
            id='f9e0eb9b-0000-4000-8000-000000000000',
            student_code='SE123456',
            device_uuid='WEB-BROWSER-UUID-12345',
            full_name='Nguyễn Văn Test',
            hashed_password=hashed_pwd
        )
        db.add(user)
    else:
        user.hashed_password = hashed_pwd
        
    # 2. Thêm Session
    session = db.query(ClassSession).filter(ClassSession.id == '2441a18c-3965-4f32-bb9f-6821d3f9e9ba').first()
    if not session:
        session = ClassSession(
            id='2441a18c-3965-4f32-bb9f-6821d3f9e9ba',
            name='Lớp Nhập môn Lập trình',
            start_time=datetime.now() - timedelta(hours=1),
            end_time=datetime.now() + timedelta(hours=1),
            base_lat=21.013,
            base_lon=105.526,
            base_bssid='127.0.0.1'
        )
        db.add(session)
        
    db.commit()
    return {"message": "Dữ liệu mẫu đã được thêm thành công vào Database!"}

class UpdateSessionRequest(BaseModel):
    lat: float
    lon: float

@router.post("/auth/update_session")
def update_session(request: UpdateSessionRequest, raw_request: Request, db: Session = Depends(get_db)):
    """
    Cập nhật tọa độ và IP của lớp học bằng vị trí hiện tại của người dùng.
    """
    session = db.query(ClassSession).filter(ClassSession.id == '2441a18c-3965-4f32-bb9f-6821d3f9e9ba').first()
    if not session:
        raise HTTPException(status_code=404, detail="Không tìm thấy session mẫu.")

    # Lấy IP thực
    forwarded_for = raw_request.headers.get("x-forwarded-for")
    if forwarded_for:
        client_ip = forwarded_for.split(",")[0].strip()
    else:
        client_ip = raw_request.client.host

    # Cập nhật
    session.base_lat = request.lat
    session.base_lon = request.lon
    session.base_bssid = client_ip
    db.commit()

    return {
        "message": "Đã cập nhật tọa độ và mạng WiFi chuẩn thành công!",
        "new_lat": request.lat,
        "new_lon": request.lon,
        "new_ip": client_ip
    }

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import logging

from ..database import get_db
from ..models import User, Session as ClassSession, AttendanceLog
from ..schemas import AttendanceRequest, AttendancePayload
from ..security import verify_signature, decrypt_payload, haversine

router = APIRouter()
logger = logging.getLogger("attendance")

@router.post("/attend")
def process_attendance(request: AttendanceRequest, raw_request: Request, db: Session = Depends(get_db)):
    # 1. Verify HMAC signature
    if not verify_signature(request.payload, request.signature):
        logger.warning(f"Invalid signature received")
        raise HTTPException(status_code=403, detail="Invalid signature")

    # 2. Decrypt Payload
    try:
        payload_dict = decrypt_payload(request.payload)
        payload = AttendancePayload(**payload_dict)
    except Exception as e:
        logger.error(f"Failed to decrypt/parse payload: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid encrypted payload")

    # 3. Check for Spoofing (Mock Location)
    if payload.is_mocked:
        log_attempt(db, payload, "SPOOFED")
        logger.warning(f"Spoofed location detected for user {payload.student_code}")
        raise HTTPException(status_code=403, detail="Mock location detected")

    # 4. Device Binding Verification
    user = db.query(User).filter(User.student_code == payload.student_code).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if user.device_uuid != payload.device_uuid:
        log_attempt(db, payload, "INVALID_DEVICE", user.id)
        logger.warning(f"Device mismatch for user {payload.student_code}. Expected {user.device_uuid}, got {payload.device_uuid}")
        raise HTTPException(status_code=403, detail="Unregistered device")

    # 5. Get Session Info
    session = db.query(ClassSession).filter(ClassSession.id == payload.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Check Time
    from datetime import datetime, timezone
    # Convert payload timestamp string or use datetime.now()
    now = datetime.now()
    
    is_late = False
    if now.hour >= 10 and now.minute >= 0:
        is_late = True

    # 6. Validate Location (Haversine <= 50m) OR Wifi BSSID
    is_valid_location = False
    if payload.lat and payload.lon:
        distance = haversine(payload.lat, payload.lon, session.base_lat, session.base_lon)
        if distance <= 50.0:
            is_valid_location = True

    is_valid_wifi = False
    
    # Lấy IP thực của client khi chạy qua proxy (Render/Nginx)
    forwarded_for = raw_request.headers.get("x-forwarded-for")
    if forwarded_for:
        client_ip = forwarded_for.split(",")[0].strip()
    else:
        client_ip = raw_request.client.host

    if payload.bssid and payload.bssid.upper() == session.base_bssid.upper():
        is_valid_wifi = True
    elif not payload.bssid and client_ip == session.base_bssid:
        # Nếu payload.bssid không có (từ Web App) thì check IP khớp với base_bssid (được lưu là IP)
        is_valid_wifi = True

    if not (is_valid_location or is_valid_wifi):
        log_attempt(db, payload, "FAILED", user.id, check_in_time=now, is_late=is_late)
        logger.info(f"Attendance failed for {payload.student_code}. Not in range and wrong WiFi.")
        raise HTTPException(status_code=400, detail="Not in required location or WiFi network")

    # 7. Record Attendance
    status_str = "LATE" if is_late else "ON_TIME"
    log_attempt(db, payload, status_str, user.id, check_in_time=now, is_late=is_late)
    logger.info(f"Attendance success for {payload.student_code} in session {session.id}. Late: {is_late}")
    return {"status": "success", "message": f"Điểm danh thành công ({'Muộn' if is_late else 'Đúng giờ'})"}

def log_attempt(db: Session, payload: AttendancePayload, status: str, user_id=None, check_in_time=None, is_late=False):
    new_log = AttendanceLog(
        user_id=user_id,
        session_id=payload.session_id,
        timestamp=payload.timestamp,
        status=status,
        lat=payload.lat,
        lon=payload.lon,
        bssid=payload.bssid,
        check_in_time=check_in_time,
        is_late=is_late
    )
    db.add(new_log)
    db.commit()

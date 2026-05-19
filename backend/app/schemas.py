from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class AttendanceRequest(BaseModel):
    payload: str
    signature: str

class AttendancePayload(BaseModel):
    student_code: str
    device_uuid: str
    session_id: uuid.UUID
    lat: Optional[float] = None
    lon: Optional[float] = None
    bssid: Optional[str] = None
    timestamp: datetime
    is_mocked: bool = False

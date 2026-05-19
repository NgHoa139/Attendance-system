from fastapi import FastAPI
from pydantic import BaseModel
import math
import os

app = FastAPI()

# ==========================================
# CẤU HÌNH HỆ THỐNG
# ==========================================
# Tọa độ tâm (Ví dụ: Khu vực Hòa Lạc)
TARGET_LAT = 21.0130  
TARGET_LON = 105.5270
MAX_RADIUS_METERS = 50  # Bán kính cho phép (mét)

# Danh sách địa chỉ MAC Wifi nội bộ hợp lệ
ALLOWED_BSSIDS = [
    "00:1A:2B:3C:4D:5E",
    "AA:BB:CC:DD:EE:FF"
]

# Cấu hình đường dẫn tuyệt đối cho file log
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE_PATH = os.path.join(BASE_DIR, "attendance_logs.txt")

# ==========================================
# MODEL DỮ LIỆU ĐẦU VÀO
# ==========================================
class CheckInRequest(BaseModel):
    user_id: str
    lat: float
    lon: float
    bssid: str
    is_mock_location: bool = False

# ==========================================
# HÀM TÍNH KHOẢNG CÁCH (HAVERSINE)
# ==========================================
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Bán kính Trái Đất (mét)
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi_1) * math.cos(phi_2) * \
        math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

# ==========================================
# API ENDPOINT: XỬ LÝ ĐIỂM DANH
# ==========================================
@app.post("/api/checkin")
def process_checkin(data: CheckInRequest):
    # 1. Chặn Fake GPS (Mock Location)
    if data.is_mock_location:
        return {"status": "fail", "message": "Phát hiện vị trí giả mạo (Mock Location)."}

    # 2. Kiểm tra BSSID (Chống giả mạo tên Wifi)
    if data.bssid not in ALLOWED_BSSIDS:
        return {"status": "fail", "message": "Sai mạng Wifi. BSSID không hợp lệ."}

    # 3. Tính toán khoảng cách tọa độ (GPS Geofencing)
    distance = haversine(TARGET_LAT, TARGET_LON, data.lat, data.lon)
    
    if distance > MAX_RADIUS_METERS:
        return {
            "status": "fail", 
            "message": f"Ngoài vùng điểm danh. Khoảng cách hiện tại: {distance:.2f}m."
        }

    # 4. Ghi nhận thành công vào Log File
    log_entry = f"User: {data.user_id} | Distance: {distance:.2f}m | BSSID: {data.bssid} | SUCCESS\n"
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
        f.write(log_entry)

    return {
        "status": "success", 
        "message": f"Điểm danh thành công. Khoảng cách: {distance:.2f}m."
    }
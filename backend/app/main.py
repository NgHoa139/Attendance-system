from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from .database import engine, Base
from .routers import attendance, auth, records, admin


# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Attendance System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup Absolute Path Logging
# Require ABSOLUTE PATH as per user request
LOG_FILE_PATH = "C:/Users/Admin/Desktop/Thư mục mới/logs/attendance.log"

# Ensure log directory exists
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

logger = logging.getLogger("attendance")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(LOG_FILE_PATH)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

app.include_router(attendance.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(records.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Attendance API is running"}

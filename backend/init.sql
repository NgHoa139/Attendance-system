CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_code VARCHAR(20) UNIQUE NOT NULL,
    device_uuid VARCHAR(255) NOT NULL, -- Ràng buộc Device Binding
    full_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    base_lat DOUBLE PRECISION NOT NULL, -- Vĩ độ cơ sở (VD: 21.0130)
    base_lon DOUBLE PRECISION NOT NULL, -- Kinh độ cơ sở (VD: 105.5270)
    base_bssid VARCHAR(50) NOT NULL,    -- Địa chỉ MAC Wifi cơ sở
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE attendance_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    session_id UUID REFERENCES sessions(id),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(20) NOT NULL, -- 'SUCCESS', 'FAILED', 'SPOOFED', 'INVALID_DEVICE'
    lat DOUBLE PRECISION,
    lon DOUBLE PRECISION,
    bssid VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

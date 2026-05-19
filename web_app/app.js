// ==========================================
// Kiểm tra đăng nhập: đọc thông tin từ localStorage
// Nếu chưa đăng nhập -> chuyển về trang login
// ==========================================
const storedUserInfo = localStorage.getItem('userInfo');
if (!storedUserInfo) {
    window.location.href = 'login.html';
}

const USER_INFO = storedUserInfo ? JSON.parse(storedUserInfo) : {};

// Cấu hình URL Backend
const API_BASE_URL = "https://attendance-system-87zs.onrender.com/api/v1";

// Cập nhật giao diện
document.getElementById('studentCodeDisplay').innerText = USER_INFO.studentCode || 'N/A';


const btnAttend = document.getElementById('btnAttend');
const statusCard = document.getElementById('statusCard');
const statusIcon = document.getElementById('statusIcon');
const statusMessage = document.getElementById('statusMessage');
const subStatusMessage = document.getElementById('subStatusMessage');

function updateStatus(state, message, subMessage, icon = '📍') {
    statusMessage.innerText = message;
    subStatusMessage.innerText = subMessage;
    statusIcon.innerText = icon;
    
    // Reset classes
    statusCard.className = 'status-card';
    document.querySelector('.icon-pulse').className = 'icon-pulse';
    
    if (state === 'loading') {
        document.querySelector('.icon-pulse').classList.add('loading');
        statusIcon.innerText = '⏳';
    } else if (state === 'success') {
        statusCard.classList.add('status-success');
        statusIcon.innerText = '✅';
    } else if (state === 'error') {
        statusCard.classList.add('status-error');
        statusIcon.innerText = '❌';
    }
}

function getGPSLocation() {
    return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
            reject(new Error("Trình duyệt không hỗ trợ GPS."));
            return;
        }

        navigator.geolocation.getCurrentPosition(
            (position) => {
                resolve({
                    lat: position.coords.latitude,
                    lon: position.coords.longitude
                });
            },
            (error) => {
                let msg = "Lỗi lấy GPS.";
                if (error.code === 1) msg = "Bạn đã từ chối quyền truy cập vị trí.";
                reject(new Error(msg));
            },
            { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
        );
    });
}

btnAttend.addEventListener('click', async () => {
    // 1. Giao diện Loading
    btnAttend.disabled = true;
    updateStatus('loading', 'Đang xác định vị trí...', 'Vui lòng cho phép quyền truy cập GPS.');

    try {
        // 2. Lấy GPS
        let location = { lat: null, lon: null };
        try {
            location = await getGPSLocation();
            updateStatus('loading', 'Đang mã hóa dữ liệu...', `Tọa độ: \${location.lat.toFixed(4)}, \${location.lon.toFixed(4)}`);
        } catch (e) {
            // Vẫn cho qua nếu không có GPS, Backend sẽ kiểm tra IP
            console.warn(e.message);
            updateStatus('loading', 'Không có GPS', 'Sẽ sử dụng điểm danh bằng mạng Wifi (IP).');
        }

        // 3. Đóng gói Payload
        const payloadObj = {
            student_code: USER_INFO.studentCode,
            device_uuid: USER_INFO.deviceUuid,
            session_id: USER_INFO.sessionId,
            lat: location.lat,
            lon: location.lon,
            bssid: null, // Trình duyệt KHÔNG THỂ lấy BSSID
            timestamp: new Date().toISOString(),
            is_mocked: false // Trình duyệt không bắt được Fake GPS dễ dàng
        };

        // 4. Mã hóa AES và ký HMAC
        const encryptedPayload = CryptoService.encryptPayload(payloadObj);
        const signature = CryptoService.generateSignature(encryptedPayload);

        updateStatus('loading', 'Đang gửi yêu cầu...', 'Kết nối tới máy chủ bảo mật.');

        // 5. Gửi lên Backend
        const response = await fetch(API_BASE_URL + '/attend', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                payload: encryptedPayload,
                signature: signature
            })
        });

        const data = await response.json();

        // 6. Cập nhật kết quả
        if (response.ok) {
            updateStatus('success', 'Điểm danh thành công!', 'Bạn đã hoàn tất điểm danh cho ca này.');
        } else {
            updateStatus('error', 'Điểm danh thất bại', data.detail || 'Không rõ lỗi.');
        }

    } catch (error) {
        updateStatus('error', 'Lỗi hệ thống', error.message);
    } finally {
        btnAttend.disabled = false;
        btnAttend.querySelector('span').innerText = 'THỰC HIỆN ĐIỂM DANH';
    }
});

// Hàm Dev: Cập nhật Tọa độ và IP hiện tại thành mặc định của trường
window.updateSessionToCurrent = function() {
    if (!navigator.geolocation) {
        alert("Trình duyệt không hỗ trợ GPS.");
        return;
    }
    
    const btn = event.target;
    btn.innerText = "Đang lấy tọa độ...";
    
    navigator.geolocation.getCurrentPosition(
        async (position) => {
            try {
                const res = await fetch(`${API_BASE_URL}/auth/update_session`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        lat: position.coords.latitude,
                        lon: position.coords.longitude
                    })
                });
                
                const data = await res.json();
                if (res.ok) {
                    alert(`Thành công! Tọa độ (${data.new_lat}, ${data.new_lon}) và IP (${data.new_ip}) của bạn đã được lưu làm mặc định của lớp học.`);
                    btn.innerText = "[DEV] Thiết lập tọa độ & WiFi này làm Mặc Định";
                } else {
                    alert("Lỗi: " + JSON.stringify(data));
                    btn.innerText = "Lỗi, thử lại!";
                }
            } catch (err) {
                alert("Không kết nối được server.");
                btn.innerText = "[DEV] Thiết lập tọa độ & WiFi này làm Mặc Định";
            }
        },
        (error) => {
            alert("Lỗi lấy GPS: " + error.message);
            btn.innerText = "[DEV] Thiết lập tọa độ & WiFi này làm Mặc Định";
        },
        { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
    );
};

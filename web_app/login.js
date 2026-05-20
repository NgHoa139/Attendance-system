const API_BASE_URL = "https://attendance-system-87zs.onrender.com/api/v1";

const loginForm = document.getElementById('loginForm');
const btnLogin = document.getElementById('btnLogin');
const statusMsg = document.getElementById('statusMsg');

function showMessage(type, message) {
    statusMsg.className = `status-msg ${type}`;
    statusMsg.textContent = message;
}

function clearMessage() {
    statusMsg.className = 'status-msg';
    statusMsg.textContent = '';
}

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    clearMessage();

    const studentCode = document.getElementById('studentCode').value.trim();
    const password = document.getElementById('password').value;

    if (!studentCode || !password) {
        showMessage('error', 'Vui lòng nhập đầy đủ Mã Sinh Viên và Mật Khẩu.');
        return;
    }

    // Set loading state
    btnLogin.disabled = true;
    btnLogin.textContent = 'Đang đăng nhập...';
    showMessage('loading', 'Đang xác thực thông tin, vui lòng chờ...');

    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ student_code: studentCode, password: password })
        });

        const data = await response.json();

        if (response.ok) {
            // Lưu thông tin đăng nhập vào localStorage và chuyển hướng
            showMessage('loading', '✅ Đăng nhập thành công! Đang chuyển hướng...');

            if (data.role === 'admin') {
                localStorage.setItem('adminToken', data.admin_token);
                window.location.href = 'admin.html';
            } else {
                localStorage.setItem('userInfo', JSON.stringify({
                    studentCode: data.student_code,
                    fullName: data.full_name,
                    deviceUuid: data.device_uuid,
                    sessionId: data.session_id
                }));
                window.location.href = 'index.html';
            }
        } else {
            showMessage('error', data.detail || 'Đăng nhập thất bại. Vui lòng thử lại.');
            btnLogin.disabled = false;
            btnLogin.textContent = 'Đăng Nhập';
        }
    } catch (error) {
        showMessage('error', 'Không kết nối được với máy chủ. Vui lòng thử lại.');
        btnLogin.disabled = false;
        btnLogin.textContent = 'Đăng Nhập';
    }
});

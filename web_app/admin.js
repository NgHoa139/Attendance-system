const API_BASE_URL = "https://attendance-system-87zs.onrender.com/api/v1";
const token = localStorage.getItem('adminToken');
if (!token) {
    window.location.href = 'login.html';
}

function logoutAdmin() {
    localStorage.removeItem('adminToken');
    window.location.href = 'login.html';
}

function switchTab(tabId) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    
    event.target.classList.add('active');
    document.getElementById(tabId).classList.add('active');
    
    if (tabId === 'logs') fetchLogs();
    if (tabId === 'users') fetchUsers();
}

async function fetchLogs() {
    try {
        const res = await fetch(`${API_BASE_URL}/admin/logs`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (res.status === 401) { logoutAdmin(); return; }
        
        const data = await res.json();
        const tbody = document.getElementById('logsTableBody');
        
        if (data.length === 0) {
            tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding: 40px; color: var(--text-sub);">Chưa có dữ liệu</td></tr>`;
            return;
        }
        
        let html = '';
        data.forEach((log, index) => {
            let inTimeStr = '-';
            if (log.check_in_time) {
                const d = new Date(log.check_in_time + 'Z');
                inTimeStr = d.toLocaleTimeString('vi-VN');
            }
            
            let outTimeStr = '-';
            if (log.check_out_time) {
                const d = new Date(log.check_out_time + 'Z');
                outTimeStr = d.toLocaleTimeString('vi-VN');
            }
            
            let badgeClass = log.status === 'ON_TIME' ? 'success' : (log.status === 'LATE' ? 'warning' : 'error');
            let statusText = log.status === 'ON_TIME' ? 'Đúng giờ' : (log.status === 'LATE' ? 'Đi muộn' : 'Thất bại');
            
            html += `
                <tr onclick="toggleDetails('detail-${index}')" style="cursor: pointer; transition: background 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.05)'" onmouseout="this.style.background='transparent'">
                    <td><strong>${log.full_name}</strong></td>
                    <td>${log.date}</td>
                    <td><span class="badge ${badgeClass}">${statusText}</span></td>
                </tr>
                <tr id="detail-${index}" style="display: none; background: rgba(0,0,0,0.2);">
                    <td colspan="3" style="padding: 20px 24px; font-size: 15px; color: var(--text-sub); line-height: 1.8;">
                        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; border-left: 4px solid var(--${badgeClass}); padding-left: 20px; margin: 8px 0;">
                            <span><strong>Mã SV:</strong> <br><span style="color:#fff; font-size: 16px;">${log.student_code}</span></span>
                            <span><strong>Check-in:</strong> <br><span style="color:#fff; font-size: 16px;">${inTimeStr}</span></span>
                            <span><strong>Check-out:</strong> <br><span style="color:#fff; font-size: 16px;">${outTimeStr}</span></span>
                            <span><strong>Số giờ làm:</strong> <br><span style="color:#a855f7; font-weight:700; font-size: 18px;">${log.working_hours > 0 ? log.working_hours + 'h' : '-'}</span></span>
                        </div>
                    </td>
                </tr>
            `;
        });
        tbody.innerHTML = html;
    } catch (err) {
        console.error(err);
    }
}

window.toggleDetails = function(id) {
    const el = document.getElementById(id);
    if (el.style.display === 'none') {
        el.style.display = 'table-row';
    } else {
        el.style.display = 'none';
    }
}

window.createUser = async function(event) {
    event.preventDefault();
    const studentCode = document.getElementById('newStudentCode').value;
    const fullName = document.getElementById('newFullName').value;
    const password = document.getElementById('newPassword').value;
    const msgEl = document.getElementById('createMessage');
    const btn = document.getElementById('btnCreateUser');
    
    try {
        btn.disabled = true;
        btn.innerText = "Đang tạo...";
        msgEl.style.display = 'none';
        
        const res = await fetch(`${API_BASE_URL}/admin/users`, {
            method: 'POST',
            headers: { 
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                student_code: studentCode,
                full_name: fullName,
                password: password
            })
        });
        
        const data = await res.json();
        
        msgEl.style.display = 'block';
        if (res.ok) {
            msgEl.style.color = '#22c55e';
            msgEl.innerText = "✅ Tạo tài khoản sinh viên thành công!";
            document.getElementById('createUserForm').reset();
            // Refresh users list in background
            fetchUsers();
        } else {
            msgEl.style.color = '#ef4444';
            msgEl.innerText = "❌ Lỗi: " + (data.detail || "Không thể tạo tài khoản");
        }
    } catch (err) {
        msgEl.style.display = 'block';
        msgEl.style.color = '#ef4444';
        msgEl.innerText = "❌ Lỗi kết nối mạng!";
    } finally {
        btn.disabled = false;
        btn.innerText = "Tạo Tài Khoản";
    }
}

async function fetchUsers() {
    try {
        const res = await fetch(`${API_BASE_URL}/admin/users`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (res.status === 401) { logoutAdmin(); return; }
        
        const data = await res.json();
        const tbody = document.getElementById('usersTableBody');
        
        if (data.length === 0) {
            tbody.innerHTML = `<tr><td colspan="4" style="text-align:center; padding: 40px; color: var(--text-sub);">Chưa có dữ liệu</td></tr>`;
            return;
        }
        
        let html = '';
        data.forEach(user => {
            html += `
                <tr>
                    <td><strong>${user.student_code}</strong></td>
                    <td>${user.full_name}</td>
                    <td>${user.total_sessions} buổi</td>
                    <td style="color:#22c55e; font-weight:600;">${user.total_hours}h</td>
                </tr>
            `;
        });
        tbody.innerHTML = html;
    } catch (err) {
        console.error(err);
    }
}

// Initial fetch
fetchLogs();

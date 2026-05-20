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
                    <td colspan="3" style="padding: 16px 24px; font-size: 14.5px; color: var(--text-sub); line-height: 1.8;">
                        <div style="display: flex; justify-content: space-between; border-left: 4px solid var(--${badgeClass}); padding-left: 16px; margin: 4px 0;">
                            <span style="letter-spacing: 0.3px;"><strong>Mã SV:</strong> <span style="color:#fff;">${log.student_code}</span></span>
                            <span style="letter-spacing: 0.3px;"><strong>Check-in:</strong> <span style="color:#fff;">${inTimeStr}</span></span>
                            <span style="letter-spacing: 0.3px;"><strong>Check-out:</strong> <span style="color:#fff;">${outTimeStr}</span></span>
                            <span style="letter-spacing: 0.3px;"><strong>Số giờ làm:</strong> <span style="color:#a855f7; font-weight:600; font-size: 15px;">${log.working_hours > 0 ? log.working_hours + 'h' : '-'}</span></span>
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

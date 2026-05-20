const token = localStorage.getItem('adminToken');
if (!token) {
    window.location.href = 'admin_login.html';
}

function logoutAdmin() {
    localStorage.removeItem('adminToken');
    window.location.href = 'admin_login.html';
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
        data.forEach(log => {
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
                <tr>
                    <td><strong>${log.student_code}</strong></td>
                    <td>${log.full_name}</td>
                    <td>${log.date}</td>
                    <td>${inTimeStr}</td>
                    <td>${outTimeStr}</td>
                    <td style="color:#a855f7; font-weight:600;">${log.working_hours > 0 ? log.working_hours + 'h' : '-'}</td>
                    <td><span class="badge ${badgeClass}">${statusText}</span></td>
                </tr>
            `;
        });
        tbody.innerHTML = html;
    } catch (err) {
        console.error(err);
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

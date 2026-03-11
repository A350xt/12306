// 登录相关功能
let qrCheckInterval = null;
let currentUUID = null;

function showTab(tabName) {
    // 隐藏所有tab
    document.querySelectorAll('.login-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // 显示选中的tab
    if (tabName === 'qr') {
        document.getElementById('qr-login').classList.add('active');
        document.querySelectorAll('.tab-btn')[0].classList.add('active');
    } else {
        document.getElementById('account-login').classList.add('active');
        document.querySelectorAll('.tab-btn')[1].classList.add('active');
    }
}

async function getQRCode() {
    const qrCodeDiv = document.getElementById('qr-code');
    const statusDiv = document.getElementById('qr-status');

    try {
        const response = await fetch('/login/12306?type=get_picture');
        const data = await response.json();

        if (data.image) {
            currentUUID = data.uuid;
            qrCodeDiv.innerHTML = `<img src="data:image/png;base64,${data.image}" alt="二维码">`;
            statusDiv.textContent = '请使用12306 APP扫描二维码';
            statusDiv.className = 'status-text';

            // 开始检查登录状态
            startCheckLogin();
        } else {
            statusDiv.textContent = '获取二维码失败';
            statusDiv.className = 'status-text error';
        }
    } catch (error) {
        statusDiv.textContent = '网络错误：' + error.message;
        statusDiv.className = 'status-text error';
    }
}

function startCheckLogin() {
    if (qrCheckInterval) {
        clearInterval(qrCheckInterval);
    }

    qrCheckInterval = setInterval(async () => {
        try {
            const response = await fetch('/login/12306?type=check_login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ uuid: currentUUID })
            });

            const data = await response.json();
            const statusDiv = document.getElementById('qr-status');

            if (data.code === '0') {
                statusDiv.textContent = '正在等待用户扫描二维码...';
                statusDiv.className = 'status-text';
            } else if (data.code === '1') {
                statusDiv.textContent = '二维码已扫描，正在等待用户确认...';
                statusDiv.className = 'status-text';
            } else if (data.code === '2') {
                statusDiv.textContent = '登录成功！';
                statusDiv.className = 'status-text success';
                clearInterval(qrCheckInterval);
                setTimeout(() => {
                    window.location.href = '/';
                }, 2000);
            } else if (data.code === '3') {
                statusDiv.textContent = '二维码已失效，请重新获取';
                statusDiv.className = 'status-text error';
                clearInterval(qrCheckInterval);
            }
        } catch (error) {
            console.error('检查登录状态失败:', error);
        }
    }, 2000);
}

// 账号登录
document.getElementById('account-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const statusDiv = document.getElementById('account-status');

    try {
        const response = await fetch('/login/account', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (data.code === '0') {
            statusDiv.textContent = '登录成功！';
            statusDiv.className = 'status-text success';
            setTimeout(() => {
                window.location.href = '/';
            }, 2000);
        } else {
            statusDiv.textContent = data.msg || '登录失败';
            statusDiv.className = 'status-text error';
        }
    } catch (error) {
        statusDiv.textContent = '网络错误：' + error.message;
        statusDiv.className = 'status-text error';
    }
});

// 页面卸载时清除定时器
window.addEventListener('beforeunload', () => {
    if (qrCheckInterval) {
        clearInterval(qrCheckInterval);
    }
});

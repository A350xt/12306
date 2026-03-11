// 车票查询功能
document.getElementById('search-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const fromStation = document.getElementById('from-station').value;
    const toStation = document.getElementById('to-station').value;
    const date = document.getElementById('date').value;
    const resultsDiv = document.getElementById('results');

    resultsDiv.innerHTML = '<p style="text-align: center;">正在查询...</p>';

    try {
        // 格式化日期为YYYYMMDD
        const formattedDate = date.replace(/-/g, '');

        const response = await fetch(`/search?type=ticket&begin=${fromStation}&end=${toStation}&date=${formattedDate}`);
        const data = await response.json();

        if (data.code === '0' && data.data && data.data.length > 0) {
            displayResults(data.data);
        } else {
            resultsDiv.innerHTML = '<p style="text-align: center;">未找到相关车票信息</p>';
        }
    } catch (error) {
        resultsDiv.innerHTML = `<p style="text-align: center; color: red;">查询失败：${error.message}</p>`;
    }
});

function displayResults(tickets) {
    const resultsDiv = document.getElementById('results');

    let html = '<h3>查询结果</h3>';

    tickets.forEach(ticket => {
        html += `
            <div class="ticket-card">
                <div class="ticket-header">
                    <div class="train-info">${ticket.station_train_code}</div>
                    <div class="time-info">
                        <div>
                            <div style="font-size: 12px; color: #666;">出发</div>
                            <div style="font-size: 20px; font-weight: bold;">${ticket.start_time}</div>
                        </div>
                        <div style="color: #667eea;">→</div>
                        <div>
                            <div style="font-size: 12px; color: #666;">到达</div>
                            <div style="font-size: 20px; font-weight: bold;">${ticket.arrive_time}</div>
                        </div>
                        <div style="color: #999;">历时: ${ticket.lishi}</div>
                    </div>
                </div>
                ${ticket.controlled_train_message ? `<div style="color: #e74c3c; margin-bottom: 10px;">${ticket.controlled_train_message}</div>` : ''}
                <div class="seat-list">
                    ${ticket.seat_info.map(seat => `
                        <div class="seat-item">
                            <div class="seat-type">${seat.seat_type}</div>
                            <div class="seat-price">¥${seat.price}</div>
                            <div style="color: ${seat.num > 0 ? '#27ae60' : '#e74c3c'};">
                                ${seat.num > 0 ? `余${seat.num}` : '无票'}
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    });

    resultsDiv.innerHTML = html;
}

// 设置默认日期为今天
document.addEventListener('DOMContentLoaded', () => {
    const dateInput = document.getElementById('date');
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.value = today;
        dateInput.min = today;
    }
});

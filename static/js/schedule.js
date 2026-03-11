// 定时抢票任务管理
document.getElementById('add-job-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const jobId = formData.get('job_id');
    const begin = formData.get('begin');
    const end = formData.get('end');
    const date = formData.get('date').replace(/-/g, '');
    const trainNo = formData.get('train_no');
    const interval = formData.get('interval');

    try {
        const response = await fetch(
            `/scheduler?operation=add&job_id=${jobId}&begin=${begin}&end=${end}&date=${date}&train_no=${trainNo}&interval=${interval}`
        );
        const data = await response.json();

        if (data.code === '0') {
            alert('任务添加成功！');
            e.target.reset();
            loadJobs();
        } else {
            alert('添加失败：' + data.msg);
        }
    } catch (error) {
        alert('网络错误：' + error.message);
    }
});

async function loadJobs() {
    const jobsDiv = document.getElementById('jobs-list');
    jobsDiv.innerHTML = '<p style="text-align: center;">加载中...</p>';

    try {
        const response = await fetch('/scheduler?operation=list');
        const data = await response.json();

        if (data.code === '0' && data.jobs && data.jobs.length > 0) {
            displayJobs(data.jobs);
        } else {
            jobsDiv.innerHTML = '<p style="text-align: center;">暂无任务</p>';
        }
    } catch (error) {
        jobsDiv.innerHTML = `<p style="text-align: center; color: red;">加载失败：${error.message}</p>`;
    }
}

function displayJobs(jobs) {
    const jobsDiv = document.getElementById('jobs-list');

    let html = '';
    jobs.forEach(job => {
        html += `
            <div class="job-card">
                <div class="job-header">
                    <div class="job-id">任务ID: ${job.id}</div>
                    <div class="job-actions">
                        <button onclick="pauseJob('${job.id}')" class="btn btn-small">暂停</button>
                        <button onclick="resumeJob('${job.id}')" class="btn btn-small">恢复</button>
                        <button onclick="removeJob('${job.id}')" class="btn btn-small" style="background: #e74c3c;">删除</button>
                    </div>
                </div>
                <div class="job-info">
                    <div>任务名称: ${job.name}</div>
                    <div>下次运行: ${job.next_run_time || '已暂停'}</div>
                    <div>触发器: ${job.trigger}</div>
                </div>
            </div>
        `;
    });

    jobsDiv.innerHTML = html;
}

async function pauseJob(jobId) {
    try {
        const response = await fetch(`/scheduler?operation=pause&job_id=${jobId}`);
        const data = await response.json();

        if (data.code === '0') {
            alert('任务已暂停');
            loadJobs();
        } else {
            alert('暂停失败：' + data.msg);
        }
    } catch (error) {
        alert('网络错误：' + error.message);
    }
}

async function resumeJob(jobId) {
    try {
        const response = await fetch(`/scheduler?operation=resume&job_id=${jobId}`);
        const data = await response.json();

        if (data.code === '0') {
            alert('任务已恢复');
            loadJobs();
        } else {
            alert('恢复失败：' + data.msg);
        }
    } catch (error) {
        alert('网络错误：' + error.message);
    }
}

async function removeJob(jobId) {
    if (!confirm('确定要删除这个任务吗？')) {
        return;
    }

    try {
        const response = await fetch(`/scheduler?operation=remove&job_id=${jobId}`);
        const data = await response.json();

        if (data.code === '0') {
            alert('任务已删除');
            loadJobs();
        } else {
            alert('删除失败：' + data.msg);
        }
    } catch (error) {
        alert('网络错误：' + error.message);
    }
}

// 页面加载时自动加载任务列表
document.addEventListener('DOMContentLoaded', () => {
    loadJobs();

    // 设置默认日期为今天
    const dateInput = document.getElementById('date');
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.value = today;
        dateInput.min = today;
    }
});

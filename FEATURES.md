# 新功能使用指南

本文档详细介绍了12306-Python项目新增的功能及其使用方法。

## 1. 账号密码登录

### 功能说明
除了原有的扫码登录外，新增了账号密码登录接口（基础框架）。

### API接口
```
POST /login/account
Content-Type: application/json

{
    "username": "你的12306用户名",
    "password": "你的密码"
}
```

### 返回示例
```json
{
    "code": "0",
    "msg": "登录成功",
    "cookie": "..."
}
```

### 注意事项
- 由于12306官方主要推广扫码登录，账号密码登录可能需要额外的验证码处理
- 目前提供基础框架，可根据实际需求扩展

## 2. 定时抢票功能

### 功能说明
支持创建定时任务，自动检查车票余票情况，发现余票时可触发通知。

### 添加抢票任务
```
GET /scheduler?operation=add&job_id=task001&begin=BJP&end=SHH&date=20260320&train_no=G1&interval=60
```

参数说明：
- `job_id`: 任务唯一标识
- `begin`: 起始站代码（如BJP=北京）
- `end`: 终点站代码（如SHH=上海）
- `date`: 出发日期（YYYYMMDD格式）
- `train_no`: 车次号
- `interval`: 检查间隔（秒），最小10秒

### 管理任务
```bash
# 列出所有任务
GET /scheduler?operation=list

# 暂停任务
GET /scheduler?operation=pause&job_id=task001

# 恢复任务
GET /scheduler?operation=resume&job_id=task001

# 删除任务
GET /scheduler?operation=remove&job_id=task001

# 查看任务详情
GET /scheduler?operation=info&job_id=task001
```

### 使用示例
```python
import requests

# 添加一个每分钟检查一次的抢票任务
response = requests.get(
    'http://localhost:5000/scheduler',
    params={
        'operation': 'add',
        'job_id': 'beijing_to_shanghai',
        'begin': 'BJP',
        'end': 'SHH',
        'date': '20260320',
        'train_no': 'G1',
        'interval': 60
    }
)
print(response.json())
```

## 3. 第三方推送通知

### 功能说明
支持多种通知方式：邮件、钉钉、企业微信等。

### 邮件通知
```python
from plugins.notification import NotificationManager

ticket_info = {
    'train_no': 'G1',
    'seat_type': '二等座',
    'num': 5,
    'price': 553.0
}

result = NotificationManager.send_ticket_notification(
    notification_type='email',
    ticket_info=ticket_info,
    from_email='your_email@gmail.com',
    password='your_password',
    to_email='recipient@example.com'
)
```

### 钉钉通知
```python
result = NotificationManager.send_ticket_notification(
    notification_type='dingtalk',
    ticket_info=ticket_info,
    webhook_url='https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN'
)
```

### 企业微信通知
```python
result = NotificationManager.send_ticket_notification(
    notification_type='wechat',
    ticket_info=ticket_info,
    webhook_url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY'
)
```

### 集成到抢票任务
修改 `plugins/ticket_booking.py` 中的 `scheduled_ticket_check_job` 函数，传入 `notification_config` 参数：

```python
notification_config = {
    'type': 'dingtalk',
    'webhook_url': 'https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN'
}

scheduled_ticket_check_job(
    job_id='test',
    begin='BJP',
    end='SHH',
    date='20260320',
    train_no='G1',
    notification_config=notification_config
)
```

## 4. 列车时刻表

### 功能说明
查询列车时刻表信息，包括各站点到达时间、停靠时间等。

### 查询时刻表
```
GET /train_schedule?operation=query&train_no=G1&date=2026-03-20
```

### 返回示例
```json
{
    "code": "0",
    "msg": "查询成功",
    "schedule": [
        {
            "station_name": "北京南",
            "arrive_time": "08:00",
            "start_time": "08:00",
            "stop_time": "0分钟",
            "running_time": "00:00",
            "day_diff": "0",
            "is_start": true,
            "is_end": false
        },
        {
            "station_name": "上海虹桥",
            "arrive_time": "12:30",
            "start_time": "12:30",
            "stop_time": "0分钟",
            "running_time": "04:30",
            "day_diff": "0",
            "is_start": false,
            "is_end": true
        }
    ]
}
```

### 检查延误
```
GET /train_schedule?operation=check_delay&train_no=G1&station_name=北京南&date=2026-03-20
```

### 发车提醒
```
GET /train_schedule?operation=reminder&train_no=G1&departure_time=08:00&station_name=北京南
```

返回示例：
```json
{
    "code": "0",
    "msg": "列车即将发车！还有25分钟",
    "status": "urgent",
    "minutes_left": 25
}
```

## 5. Web UI界面

### 访问地址
- 首页：`http://localhost:5000/`
- 登录页面：`http://localhost:5000/ui/login`
- 车票查询：`http://localhost:5000/ui/search`
- 定时抢票：`http://localhost:5000/ui/schedule`

### 功能特点
- 响应式设计，支持移动端访问
- 直观的操作界面
- 实时显示查询结果
- 可视化的任务管理

### 使用说明

#### 登录
1. 访问 `/ui/login`
2. 选择扫码登录或账号登录
3. 扫码登录：点击"获取二维码"，使用12306 APP扫描
4. 账号登录：输入用户名和密码（开发中）

#### 车票查询
1. 访问 `/ui/search`
2. 输入出发站、到达站、日期
3. 点击"查询"按钮
4. 查看车票列表，包含座位类型、余票数、价格等信息

#### 定时抢票
1. 访问 `/ui/schedule`
2. 填写任务信息：
   - 任务ID（唯一标识）
   - 起始站代码、终点站代码
   - 出发日期、车次号
   - 检查间隔（秒）
3. 点击"添加任务"
4. 在任务列表中可以暂停、恢复、删除任务
5. 点击"刷新"查看最新任务状态

## 6. 代码结构

新增文件：
```
plugins/
├── ticket_booking.py       # 抢票功能
├── scheduler_manager.py    # 定时任务管理
├── notification.py         # 推送通知
└── train_schedule.py       # 列车时刻表

program/
├── scheduler.py           # 抢票路由处理
└── train_schedule.py      # 时刻表路由处理

templates/
├── index.html            # 首页
├── login.html            # 登录页
├── search.html           # 查询页
└── schedule.html         # 抢票管理页

static/
├── css/
│   └── style.css        # 样式表
└── js/
    ├── login.js         # 登录逻辑
    ├── search.js        # 查询逻辑
    └── schedule.js      # 任务管理逻辑
```

## 7. 常见问题

### Q1: 定时任务不执行怎么办？
A: 检查以下几点：
1. APScheduler是否正常启动（查看控制台日志）
2. 任务参数是否正确
3. 检查interval是否>=10秒
4. 查看任务状态：`/scheduler?operation=info&job_id=YOUR_ID`

### Q2: 如何配置邮件通知？
A:
1. 使用Gmail需要开启"允许不够安全的应用"或使用应用专用密码
2. 其他邮箱请查阅对应的SMTP设置
3. 修改 `plugins/notification.py` 中的smtp_host和smtp_port

### Q3: 车站代码在哪里查？
A:
1. 访问 `/update_station` 更新车站数据库
2. 查看 `resource/station_dict.txt` 文件
3. 或使用 `/search?type=Station&station=北京` 查询

### Q4: 如何停止所有定时任务？
A:
```python
from whole.Flask import scheduler
scheduler.shutdown()
```

## 8. 开发建议

### 扩展账号密码登录
需要处理：
1. 验证码识别
2. 滑块验证
3. Session管理
4. Cookie持久化

### 完善自动购票
需要实现：
1. 提交订单接口
2. 确认乘客信息
3. 选择座位
4. 支付接口（需用户授权）

### 增强延误检测
建议对接：
1. 12306实时数据
2. 第三方数据源（智行、携程等）
3. 自建数据采集系统

## 9. 贡献指南

欢迎提交Issue和Pull Request！

项目地址：https://github.com/2375137/12306

# 12306-Python
一个使用Python编写的12306高铁爬虫项目，并通过Flask框架提供Web服务
## 当前实现的功能:
### 登录
- [x] 扫码登录
- [x] 账号密码登录
### 个人行程
- [x] 本人车票查询(需扫码验证)
- [x] 获取全部车票
### 车站
- [x] 车站大屏
- [x] 获取并更新站点
### 车票(查票、抢票)
- [x] 查询火车票、高铁票
- [x] 定时抢火车票、高铁票

## 计划实现功能
### UI
- [x] 添加UI页面
### 行程提醒
- [x] 接入第三方推送,实现检票发车提醒
- [x] 添加列车时刻表,发车前检测是否延误

## 特性
- **实时查票**：用户可以通过Web界面查询指定日期和路线的火车票信息。
- **个人车票查询**：输入用户信息后，可以查询到个人已购车票详情。
- **车站大屏信息**：获取车站大屏，实时展示车站检票口、列车到站、离站信息。
- **车站信息获取**：提供接口获取中国铁路车站的基本信息。
- **定时抢票**：支持设置定时任务自动查询余票，并通过多种方式发送通知。
- **第三方推送**：支持邮件、钉钉、企业微信等多种通知方式。
- **列车时刻表**：查询列车时刻表，支持发车提醒和延误检测。
- **友好的Web界面**：提供直观的用户界面，方便操作。

## 技术栈
- **Python**: 使用Python进行爬虫开发，利用其丰富的库支持。
- **Flask**: 基于Flask框架搭建Web服务，提供友好的用户交互界面。
- **Requests**: 用于发起网络请求，获取12306网站数据。
- **APScheduler**: 实现定时任务调度功能。
- **SQLite**: 轻量级数据库，存储车站信息和任务配置。

## 安装与使用
1. 克隆本项目到本地, Windows可以直接使用`TrainAssistant.exe`。
   ```bash
   git clone https://github.com/2375137/12306.git
   ```
2. 安装依赖。
   ```bash
   pip install -r requirements.txt
   ```
3. 运行Flask服务。
   ```bash
   python app.py
   ```
4. 访问 `http://localhost:5000` 开始使用。
   - 首页：功能导航和API文档
   - `/ui/login`：登录页面
   - `/ui/search`：车票查询页面
   - `/ui/schedule`：定时抢票管理
5. API接口请参照以下文档：

### API接口文档
#### 登录相关
- `GET /login/12306?type=get_picture` - 获取登录二维码
- `POST /login/12306?type=check_login` - 检查登录状态
- `POST /login/account` - 账号密码登录
- `GET /login/owner` - Owner登录

#### 车票查询
- `GET /search?type=ticket&begin={起始站}&end={终点站}&date={日期}` - 查询车票
- `GET /search?type=MyQuery&operation=search` - 查询个人车票
- `GET /search?type=StationScreen&station={车站}` - 车站大屏

#### 定时抢票
- `GET /scheduler?operation=add&job_id={ID}&begin={起始站}&end={终点站}&date={日期}&train_no={车次}&interval={间隔}` - 添加抢票任务
- `GET /scheduler?operation=list` - 列出所有任务
- `GET /scheduler?operation=pause&job_id={ID}` - 暂停任务
- `GET /scheduler?operation=resume&job_id={ID}` - 恢复任务
- `GET /scheduler?operation=remove&job_id={ID}` - 删除任务

#### 列车时刻表
- `GET /train_schedule?operation=query&train_no={车次}&date={日期}` - 查询列车时刻表
- `GET /train_schedule?operation=check_delay&train_no={车次}&station_name={站名}&date={日期}` - 检查延误
- `GET /train_schedule?operation=reminder&train_no={车次}&departure_time={发车时间}&station_name={站名}` - 发车提醒

#### 车站信息
- `GET /update_station` - 更新车站信息

## 注意事项
- 本项目仅供学习和研究使用，请遵守相关法律法规，不得用于商业用途。
- 为减轻12306服务器压力，请合理使用爬虫功能。

## 许可证
本项目遵循Apache2.0许可证。
---

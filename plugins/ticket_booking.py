"""
定时抢票功能模块
"""
import json
import requests
from plugins.cookie import get_cookie
from plugins.search_ticket import SearchTicket, Process
from plugins.notification import NotificationManager


class TicketBooking:
    """车票预订功能"""

    def __init__(self):
        self._headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/123.0.0.0 Safari/537.36",
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
            'Origin': 'https://kyfw.12306.cn',
            'Host': 'kyfw.12306.cn'
        }

    def check_ticket_availability(self, begin, end, date, train_no=None):
        """
        检查车票是否可用
        :param begin: 起始站代码
        :param end: 终点站代码
        :param date: 日期 YYYY-MM-DD
        :param train_no: 可选，指定车次
        :return: 是否有票
        """
        try:
            search = SearchTicket(begin, end, date)
            result = search.mobile_search()

            if result.get('status') and result.get('result'):
                tickets = Process().process_mobile_search(result)

                for ticket in tickets:
                    # 如果指定了车次，只检查该车次
                    if train_no and ticket['station_train_code'] != train_no:
                        continue

                    # 检查是否有座位可用
                    if ticket.get('seat_info') and len(ticket['seat_info']) > 0:
                        for seat in ticket['seat_info']:
                            if seat['num'] > 0:
                                return {
                                    'available': True,
                                    'train_no': ticket['station_train_code'],
                                    'seat_type': seat['seat_type'],
                                    'num': seat['num'],
                                    'price': seat['price']
                                }
            return {'available': False, 'msg': '暂无余票'}
        except Exception as e:
            return {'available': False, 'msg': f'查询失败: {str(e)}'}

    def book_ticket(self, begin, end, date, train_no, seat_type, passenger_info):
        """
        预订车票（基础框架）
        :param begin: 起始站
        :param end: 终点站
        :param date: 日期
        :param train_no: 车次
        :param seat_type: 座位类型
        :param passenger_info: 乘客信息
        :return: 预订结果
        """
        # 注意：完整的购票流程需要：
        # 1. 提交订单
        # 2. 确认乘客信息
        # 3. 选择席位
        # 4. 支付
        # 这里提供基础框架，实际购票需要处理更多细节和12306的各种验证

        return {
            'code': '-1',
            'msg': '自动购票功能开发中',
            'tip': '由于12306购票流程复杂且涉及支付，需要用户授权和完善的错误处理'
        }


def scheduled_ticket_check_job(job_id, begin, end, date, train_no, notification_config=None):
    """
    定时任务：检查车票
    :param job_id: 任务ID
    :param begin: 起始站
    :param end: 终点站
    :param date: 日期
    :param train_no: 车次
    :param notification_config: 通知配置（可选）
    """
    booking = TicketBooking()
    result = booking.check_ticket_availability(begin, end, date, train_no)

    if result.get('available'):
        print(f"[抢票任务 {job_id}] 发现余票！车次: {result['train_no']}, "
              f"座位: {result['seat_type']}, 数量: {result['num']}, 价格: {result['price']}")

        # 如果配置了通知，发送通知
        if notification_config:
            try:
                notification_type = notification_config.get('type')
                NotificationManager.send_ticket_notification(
                    notification_type,
                    result,
                    **notification_config
                )
                print(f"[抢票任务 {job_id}] 通知已发送")
            except Exception as e:
                print(f"[抢票任务 {job_id}] 发送通知失败: {str(e)}")
    else:
        print(f"[抢票任务 {job_id}] 暂无余票")

    return result

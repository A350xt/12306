"""
列车时刻表功能模块
"""
import requests
from datetime import datetime


class TrainSchedule:
    """列车时刻表查询"""

    def __init__(self):
        self._headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/123.0.0.0 Safari/537.36",
            'Referer': 'https://kyfw.12306.cn/',
            'Origin': 'https://kyfw.12306.cn',
            'Host': 'kyfw.12306.cn'
        }

    def get_train_schedule(self, train_no, date):
        """
        获取列车时刻表
        :param train_no: 车次号
        :param date: 日期 YYYY-MM-DD
        :return: 时刻表信息
        """
        try:
            # 12306官方时刻表接口
            url = "https://kyfw.12306.cn/otn/czxx/queryByTrainNo"
            params = {
                'train_no': train_no,
                'from_station_telecode': '',
                'to_station_telecode': '',
                'depart_date': date
            }

            response = requests.get(url, headers=self._headers, params=params, timeout=10)
            data = response.json()

            if data.get('httpstatus') == 200 and data.get('data'):
                return {
                    'code': '0',
                    'msg': '查询成功',
                    'schedule': self._parse_schedule(data['data'])
                }
            else:
                return {'code': '-1', 'msg': '查询失败，未找到该车次信息'}
        except Exception as e:
            return {'code': '-1', 'msg': f'查询失败: {str(e)}'}

    def _parse_schedule(self, raw_data):
        """
        解析时刻表数据
        :param raw_data: 原始数据
        :return: 格式化后的时刻表
        """
        if not raw_data or 'data' not in raw_data:
            return []

        schedule = []
        for station in raw_data['data']:
            schedule.append({
                'station_name': station.get('station_name', ''),
                'arrive_time': station.get('arrive_time', ''),
                'start_time': station.get('start_time', ''),
                'stop_time': station.get('stopover_time', '0分钟'),
                'running_time': station.get('running_time', ''),
                'day_diff': station.get('arrive_day_diff', '0'),
                'is_start': station.get('isStart', False),
                'is_end': station.get('isEnd', False)
            })

        return schedule

    def check_delay(self, train_no, station_name, scheduled_time):
        """
        检查列车延误情况（基础实现）
        :param train_no: 车次号
        :param station_name: 站名
        :param scheduled_time: 计划时间
        :return: 延误信息
        """
        # 注意：实际的延误检测需要对接实时数据源
        # 这里提供基础框架
        return {
            'code': '0',
            'msg': '延误检测功能开发中',
            'tip': '需要对接12306实时数据或第三方数据源以获取准确的延误信息'
        }


class DelayDetection:
    """列车延误检测"""

    @staticmethod
    def compare_schedule_with_realtime(train_no, station_name, date):
        """
        对比计划时刻表与实时数据
        :param train_no: 车次号
        :param station_name: 站名
        :param date: 日期
        :return: 延误情况
        """
        schedule_api = TrainSchedule()

        # 获取计划时刻表
        schedule_result = schedule_api.get_train_schedule(train_no, date)

        if schedule_result.get('code') != '0':
            return {'code': '-1', 'msg': '获取时刻表失败'}

        # 查找指定站点
        schedule = schedule_result.get('schedule', [])
        target_station = None

        for station in schedule:
            if station['station_name'] == station_name:
                target_station = station
                break

        if not target_station:
            return {'code': '-1', 'msg': f'未找到站点：{station_name}'}

        # 这里需要实时数据来比对
        # 由于12306不提供公开的实时延误API，可以通过以下方式获取：
        # 1. 爬取车站大屏数据
        # 2. 对接第三方数据源（如智行、携程等）
        # 3. 使用自己的数据采集系统

        return {
            'code': '0',
            'msg': '延误检测基础功能已就绪',
            'scheduled_info': target_station,
            'tip': '需要实时数据源支持才能准确检测延误'
        }

    @staticmethod
    def get_departure_reminder(train_no, departure_time, station_name):
        """
        获取发车提醒
        :param train_no: 车次号
        :param departure_time: 发车时间
        :param station_name: 站名
        :return: 提醒信息
        """
        try:
            # 计算当前时间距离发车的时间差
            now = datetime.now()
            departure = datetime.strptime(departure_time, '%H:%M')
            departure = departure.replace(year=now.year, month=now.month, day=now.day)

            time_diff = (departure - now).total_seconds() / 60  # 转换为分钟

            if time_diff < 0:
                return {'code': '0', 'msg': '列车已发车', 'status': 'departed'}
            elif time_diff <= 30:
                return {
                    'code': '0',
                    'msg': f'列车即将发车！还有{int(time_diff)}分钟',
                    'status': 'urgent',
                    'minutes_left': int(time_diff)
                }
            elif time_diff <= 60:
                return {
                    'code': '0',
                    'msg': f'请准备检票，还有{int(time_diff)}分钟发车',
                    'status': 'prepare',
                    'minutes_left': int(time_diff)
                }
            else:
                return {
                    'code': '0',
                    'msg': f'距离发车还有{int(time_diff)}分钟',
                    'status': 'normal',
                    'minutes_left': int(time_diff)
                }
        except Exception as e:
            return {'code': '-1', 'msg': f'计算发车时间失败: {str(e)}'}

"""
列车时刻表路由处理
"""
from plugins.train_schedule import TrainSchedule, DelayDetection


class Route:
    @staticmethod
    def schedule(request):
        """
        处理列车时刻表相关请求
        :param request: Flask request对象
        :return: 处理结果
        """
        operation = request.args.get('operation')

        if operation == 'query':
            # 查询列车时刻表
            train_no = request.args.get('train_no')
            date = request.args.get('date')

            if not train_no or not date:
                return {'code': '-1', 'msg': '缺少必要参数：train_no, date'}

            schedule_api = TrainSchedule()
            return schedule_api.get_train_schedule(train_no, date)

        elif operation == 'check_delay':
            # 检查列车延误
            train_no = request.args.get('train_no')
            station_name = request.args.get('station_name')
            date = request.args.get('date')

            if not all([train_no, station_name, date]):
                return {'code': '-1', 'msg': '缺少必要参数：train_no, station_name, date'}

            return DelayDetection.compare_schedule_with_realtime(train_no, station_name, date)

        elif operation == 'reminder':
            # 获取发车提醒
            train_no = request.args.get('train_no')
            departure_time = request.args.get('departure_time')
            station_name = request.args.get('station_name')

            if not all([train_no, departure_time, station_name]):
                return {'code': '-1', 'msg': '缺少必要参数：train_no, departure_time, station_name'}

            return DelayDetection.get_departure_reminder(train_no, departure_time, station_name)

        else:
            return {'code': '-1', 'msg': '不支持的操作类型'}

"""
定时抢票路由处理
"""
from plugins.scheduler_manager import SchedulerManager


class Route:
    @staticmethod
    def scheduler(request):
        """
        处理定时任务相关请求
        :param request: Flask request对象
        :return: 处理结果
        """
        operation = request.args.get('operation')

        if operation == 'add':
            # 添加定时任务
            return Route.add_job(request)
        elif operation == 'remove':
            # 删除任务
            job_id = request.args.get('job_id')
            if not job_id:
                return {'code': '-1', 'msg': '缺少job_id参数'}
            return SchedulerManager.remove_job(job_id)
        elif operation == 'pause':
            # 暂停任务
            job_id = request.args.get('job_id')
            if not job_id:
                return {'code': '-1', 'msg': '缺少job_id参数'}
            return SchedulerManager.pause_job(job_id)
        elif operation == 'resume':
            # 恢复任务
            job_id = request.args.get('job_id')
            if not job_id:
                return {'code': '-1', 'msg': '缺少job_id参数'}
            return SchedulerManager.resume_job(job_id)
        elif operation == 'list':
            # 列出所有任务
            return SchedulerManager.list_jobs()
        elif operation == 'info':
            # 获取任务详情
            job_id = request.args.get('job_id')
            if not job_id:
                return {'code': '-1', 'msg': '缺少job_id参数'}
            return SchedulerManager.get_job_info(job_id)
        else:
            return {'code': '-1', 'msg': '不支持的操作类型'}

    @staticmethod
    def add_job(request):
        """
        添加抢票任务
        :param request: Flask request对象
        :return: 添加结果
        """
        # 获取参数
        job_id = request.args.get('job_id')
        begin = request.args.get('begin')
        end = request.args.get('end')
        date = request.args.get('date')
        train_no = request.args.get('train_no')
        interval = request.args.get('interval', '60')

        # 参数校验
        if not all([job_id, begin, end, date, train_no]):
            return {'code': '-1', 'msg': '缺少必要参数：job_id, begin, end, date, train_no'}

        try:
            interval = int(interval)
            if interval < 10:
                return {'code': '-1', 'msg': '检查间隔不能小于10秒'}
        except ValueError:
            return {'code': '-1', 'msg': 'interval参数必须是数字'}

        # 添加任务
        return SchedulerManager.add_ticket_job(job_id, begin, end, date, train_no, interval)

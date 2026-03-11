"""
定时任务管理模块
"""
from whole.Flask import scheduler
from plugins.ticket_booking import scheduled_ticket_check_job
from datetime import datetime


class SchedulerManager:
    """定时任务管理器"""

    @staticmethod
    def add_ticket_job(job_id, begin, end, date, train_no, check_interval=60):
        """
        添加抢票定时任务
        :param job_id: 任务ID（唯一标识）
        :param begin: 起始站代码
        :param end: 终点站代码
        :param date: 日期 YYYY-MM-DD
        :param train_no: 车次号
        :param check_interval: 检查间隔（秒），默认60秒
        :return: 添加结果
        """
        try:
            # 检查任务是否已存在
            existing_job = scheduler.get_job(job_id)
            if existing_job:
                return {'code': '-1', 'msg': '任务ID已存在', 'job_id': job_id}

            # 添加定时任务
            scheduler.add_job(
                id=job_id,
                func=scheduled_ticket_check_job,
                trigger='interval',
                seconds=check_interval,
                args=[job_id, begin, end, date, train_no],
                replace_existing=False,
                max_instances=1
            )

            return {
                'code': '0',
                'msg': '任务添加成功',
                'job_id': job_id,
                'interval': check_interval
            }
        except Exception as e:
            return {'code': '-1', 'msg': f'添加任务失败: {str(e)}'}

    @staticmethod
    def remove_job(job_id):
        """
        删除定时任务
        :param job_id: 任务ID
        :return: 删除结果
        """
        try:
            scheduler.remove_job(job_id)
            return {'code': '0', 'msg': '任务删除成功', 'job_id': job_id}
        except Exception as e:
            return {'code': '-1', 'msg': f'删除任务失败: {str(e)}'}

    @staticmethod
    def pause_job(job_id):
        """
        暂停定时任务
        :param job_id: 任务ID
        :return: 暂停结果
        """
        try:
            scheduler.pause_job(job_id)
            return {'code': '0', 'msg': '任务暂停成功', 'job_id': job_id}
        except Exception as e:
            return {'code': '-1', 'msg': f'暂停任务失败: {str(e)}'}

    @staticmethod
    def resume_job(job_id):
        """
        恢复定时任务
        :param job_id: 任务ID
        :return: 恢复结果
        """
        try:
            scheduler.resume_job(job_id)
            return {'code': '0', 'msg': '任务恢复成功', 'job_id': job_id}
        except Exception as e:
            return {'code': '-1', 'msg': f'恢复任务失败: {str(e)}'}

    @staticmethod
    def list_jobs():
        """
        列出所有定时任务
        :return: 任务列表
        """
        try:
            jobs = scheduler.get_jobs()
            job_list = []
            for job in jobs:
                job_info = {
                    'id': job.id,
                    'name': job.name,
                    'next_run_time': job.next_run_time.strftime('%Y-%m-%d %H:%M:%S') if job.next_run_time else None,
                    'trigger': str(job.trigger)
                }
                job_list.append(job_info)

            return {'code': '0', 'msg': '获取成功', 'jobs': job_list, 'count': len(job_list)}
        except Exception as e:
            return {'code': '-1', 'msg': f'获取任务列表失败: {str(e)}'}

    @staticmethod
    def get_job_info(job_id):
        """
        获取任务详情
        :param job_id: 任务ID
        :return: 任务信息
        """
        try:
            job = scheduler.get_job(job_id)
            if not job:
                return {'code': '-1', 'msg': '任务不存在'}

            job_info = {
                'id': job.id,
                'name': job.name,
                'next_run_time': job.next_run_time.strftime('%Y-%m-%d %H:%M:%S') if job.next_run_time else None,
                'trigger': str(job.trigger),
                'func': job.func.__name__ if job.func else None
            }

            return {'code': '0', 'msg': '获取成功', 'job': job_info}
        except Exception as e:
            return {'code': '-1', 'msg': f'获取任务信息失败: {str(e)}'}

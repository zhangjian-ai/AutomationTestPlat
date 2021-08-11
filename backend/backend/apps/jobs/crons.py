# -*- coding: UTF-8 -*-
import logging

from .models import Job

logger = logging.getLogger('test_plat')


def turn_test_job_status():
    """测试任务状态流转定时任务"""
    logger.info('执行定时任务: turn_test_job_status')

    # 已创建任务且未被指派，则改变状态为待指派
    jobs = Job.objects.filter(status=0, executor__isnull=True)
    if jobs:
        jobs.update(status=1)

    # 已创建任务且已被指派，则改变状态为待测试
    jobs = Job.objects.filter(status=0, executor__isnull=False)
    if jobs:
        jobs.update(status=2)

    # 待指派任务且已被指派，则改变状态为待测试
    jobs = Job.objects.filter(status=1, executor__isnull=False)
    if jobs:
        jobs.update(status=2)

    logger.info('完成定时任务: turn_test_job_status')


if __name__ == '__main__':
    turn_test_job_status()

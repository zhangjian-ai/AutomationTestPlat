import datetime

from django.shortcuts import render
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from jobs.models import Job


class JobInductions(APIView):
    """
    测试任务统计视图
    默认纬度：当前周
    """

    def get(self, request):
        # 获取scope
        scope = request.query_params.get('scope')
        # 按周的纬度
        if scope == 'W':
            scope = '本周'
            # 获取当前周的时间范围
            days = datetime.datetime.now().weekday()  # 获取今天是周几：0～6，0表示周一
            today = datetime.date.today()
            monday = today - datetime.timedelta(days=days)
            sunday = today + datetime.timedelta(days=6 - days)
            # 格式转换
            monday = timezone.datetime.strftime(monday, "%Y-%m-%d") + " 00:00:00"
            sunday = timezone.datetime.strftime(sunday, "%Y-%m-%d") + " 23:59:59"

        # 按预期完成的任务数
        done = Job.objects.filter(expect_end_time__gte=monday, expect_end_time__lte=sunday, status=4,
                                  is_delay=False).count()

        # 延期完成的任务数
        delay_done = Job.objects.filter(expect_end_time__gte=monday, expect_end_time__lte=sunday, status=4,
                                        is_delay=True).count()

        # 挂起的任务数
        block = Job.objects.filter(expect_end_time__gte=monday, expect_end_time__lte=sunday, status=5).count()

        # 预期未完成任务数
        unfinish = Job.objects.filter(expect_end_time__gte=monday, expect_end_time__lte=sunday, status__in=[0, 1, 2, 3],
                                      expect_end_time__gt=datetime.datetime.now()).count()
        # 延期未完成任务数
        deley_unfinish = Job.objects.filter(expect_end_time__gte=monday, expect_end_time__lte=sunday,
                                            status__in=[0, 1, 2, 3],
                                            expect_end_time__lt=datetime.datetime.now()).count()

        data = [
            {'value': done, 'name': '已完成'},
            {'value': delay_done, 'name': '已完成(延期)'},
            {'value': block, 'name': '挂起'},
            {'value': unfinish, 'name': '未完成'},
            {'value': deley_unfinish, 'name': '已延期'},
        ]
        category = [x['name'] for x in data]
        title = '测试任务概况'
        colors = ['#00AA00', '#BBBB00', '#808080', '#6495ED', '#FF4500']

        return Response({'data': data, 'category': category, 'title': title, 'colors': colors, 'scope': scope})

import json
import re
from datetime import datetime

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import JobSerializer, JobToCaseSerializer
from .models import Job, JobToCase
from users.models import User
from django.conf import settings

from backend.utils.fastdfs.FastDFSStorage import FastDFSStorage


class JobView(APIView):
    """测试任务视图"""

    def post(self, request):
        """创建任务"""
        data = request.data

        serializer = JobSerializer(data=data, context=request.user)

        # 创建时如果指定了责任人，那么任务状态直接为待测试
        if data.get('executor'):
            data['status'] = 2

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ValidationError as e:
            return Response({'msg': e.get_full_details()}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'msg': '测试任务创建成功', 'data': serializer.data}, status=status.HTTP_201_CREATED)

    def get(self, request):
        """查询任务"""
        pass

    def put(self, request):
        """修改任务状态"""
        data = request.data
        id = data.pop('id')
        state = data.get('status')

        try:
            job = Job.objects.get(id=id)

            if state == 4:
                relation = JobToCase.objects.filter(job=job, case_status__in=[0, 2, 3])
                if len(relation) != 0:
                    return Response({'msg': '任务尚未完成'}, status=status.HTTP_400_BAD_REQUEST)

                # 判断是否延期
                if job.expect_end_time < datetime.now():
                    data['is_delay'] = True

                # 加上实际结束时间
                data['actual_end_time'] = datetime.now()

            serializer = JobSerializer(instance=job, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Job.DoesNotExist:
            return Response({'msg': '任务不存在'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'data': serializer.data, 'msg': '任务已关闭' if status == 4 else '状态已变更'})


class JobListView(ListAPIView):
    """用例列表视图"""

    serializer_class = JobSerializer

    def get_queryset(self):
        # 获取请求参数，前端传入的对象，被默认转成了字符串：'{}'
        conditions = self.request.query_params.get('conditions')

        if conditions == 'unfinish':
            instance = Job.objects.filter(executor=self.request.user, status__in=[2, 3, 5]).order_by(
                'expect_end_time')

        elif conditions == 'finish':
            instance = Job.objects.filter(executor=self.request.user, status=4).order_by('-actual_end_time')

        else:
            # 把字符串转换成对应的字典
            conditions = json.loads(conditions)

            # 处理掉空值，避免干扰查询
            valid_conditions = dict()
            for key, value in conditions.items():
                if value != "":
                    valid_conditions[key] = value

            # 任务编号和名称提供模糊查询
            task_no = valid_conditions.pop('task_no', "")
            task_name = valid_conditions.pop('task_name', "")

            instance = Job.objects.filter(**valid_conditions, task_name__contains=task_name,
                                          task_no__icontains=task_no).order_by('expect_end_time')

        return instance


class DispatchJobView(APIView):
    """指派任务视图"""

    def put(self, request):
        user_id = request.data.get('user_id')
        job_ids = request.data.get('job_ids')

        querySet = Job.objects.filter(id__in=job_ids)

        if not querySet:
            return Response({'msg': '要指派的测试任务不存在'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'msg': '被指派人不存在'}, status=status.HTTP_400_BAD_REQUEST)

        querySet.update(executor=user, status=2)

        return Response({'msg': '任务指派完成'})


class JobCaseListView(ListAPIView):
    """单个任务下的用例列表"""

    serializer_class = JobToCaseSerializer

    def get_queryset(self):
        job_id = self.kwargs['id']

        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({'msg': '测试任务不存在'}, status=status.HTTP_400_BAD_REQUEST)

        case = JobToCase.objects.filter(job=job)
        return case


class TestResultView(APIView):
    """测试结果视图"""

    def post(self, request):
        # 获取关联id
        data = request.data
        id = data.pop('id')

        try:
            relation = JobToCase.objects.get(id=id)

            # 更新用例时可能会删除掉一些图片，所以跟新时检查原来的图片是否还在用，没用就删除
            if relation.test_detail:
                ids = re.findall(rf'<img src="{settings.FDFS_URL}(.+?)">', relation.test_detail)
                if ids:
                    storage = FastDFSStorage()
                    for id in ids:
                        if id not in data['test_detail']:
                            storage.delete(id)
            # 修改测试任务状态
            if relation.job.status == 2:
                relation.job.status = 3
                relation.job.save()

            serializer = JobToCaseSerializer(instance=relation, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except JobToCase.DoesNotExist:
            return Response({'msg': '任务和用例无关联'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'data': serializer.data, 'msg': '保存成功'})

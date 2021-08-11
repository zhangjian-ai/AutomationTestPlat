import json
import time

import xmindparser
from django.db import transaction, DatabaseError

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Client, Module, Case
from .serializer import CaseSerializer, ClientSerializer, ModuleSerializer, JobClientSerializer


class ScriptUploadCaseView(APIView):
    """
    脚本上传用例视图
    """

    def post(self, request):
        # 获取数据
        data = request.data.get('data')
        # 校验列表是否为空
        if not data or not isinstance(data, list):
            return Response({'msg': '参数为空或格式错误，期望格式是list'}, status=status.HTTP_400_BAD_REQUEST)
        # 统计变量
        total = len(data)
        success = list()
        fail = list()
        message = set()

        for case in data:
            # 检查用例所属端、功能模块、owner
            case_id = case.get('case_id')
            client = case.pop('client')
            module = case.pop('module')
            try:
                client_obj = Client.objects.get(name=client)
                module_obj = Module.objects.get(name=module, client=client_obj)
            except Client.DoesNotExist:
                message.add(f'当前应用[{client}]不存在，请先添加')
                fail.append(case_id)
            except Module.DoesNotExist:
                message.add(f'当前应用[{client}]无功能模块[{module}]，请先添加')
                fail.append(case_id)
            else:
                # 校验通过，则为导入数据添加外键对象
                case['client_id'] = client_obj.id
                case['module_id'] = module_obj.id

                serializer = CaseSerializer(data=case, context=request.user)

                try:
                    serializer.is_valid(raise_exception=True)
                except Exception as e:
                    message.add(f'[{case["case_id"]}]用例校验失败:\n>{e}')
                    fail.append(case_id)
                else:
                    try:
                        serializer.save()
                    except Exception as e:
                        message.add(f'[{case["case_id"]}]写入数据库失败:\n>{e}')
                        fail.append(case_id)
                    else:
                        success.append(case_id)

        return Response({'success': success, 'fail': fail, 'total': total, 'msg': message},
                        status=status.HTTP_201_CREATED)


class ClientView(APIView):
    """应用视图"""

    def get(self, request):
        instance = Client.objects.all()
        serializer = ClientSerializer(instance=instance, many=True)

        return Response(serializer.data)

    def post(self, request):
        data = request.data

        serializer = ClientSerializer(data=data, context=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ModuleView(APIView):
    """功能模块视图"""

    def get(self, request):
        instance = Module.objects.all()
        serializer = ClientSerializer(instance=instance, many=True)

        return Response(serializer.data)

    def post(self, request):
        data = request.data

        serializer = ModuleSerializer(data=data, context=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CaseListView(ListAPIView):
    """用例列表视图"""

    serializer_class = CaseSerializer

    def get_queryset(self):
        # 获取请求参数，前端传入的对象，被默认转成了字符串：'{}'
        conditions = self.request.query_params.get('conditions')
        # 把字符串转换成对应的字典
        conditions = json.loads(conditions)

        # 处理掉空值，避免干扰查询
        valid_conditions = dict()
        for key, value in conditions.items():
            if value != "":
                valid_conditions[key] = value

        # 用例编号和名称提供模糊查询
        case_id = valid_conditions.pop('case_id', "")
        case_name = valid_conditions.pop('case_name', "")

        instance = Case.objects.filter(**valid_conditions, case_name__contains=case_name, case_id__icontains=case_id,
                                       status=True).order_by('-create_time')

        return instance


class CaseView(APIView):
    """
    用例视图
    """

    serializer_class = CaseSerializer

    def get(self, request):
        """查询用例"""
        case_id = request.query_params.get('case_id')

        try:
            case = Case.objects.get(case_id=case_id)
        except Case.DoesNotExist:
            return Response({'msg': '用例不存在'})
        else:
            serializer = CaseSerializer(instance=case)
            return Response(serializer.data)

    def post(self, request):
        """手动新增用例"""
        data = request.data

        data['owner'] = request.user.nickname
        data['add_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        serializer = CaseSerializer(data=data, context=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'msg': '用例添加成功'}, status=status.HTTP_201_CREATED)

    def put(self, request):
        """修改用例"""
        data = request.data
        id = data.pop('id')
        case_id = data.get('case_id')

        try:
            case = Case.objects.get(id=id, case_id=case_id)
        except Case.DoesNotExist:
            return Response({'msg': '用例不存在'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = CaseSerializer(instance=case, data=data, context=request.user)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({'msg': '保存修改成功'})

    def delete(self, request):
        """删除用例"""
        data = request.data
        id = data.get('id')
        case_id = data.get('case_id')

        try:
            case = Case.objects.get(id=id, case_id=case_id)
        except Case.DoesNotExist:
            return Response({'msg': '用例不存在'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            case.status = False
            case.save()
            return Response({'msg': '用例删除完成'})


class XmindUploadCaseView(APIView):
    """xmind用例导入视图"""

    def post(self, request):
        # 获取上传文件内容
        content = request.data.get('file')

        # xmind转成dict
        xmind_dict = xmindparser.xmind_to_dict(content)

        # 定义一个用例等级映射字典
        level_mapping = {
            'priority-1': 'H',
            'priority-2': 'M',
            'priority-3': 'L'
        }

        # 写入数据库
        success = list()
        serializer_list = list()

        # 用例筛选校验
        for sheet in xmind_dict:
            app_name = sheet.get('topic').get('title')
            for module in sheet.get('topic').get('topics'):
                module_name = module.get('title')
                # 校验测试应用及模块是否存在
                try:
                    client_obj = Client.objects.get(name=app_name)
                    module_obj = Module.objects.get(name=module_name, client=client_obj)
                except Client.DoesNotExist as e:
                    error = f'[{content.__str__()}]-应用[{app_name}]不存在，请先添加'
                    return Response({'error': error})
                except Module.DoesNotExist as e:
                    error = f'[{content.__str__()}]-应用[{app_name}]无功能模块[{module_name}]，请先添加'
                    return Response({'error': error})
                else:
                    for case in module.get('topics'):
                        case_name = case.get('title')
                        for info in case.get('topics'):
                            case_id = info.get('title')
                            level = level_mapping.get(info.get("makers")[0], 'M')
                            step = ''
                            for sub_step in info.get('topics'):
                                step += sub_step.get('title') + ' \n '

                            single_case = dict()
                            single_case['client_id'] = client_obj.id
                            single_case['module_id'] = module_obj.id
                            single_case['case_name'] = case_name
                            single_case['case_id'] = case_id
                            single_case['level'] = level
                            single_case['step'] = step
                            single_case['owner'] = request.user.nickname
                            # 默认导入当天为用例编写时间
                            single_case['add_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                            serializer = CaseSerializer(data=single_case, context=request.user)

                            try:
                                serializer.is_valid(raise_exception=True)
                            except ValidationError as e:
                                error = f'[{content.__str__()}]-[{single_case["case_id"]}]用例编号已存在' if '用例编号' in f'{e}' else f'[{content.__str__()}]-[{single_case["case_id"]}]校验异常:\n >{e}'
                                return Response({'error': error})
                            else:
                                serializer_list.append(serializer)

        # 开启事物，写入数据库
        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
                for serializer in serializer_list:
                    serializer.save()
                    success.append(f'[{content.__str__()}]-[{serializer.validated_data["case_id"]}]')
            except DatabaseError as e:
                # 有任何异常都回退并返回
                transaction.savepoint_rollback(save_id)

                error = f'[{content.__str__()}]中用例写入数据库失败:\n >{e}'
                return Response({'error': error})
            except Exception:
                # 有任何异常都回退并返回
                transaction.savepoint_rollback(save_id)

                return Response({'error': '惊！发生未知异常！！！'})
            else:
                # 无异常就提交事物
                transaction.savepoint_commit(save_id)

                return Response({'count': len(success), 'success': success}, status=status.HTTP_201_CREATED)


class JobCaseListView(APIView):
    """Job任务用例列表"""

    def get(self, request):
        querySet = Client.objects.all()
        serializer = JobClientSerializer(instance=querySet, many=True)

        return Response(serializer.data)

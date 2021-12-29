import json
import random
import time
import traceback
import logging
from datetime import datetime

import xmindparser
from django.db import transaction, DatabaseError

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Module, Case
from .serializer import CaseSerializer, ModuleSerializer, CaseDetailSerializer, CaseTreeSerializer
from backend.utils.custom_permissions import ModulePermission

logger = logging.getLogger('test_plat')


class ModuleView(APIView):
    """功能模块视图"""

    permission_classes = [IsAuthenticated, ModulePermission]

    def get(self, request):
        instance = Module.objects.filter(parent=None)
        serializer = ModuleSerializer(instance=instance, many=True)

        # 将[] 改成 null，避免前端界面展示空级联
        json_data = json.dumps(serializer.data)
        json_data = json_data.replace('"subs": []', '"subs": null')

        return Response(json.loads(json_data))

    def post(self, request):
        data = request.data

        serializer = ModuleSerializer(data=data, context=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        logger.info(f"模块创建成功：【{serializer.data['name']}】")
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
            if value not in ("", None):
                valid_conditions[key] = value

        # 用例编号和名称提供模糊查询
        no = valid_conditions.pop('no', "")
        name = valid_conditions.pop('name', "")

        # 创建时间为范围匹配
        code_time = valid_conditions.pop('code_time', None)
        if code_time:
            instance = Case.objects.filter(**valid_conditions, name__contains=name, no__icontains=no,
                                           code_time__gte=code_time[0], code_time__lte=code_time[1],
                                           status=True).order_by('-create_time')
        else:
            instance = Case.objects.filter(**valid_conditions, name__contains=name, no__icontains=no,
                                           status=True).order_by('-create_time')

        return instance


class CaseView(APIView):
    """
    用例视图
    """

    serializer_class = CaseSerializer

    def get(self, request):
        """查询用例"""
        id = request.query_params.get('id')

        if id:
            try:
                case = Case.objects.get(id=id)
            except Case.DoesNotExist:
                logger.warning(f"用例不存在，ID：{id}")
                return Response({'msg': '用例不存在'})
            else:
                serializer = CaseSerializer(instance=case)
                detail_serializer = CaseDetailSerializer(instance=case.detail)
                base = serializer.data
                detail = detail_serializer.data
                base.update(detail)
                return Response(base)
        else:
            no = request.query_params.get('no')
            try:
                Case.objects.get(no=no)
            except Case.DoesNotExist:
                logger.warning(f"用例不存在，NO.：{no}")
                return Response({'msg': '用例不存在'})
            else:
                return Response()

    def post(self, request):
        """手动新增用例"""
        data = request.data

        # 无用例编号时，自动添加
        if not data.get('no'):
            data['no'] = 'test_' + '{0:%Y%m%d%H%M%S}'.format(datetime.now()) + str(random.randint(0, 9999)).zfill(4)

        # 校验模块下用例名称
        try:
            Case.objects.get(name=data['name'], module=data['module'])
        except Case.DoesNotExist:
            pass
        else:
            logger.warning(f"模块中已存在同名用例，NAME：{data['name']}")
            error = f"模块中已存在同名用例 [{data['name']}]"
            return Response({'msg': error}, status=status.HTTP_400_BAD_REQUEST)

        data['author'] = request.user.nickname
        data['creator'] = request.user.id
        data['code_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        serializer = CaseSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        logger.warning(f"用例添加成功，id：{serializer.data['id']}")
        return Response({'msg': '用例添加成功', 'data': serializer.data}, status=status.HTTP_201_CREATED)

    def put(self, request):
        """修改用例"""
        data = request.data
        id = data.pop('id')

        try:
            case = Case.objects.get(id=id)
        except Case.DoesNotExist:
            logger.warning(f"用例不存在，ID：{id}")
            return Response({'msg': '用例不存在'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 修改用例
            for key, value in data.items():
                if hasattr(case, key):
                    if key == 'module':
                        try:
                            module = Module.objects.get(id=value)
                        except Case.DoesNotExist:
                            logger.error(traceback.format_exc())
                            return Response({'msg': '当前勾选的模块不在系统中'}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            setattr(case, key, module)
                            continue
                    if key == 'is_auto' and not value:
                        setattr(case, key, value)
                        setattr(case.detail, 'path', None)
                        setattr(case, 'version', None)
                        setattr(case, 'type', None)
                        continue

                    setattr(case, key, value)
                elif hasattr(case.detail, key):
                    setattr(case.detail, key, value)

            # 更新修改人及修改时间
            setattr(case, 'reviser', request.user)
            setattr(case, 'update_time', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

            # 保存修改
            case.save()
            case.detail.save()

            return Response({'msg': '保存修改成功'})

    def delete(self, request):
        """删除用例"""
        data = request.data
        id = data.get('id')

        try:
            case = Case.objects.get(id=id)
        except Case.DoesNotExist:
            logger.warning(f"用例不存在，ID：{id}")
            return Response({'msg': '用例不存在'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            case.status = False
            case.save()
            logger.warning(f"用例已删除，ID：{case.id}")
            return Response({'msg': '用例已删除'})


class CaseTreeView(APIView):
    """Job任务用例列表"""

    def get(self, request):
        queryset = Module.objects.filter(parent=None)
        serializer = CaseTreeSerializer(instance=queryset, many=True)

        # 处理响应数据
        def make_result(items: list):
            for item in items:
                if item.get('subs'):
                    make_result(item.get('subs'))

                # 当模块下面无用例时，则不可选中
                if not item.get('cases'):
                    item['disabled'] = True

                for module in item['subs']:
                    if not module.get('disabled', False):
                        item['disabled'] = False
                        break

                # 将用例加到subs列表，方便前端解析
                item['subs'].extend(item.pop('cases'))

        make_result(serializer.data)

        return Response(serializer.data)


class XmindUploadCaseView(APIView):
    """xmind用例导入视图"""

    def post(self, request):
        # 获取上传文件内容
        content = request.data.get('file')

        # xmind转成dict
        xmind_dict = xmindparser.xmind_to_dict(content)

        # 定义一个用例等级映射字典
        level_mapping = {
            'priority-1': 1,
            'priority-2': 2,
            'priority-3': 3
        }

        # 写入数据库
        success = list()
        serializer_list = list()
        ids = list()

        # 用例筛选校验
        for sheet in xmind_dict:
            # 校验根级模块
            name = sheet.get('topic').get('title')
            try:
                ins_module = Module.objects.get(name=name, parent_id=None)
            except Module.DoesNotExist:
                error = f'[{content.__str__()}] - [{name}] 不存在'
                logger.error(traceback.format_exc())
                return Response({'error': error})

            for module_1 in sheet.get('topic').get('topics'):
                # 校验一级模块
                if module_1.get("makers"):
                    error = f'[{content.__str__()}]-  [{name}] 下级必须是功能模块'
                    logger.error(error)
                    return Response({'error': error})
                name_1 = module_1.get('title')
                try:
                    ins_module_1 = Module.objects.get(name=name_1, parent=ins_module)
                except Module.DoesNotExist:
                    error = f'[{content.__str__()}]-[{name}] 下无模块 [{name_1}]，请先添加'
                    logger.error(error)
                    return Response({'error': error})

                for module_2 in module_1.get('topics'):
                    # 校验二级模块
                    if not module_2.get("makers"):
                        name_2 = module_2.get('title')
                        try:
                            ins_module_2 = Module.objects.get(name=name_2, parent=ins_module_1)
                        except Module.DoesNotExist:
                            error = f'[{content.__str__()}]-模块 [{name_1}] 下无模块 [{name_2}] ，请先添加'
                            logger.error(error)
                            return Response({'error': error})

                        # 用例信息
                        case_list = module_2.get('topics')
                    else:
                        ins_module_2 = None
                        case_list = [module_2]

                    # 搜集用例信息
                    for case in case_list:
                        if not case.get("makers"):
                            error = f"[{content.__str__()}] - 用例 [{case.get('title')}] 用例等级必填"
                            logger.error(error)
                            return Response({'error': error})

                        # 校验同一模块下是否有同名用例
                        name = case.get('title')
                        try:
                            ins = Case.objects.get(name=name,
                                                   module=ins_module_2 if ins_module_2 else ins_module_1)
                        except Case.DoesNotExist:
                            pass
                        else:
                            error = f'[{content.__str__()}] - 模块 [{name_1}] 中已存在用例 [{name}]  状态: {"可用" if ins.status else "不可用"}'
                            logger.error(error)
                            return Response({'error': error})

                        priority = level_mapping.get(case.get("makers")[0], 2)

                        if case.get('topics'):
                            info = case.get('topics')[0]
                            step = info.get('title')
                            expectation = info.get('topics')[0].get('title') if info.get('topics') else None
                        else:
                            step = None
                            expectation = None

                        single_case = dict()
                        single_case['no'] = 'test_' + '{0:%Y%m%d%H%M%S}'.format(datetime.now()) + str(
                            random.randint(0, 9999)).zfill(4)
                        single_case['module'] = ins_module_2.id if ins_module_2 else ins_module_1.id
                        single_case['name'] = name
                        single_case['priority'] = priority
                        single_case['step'] = step
                        single_case['expectation'] = expectation
                        single_case['author'] = request.user.nickname
                        single_case['creator'] = request.user.id
                        # 默认导入当天为用例编写时间
                        single_case['code_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                        serializer = CaseSerializer(data=single_case)

                        try:
                            serializer.is_valid(raise_exception=True)
                        except ValidationError as e:
                            error = f'[{content.__str__()}] - [{single_case["name"]}] 用例编号已存在' if '用例编号' in f'{e}' else f'[{content.__str__()}] - [{single_case["name"]}] 校验异常:\n >{e}'
                            logger.error(error)
                            return Response({'error': error})
                        else:
                            serializer_list.append(serializer)

        # 开启事物，写入数据库
        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
                for serializer in serializer_list:
                    serializer.save()
                    success.append(f'[{content.__str__()}]-[{serializer.validated_data["name"]}]')
                    ids.append(serializer.data.get('id'))
            except DatabaseError as e:
                # 有任何异常都回退并返回
                transaction.savepoint_rollback(save_id)
                error = f'[{content.__str__()}] 用例写入数据库失败:\n >{e}'
                logger.error(traceback.format_exc())
                return Response({'error': error})
            except Exception as e:
                # 有任何异常都回退并返回
                transaction.savepoint_rollback(save_id)
                logger.error(traceback.format_exc())
                return Response({'error': f'惊！发生未知异常！！！ \n {e}'})
            else:
                # 无异常就提交事物
                transaction.savepoint_commit(save_id)
                logger.error(f'[{content.__str__()}] 用例导入完成！')
                return Response({'count': len(success), 'success': success, 'ids': ids}, status=status.HTTP_201_CREATED)


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
                client_obj = Module.objects.get(name=client)
                module_obj = Module.objects.get(name=module, client=client_obj)
            except Module.DoesNotExist:
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

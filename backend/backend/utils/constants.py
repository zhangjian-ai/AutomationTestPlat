# 短信验证码的过期时间单位秒
import time

SMS_CODE_EXPIRES = 300

# 短信验证码发送时间周期
SMS_CODE_INTERVAL = 60

# 测试短信模板ID
SMS_TEMPLATE_ID = 1

# 静态资源
RESOURCE = {
    'IMAGE': [(0, 'login'), (1, 'logo'), (2, 'auto_true'), (3, 'auto_false'), (4, 'loading')],
    'FILE': [(0, 'xmind_template')]
}

# 测试用例常量
CASE = {
    'LEVEL': [(1, '高'), (2, '中'), (3, '低')]
}

# 测试任务常量
JOB = {
    'STATUS': [(0, '已创建'), (1, '待指派'), (2, '待测试'), (3, '测试中'), (4, '已完成'), (5, '已挂起')],
    'TYPE': [(0, 'DEV任务'), (1, 'PUB任务'), (2, '生产任务'), (3, '回归任务'), (4, '冒烟任务')],
    'LEVEL': [(0, '紧急'), (1, '重要'), (2, '一般'), (3, '普通')],
    'CASE_STATUS': [(0, 'WAIT'), (1, 'PASS'), (2, 'FAIL'), (3, 'BLOCK'), (4, 'BREAK')]
}

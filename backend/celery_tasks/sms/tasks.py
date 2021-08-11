import logging
from celery_tasks.main import celery_app

from celery_tasks.sms.yuntongxun.sms import CCP

logger = logging.getLogger('test_plat')


@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, code, expires, temp_id):
    """
    异步发送短信验证码
    :param mobile: 手机号
    :param code: 验证码
    :param expires: 过期时间 s
    :param temp_id: 短信模板ID
    :return: None
    """

    try:
        ccp = CCP()
        res = ccp.send_template_sms(mobile, datas=[code, expires // 60], temp_id=temp_id)
    except Exception as e:
        logger.error("发送验证码短信[异常][ mobile: %s, message: %s ]" % (mobile, e))
    else:
        if res == 0:
            logger.info("发送验证码短信[正常][ mobile: %s ]" % mobile)
        else:
            logger.error("发送验证码短信[失败][ mobile: %s ]" % mobile)

"""
第三方推送通知模块
支持邮件、Webhook等多种通知方式
"""
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailNotification:
    """邮件通知"""

    def __init__(self, smtp_host='smtp.gmail.com', smtp_port=587):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port

    def send(self, from_email, password, to_email, subject, content):
        """
        发送邮件
        :param from_email: 发件人邮箱
        :param password: 邮箱密码或应用专用密码
        :param to_email: 收件人邮箱
        :param subject: 邮件主题
        :param content: 邮件内容
        :return: 发送结果
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject

            msg.attach(MIMEText(content, 'html', 'utf-8'))

            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(from_email, password)
            server.send_message(msg)
            server.quit()

            return {'code': '0', 'msg': '邮件发送成功'}
        except Exception as e:
            return {'code': '-1', 'msg': f'邮件发送失败: {str(e)}'}


class WebhookNotification:
    """Webhook通知（适用于企业微信、钉钉、飞书等）"""

    @staticmethod
    def send(webhook_url, data):
        """
        发送Webhook通知
        :param webhook_url: Webhook地址
        :param data: 通知数据（JSON格式）
        :return: 发送结果
        """
        try:
            response = requests.post(webhook_url, json=data, timeout=10)
            if response.status_code == 200:
                return {'code': '0', 'msg': 'Webhook发送成功', 'response': response.json()}
            else:
                return {'code': '-1', 'msg': f'Webhook发送失败: HTTP {response.status_code}'}
        except Exception as e:
            return {'code': '-1', 'msg': f'Webhook发送失败: {str(e)}'}


class DingTalkNotification:
    """钉钉机器人通知"""

    @staticmethod
    def send_text(webhook_url, content, at_mobiles=None, is_at_all=False):
        """
        发送钉钉文本消息
        :param webhook_url: 钉钉机器人Webhook地址
        :param content: 消息内容
        :param at_mobiles: @的手机号列表
        :param is_at_all: 是否@所有人
        :return: 发送结果
        """
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": {
                "atMobiles": at_mobiles or [],
                "isAtAll": is_at_all
            }
        }
        return WebhookNotification.send(webhook_url, data)

    @staticmethod
    def send_markdown(webhook_url, title, text):
        """
        发送钉钉Markdown消息
        :param webhook_url: 钉钉机器人Webhook地址
        :param title: 消息标题
        :param text: Markdown内容
        :return: 发送结果
        """
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            }
        }
        return WebhookNotification.send(webhook_url, data)


class WeChatWorkNotification:
    """企业微信机器人通知"""

    @staticmethod
    def send_text(webhook_url, content, mentioned_list=None):
        """
        发送企业微信文本消息
        :param webhook_url: 企业微信机器人Webhook地址
        :param content: 消息内容
        :param mentioned_list: @的用户列表
        :return: 发送结果
        """
        data = {
            "msgtype": "text",
            "text": {
                "content": content,
                "mentioned_list": mentioned_list or []
            }
        }
        return WebhookNotification.send(webhook_url, data)

    @staticmethod
    def send_markdown(webhook_url, content):
        """
        发送企业微信Markdown消息
        :param webhook_url: 企业微信机器人Webhook地址
        :param content: Markdown内容
        :return: 发送结果
        """
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }
        return WebhookNotification.send(webhook_url, data)


class NotificationManager:
    """通知管理器"""

    @staticmethod
    def send_ticket_notification(notification_type, ticket_info, **kwargs):
        """
        发送车票通知
        :param notification_type: 通知类型 (email, dingtalk, wechat)
        :param ticket_info: 车票信息
        :param kwargs: 其他参数（如邮箱配置、Webhook地址等）
        :return: 发送结果
        """
        # 构造通知内容
        title = "🎫 12306车票余票提醒"
        content = f"""
检测到余票信息！

车次：{ticket_info.get('train_no', '未知')}
座位类型：{ticket_info.get('seat_type', '未知')}
剩余数量：{ticket_info.get('num', 0)}
价格：¥{ticket_info.get('price', 0)}

请及时登录12306进行购票！
        """

        if notification_type == 'email':
            from_email = kwargs.get('from_email')
            password = kwargs.get('password')
            to_email = kwargs.get('to_email')
            if not all([from_email, password, to_email]):
                return {'code': '-1', 'msg': '缺少邮件配置参数'}

            email_notifier = EmailNotification()
            return email_notifier.send(from_email, password, to_email, title, content)

        elif notification_type == 'dingtalk':
            webhook_url = kwargs.get('webhook_url')
            if not webhook_url:
                return {'code': '-1', 'msg': '缺少钉钉Webhook地址'}

            return DingTalkNotification.send_markdown(webhook_url, title, content)

        elif notification_type == 'wechat':
            webhook_url = kwargs.get('webhook_url')
            if not webhook_url:
                return {'code': '-1', 'msg': '缺少企业微信Webhook地址'}

            return WeChatWorkNotification.send_markdown(webhook_url, content)

        else:
            return {'code': '-1', 'msg': '不支持的通知类型'}

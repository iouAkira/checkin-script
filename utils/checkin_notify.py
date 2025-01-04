import requests

from checkin.checkin_2bulu import log


def notify(notify_config, message):
    bot_token = notify_config["telegram"]["bot_token"]
    chat_id = notify_config["telegram"]["chat_id"]

    # 发送消息
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        log.logger.info("通知发送成功")
    else:
        log.logger.error(f"通知发送失败，状态码: {response.status_code}")

import requests
from utils.logger import log

class CheckinLanjing:
    def __init__(self, account_config):
        self.checkin_url = "https://p0245.api.asiatic.online/portal-api/mp/activity/signIn"
        self.headers = {
            "Content-Length": "59",
            "X-Access-Token": account_config["token"],
            "content-type": "application/json",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.56(0x18003831) NetType/WIFI Language/zh_CN",
            "Accept-Encoding": "gzip,compress,br,deflate",
            "Referer": "https://servicewechat.com/wx6bd635a01d288b76/68/page-frame.html",
            "Host": "p0245.api.asiatic.online"
        }
        self.mall_id = account_config.get("mall_id", "1547404683667185667")
        self.checkin_msg = ""

    def do_checkin(self):
        data = {
            "{\"id\":\"1557211367844347906\",\"mallId\":\"" + self.mall_id + "\"}" : ""
        }
        try:
            response = requests.post(self.checkin_url, headers=self.headers, json=data)
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    self.checkin_msg = "签到成功！"
                    log.logger.info("蓝鲸世界签到成功")
                    return True
                elif result.get("code") == 1 and "今日已签到" in result.get("message", ""):
                    self.checkin_msg = "今日已签到！"
                    log.logger.info("蓝鲸世界今日已签到")
                    return True
                else:
                    self.checkin_msg = f"签到失败：{result.get('message')}"
                    log.logger.error(f"蓝鲸世界签到失败：{result}")
                    return False
            else:
                self.checkin_msg = f"请求失败，状态码：{response.status_code}"
                log.logger.error(f"蓝鲸世界签到请求失败，状态码：{response.status_code}")
                return False
        except Exception as e:
            self.checkin_msg = f"签到异常：{str(e)}"
            log.logger.error(f"蓝鲸世界签到异常：{str(e)}")
            return False

    def run_checkin(self):
        if self.do_checkin():
            return self.checkin_msg
        return "签到失败"
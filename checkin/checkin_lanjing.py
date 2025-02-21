import requests
from utils.logger import log

class CheckinLanjing:
    def __init__(self, account_config):
        self.base_url = "https://p0245.api.asiatic.online"
        self.checkin_url = f"{self.base_url}/portal-api/mp/activity/signIn"
        self.token_url = f"{self.base_url}/portal-api/mp/home/tokenByMaCode"
        self.mall_list_url = f"{self.base_url}/portal-api/mp/home/mallList"
        self.base_headers = {
            "content-type": "application/json",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.56(0x18003831) NetType/WIFI Language/zh_CN",
            "Accept-Encoding": "gzip,compress,br,deflate",
            "Referer": "https://servicewechat.com/wx6bd635a01d288b76/68/page-frame.html",
            "Host": "p0245.api.asiatic.online"
        }
        self.mall_id = account_config.get("mall_id", "1547404683667185667")
        self.code = account_config["code"]
        self.token = None
        self.checkin_msg = ""

    def get_mall_list(self):
        try:
            response = requests.get(self.mall_list_url, headers=self.base_headers)
            if response.status_code == 200:
                log.logger.info("蓝鲸世界获取商场列表成功")
                return True
            else:
                log.logger.error(f"蓝鲸世界获取商场列表失败，状态码：{response.status_code}")
                return False
        except Exception as e:
            log.logger.error(f"蓝鲸世界获取商场列表异常：{str(e)}")
            return False

    def get_token(self):
        # 先获取商场列表
        if not self.get_mall_list():
            return False

        params = {
            "mallId": self.mall_id,
            "code": self.code
        }
        try:
            response = requests.get(self.token_url, headers=self.base_headers, params=params)
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    self.token = result["result"]["token"]
                    log.logger.info("蓝鲸世界获取token成功")
                    return True
                else:
                    self.checkin_msg += f"获取token失败：{result.get('message')}"
                    log.logger.error(f"蓝鲸世界获取token失败，响应：{result}")
                    return False
            else:
                self.checkin_msg += f"获取token请求失败，状态码：{response.status_code}"
                log.logger.error(f"蓝鲸世界获取token请求失败，状态码：{response.status_code}")
                return False
        except Exception as e:
            self.checkin_msg += f"获取token异常：{str(e)}"
            log.logger.error(f"蓝鲸世界获取token异常：{str(e)}")
            return False

    def do_checkin(self):
        if not self.token:
            if not self.get_token():
                return False

        data = {
            "id":"1557211367844347906",
            "mallId": self.mall_id
        }
        headers = self.base_headers.copy()
        headers["X-Access-Token"] = self.token
        try:
            response = requests.post(self.checkin_url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    self.checkin_msg += "签到成功！"
                    log.logger.info("蓝鲸世界签到成功")
                    return True
                elif result.get("code") == 1 and "今日已签到" in result.get("message", ""):
                    self.checkin_msg += "今日已签到！"
                    log.logger.info("蓝鲸世界今日已签到")
                    return True
                else:
                    self.checkin_msg += f"签到失败：{result.get('message')}"
                    log.logger.error(f"蓝鲸世界签到失败，请求头：{self.headers}，请求体：{data}，响应：{result}")
                    return False
            else:
                self.checkin_msg += f"请求失败，状态码：{response.status_code}"
                log.logger.error(f"蓝鲸世界签到请求失败，状态码：{response.status_code}，请求头：{self.headers}，请求体：{data}，response：{response.text}")
                return False
        except Exception as e:
            self.checkin_msg += f"签到异常：{str(e)}"
            log.logger.error(f"蓝鲸世界签到异常：{str(e)}，请求头：{self.headers}，请求体：{data}")
            return False

    def run_checkin(self):
        if self.do_checkin():
            return self.checkin_msg
        return "签到失败"
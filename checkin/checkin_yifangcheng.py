import requests
from utils.logger import log

class CheckinYifangcheng:
    def __init__(self, account_config):
        self.base_url = "https://yxapi.uniworld-sz.cn"
        self.checkin_url = f"{self.base_url}/foreign/sign/doSign"
        self.query_result_url = f"{self.base_url}/foreign/sign/queryVipSignResult"
        self.headers = {
            "Host": "yxapi.uniworld-sz.cn",
            "content-type": "application/json",
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip,compress,br,deflate",
            "Cookie": account_config["token"],
            "Referer": "https://servicewechat.com/wxcfa72ba1cb73037f/232/page-frame.html",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.56(0x18003831) NetType/WIFI Language/zh_CN",
            "token": account_config["token"]
        }
        self.mall_id = account_config.get("mall_id", "000001")
        self.checkin_msg = ""

    def do_checkin(self):
        params = {
            "mallId": self.mall_id,
            "inMallFlag": "0"
        }
        try:
            response = requests.get(self.checkin_url, headers=self.headers, params=params)
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 200:
                    handle_uuid = result["data"]["handleUuid"]
                    self.checkin_msg += "签到成功！"
                    log.logger.info("壹方城签到成功")
                    return handle_uuid
                elif result.get("code") == 1 and "今日已签到" in result.get("message", ""):
                    self.checkin_msg += "今日已签到！"
                    log.logger.info("壹方城今日已签到")
                    return None
                else:
                    self.checkin_msg += f"签到失败：{result.get('msg')}"
                    log.logger.error(f"壹方城签到失败，请求头：{self.headers}，请求参数：{params}，响应：{result}")
                    return None
            else:
                self.checkin_msg += f"请求失败，状态码：{response.status_code}"
                log.logger.error(f"壹方城签到请求失败，状态码：{response.status_code}，请求头：{self.headers}，请求参数：{params}")
                return None
        except Exception as e:
            self.checkin_msg += f"签到异常：{str(e)}"
            log.logger.error(f"壹方城签到异常：{str(e)}，请求头：{self.headers}，请求参数：{params}")
            return None

    def query_sign_result(self, handle_uuid):
        if not handle_uuid:
            return

        params = {"handleUuid": handle_uuid}
        try:
            response = requests.get(self.query_result_url, headers=self.headers, params=params)
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 200:
                    data = result.get("data", {})
                    records = result.get("records", [])
                    if records:
                        points = records[0].get("couponValue", 0)
                        self.checkin_msg += f"\n获得积分：{points}"
                    status = data.get("handleStatus")
                    if status == "succ":
                        log.logger.info("壹方城签到积分查询成功")
                    else:
                        log.logger.warning(f"壹方城签到积分状态异常：{status}")
                else:
                    log.logger.error(f"壹方城签到积分查询失败，请求头：{self.headers}，请求参数：{params}，响应：{result}")
            else:
                log.logger.error(f"壹方城签到积分查询请求失败，状态码：{response.status_code}，请求头：{self.headers}，请求参数：{params}")
        except Exception as e:
            log.logger.error(f"壹方城签到积分查询异常：{str(e)}，请求头：{self.headers}，请求参数：{params}")

    def run_checkin(self):
        handle_uuid = self.do_checkin()
        if handle_uuid:
            self.query_sign_result(handle_uuid)
        return self.checkin_msg
import requests
import json
from utils.logger import log

class CheckinGoldPrice:
    def __init__(self, account_config):
        self.url = "https://www.kaka-tech.com/Kaka/api/services/app/goldKindsPage/GetPriceCacheItemsByCodeAsync"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.56(0x1800382d) NetType/4G Language/zh_CN",
            "Content-Type": "application/json",
            "Cookie": account_config.get("cookie", ""),
            "Host": "www.kaka-tech.com",
            "Referer": "https://servicewechat.com/wx63977453b4cc6d6c/27/page-frame.html"
        }
        self.payload = {"value": ["au9999", "pt", "ag9999"]}
        self.checkin_msg = ""

    def get_gold_prices(self):
        """
        获取黄金、铂金、白银价格
        :return: 价格信息字典或None
        """
        try:
            response = requests.post(
                self.url, 
                headers=self.headers, 
                data=json.dumps(self.payload),
                verify=False  # 禁用SSL验证，对应curl中的-k参数
            )
            response.raise_for_status()
            data = response.json()

            if data.get("success", False):
                prices = {}
                for item in data.get("result", []):
                    prices[item["code"]] = {
                        "name": item["displayName"],
                        "today_price": item["todayPrice"],
                        "put_in_price": item["putInPrice"],
                        "recycling_price": item["recyclingPrice"]
                    }
                
                # 构建消息
                self.checkin_msg = "今日金属价格:\n"
                for code, price_info in prices.items():
                    self.checkin_msg += (
                        f"{price_info['name']}({code}):\n"
                        f"  今日价格: {price_info['today_price']}\n"
                        f"  进价: {price_info['put_in_price']}\n"
                        f"  回收价: {price_info['recycling_price']}\n\n"
                    )
                
                log.logger.info("成功获取金属价格")
                return prices
            else:
                log.logger.error("获取金属价格失败")
                return None

        except Exception as e:
            log.logger.error(f"获取金属价格时发生错误: {e}")
            return None

    def run_checkin(self):
        """
        执行金价获取任务
        :return: 任务执行结果
        """
        result = self.get_gold_prices()
        return "金价获取成功" if result else "金价获取失败"

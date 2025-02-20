import requests

from utils.logger import log


class Checkin2bulu:
    def __init__(self, account_config):
        self.get_storage_url = "https://helper.2bulu.com/dataSpace/getStorageSpace"
        self.claim_capacity_url = "https://helper.2bulu.com/dataSpace/claimCapacity"
        self.headers = {
            "Host": "helper.2bulu.com",
            "Accept": "*/*",
            "Cookie": account_config["cookie"],
            "User-Agent": "region:CN;lan:zh-Hans;OutdoorAssistantApplication/7.8.9 (lolaage.2bulu.zhushou; build:7.8.9.1; iOS 18.1.1) Alamofire/5.9.1",
            "Accept-Language": "zh-Hans;q=1.0, zh-Hans-CN;q=0.9",
            "Accept-Encoding": "br;q=1.0, gzip;q=0.9, deflate;q=0.8",
            "Connection": "keep-alive"
        }
        self.params = account_config["params"]
        self.tasks = account_config["tasks"]
        self.checkin_msg = ""

    def get_storage_space(self):
        response = requests.get(self.get_storage_url,
                                headers=self.headers, params=self.params)
        if response.status_code == 200:
            data = response.json()
            if data.get("errCode") == "0":
                return data
            else:
                log.logger.error(f"请求失败，请求头：{self.headers}，请求参数：{self.params}，响应：{data}")
                return None
        else:
            log.logger.error(f"请求失败，状态码：{response.status_code}，请求头：{self.headers}，请求参数：{self.params}")
            return None

    def claim_capacity(self, task_id):
        claim_params = self.params.copy()
        claim_params["taskId"] = task_id
        claim_params["psign"] = "665e41951979e44cb99413"
        response = requests.post(
            self.claim_capacity_url, headers=self.headers, params=claim_params)
        if response.status_code == 200:
            data = response.json()
            if data.get("errCode") == "0":
                log.logger.info("签到成功")
                return True
            else:
                log.logger.error(f"签到失败，请求头：{self.headers}，请求参数：{claim_params}，响应：{data}")
                return False
        else:
            log.logger.error(f"请求失败，状态码：{response.status_code}，请求头：{self.headers}，请求参数：{claim_params}")
            return False

    def run_checkin(self):
        before_storage_data = self.get_storage_space()
        sum_capacity = before_storage_data["data"]["sumCapacity"]
        self.checkin_msg += f"签到前容量: {sum_capacity / 1024 / 1024:.2f} MB \n"
        if before_storage_data:
            task_infos = before_storage_data["data"]["dataSpaceTaskInfos"]
            for task in task_infos:
                for config_task in self.tasks:
                    if task["name"] == config_task["name"]:
                        if task["status"] == 2:
                            self.checkin_msg += f"任务 {config_task['name']} 已完成，任务跳过"
                        elif task["status"] == 1:
                            log.logger.info(f"任务 {config_task['name']} 还未执行，准备执行")
                            if self.claim_capacity(config_task["taskId"]):
                                after_storage_data = self.get_storage_space()
                                sum_capacity = after_storage_data["data"]["sumCapacity"]
                                use_capacity = after_storage_data["data"]["useCapacity"]
                                self.checkin_msg += f"签到后容量: {sum_capacity / 1024 / 1024:.2f} MB\n"
                                self.checkin_msg += f"当前已使用容量: {use_capacity / 1024 / 1024:.2f} MB"
                                return f"任务 {config_task['name']} 签到成功"
                            else:
                                return f"任务 {config_task['name']} 签到失败"
        return "签到流程执行失败"

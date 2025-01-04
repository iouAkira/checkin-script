import yaml
import time
from checkin.checkin_2bulu import Checkin2bulu
from utils.checkin_notify import notify
from utils.logger import log


def load_config():
    with open("/data/checkin/config.yaml", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def main():
    config = load_config()

    # 遍历每种类型（2bulu、xxx、vvv）
    for task_type, task_config in config.items():
        if task_type == "notify":
            continue  # 跳过通知配置

        log.logger.info(f"正在处理任务类型: {task_type}")

        for account in task_config["accounts"]:
            log.logger.info(f"正在处理账号: {account['name']}")
            checkin = Checkin2bulu(account)
            checkin.checkin_msg = f"🚶两步路账号: {account['name']} \n\n****************************\n"
            result = checkin.run_checkin()
            log.logger.info(result)
            print(checkin.checkin_msg)
            # 发送通知
            notify(config["notify"], checkin.checkin_msg)
            time.sleep(5)


if __name__ == "__main__":
    main()

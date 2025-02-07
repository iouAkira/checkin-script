import yaml
import time
import os
import random
import sys
from checkin.checkin_2bulu import Checkin2bulu
from checkin.daily_gold_price import CheckinGoldPrice
from utils.checkin_notify import notify
from utils.logger import log
from datetime import datetime, time as datetime_time


def load_config():
    # 从系统环境变量 MNT_DIR 目录的 checkin 文件夹中读取 config.yaml 文件
    mnt_dir = os.getenv("MNT_DIR")
    config_path = None

    if mnt_dir:
        config_path = os.path.join(mnt_dir, "checkin", "config.yaml")
        if not os.path.exists(config_path):
            log.logger.warning(f"未在 {config_path} 找到配置文件，尝试在当前目录查找。")
            config_path = None

    # 如果未找到配置文件，则尝试在当前目录查找
    if not config_path:
        config_path = "config.yaml"
        if not os.path.exists(config_path):
            log.logger.error("未找到配置文件，请确保 config.yaml 文件存在。")
            raise FileNotFoundError("未找到配置文件，请确保 config.yaml 文件存在。")

    # 读取配置文件
    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def main():
    config = load_config()

    # 获取命令行传入的任务类型
    task_type = sys.argv[1] if len(sys.argv) > 1 else None

    # 遍历每种类型（2bulu、gold_price）
    for current_task_type, task_config in config.items():
        if current_task_type == "notify":
            continue  # 跳过通知配置

        # 如果指定了任务类型，只处理指定的任务类型
        if task_type and current_task_type != task_type:
            continue

        log.logger.info(f"正在处理任务类型: {current_task_type}")

        # 处理两步路签到
        if current_task_type == "2bulu":
            for account in task_config["accounts"]:
                log.logger.info(f"正在处理账号: {account['name']}")
                # 休眠随机秒数
                random_seconds = random.randint(1, 240)
                log.logger.info(f"随机休眠 {random_seconds} 秒...")
                time.sleep(random_seconds)
                log.logger.info("随机休眠结束，继续执行脚本。")
                checkin = Checkin2bulu(account)
                checkin.checkin_msg = f"🚶两步路账号: {account['name']} \n\n****************************\n"
                result = checkin.run_checkin()
                log.logger.info(result)
                print(checkin.checkin_msg)
                # 发送通知
                notify(config["notify"], checkin.checkin_msg)
                time.sleep(5)

        # 处理金价获取
        if current_task_type == "gold_price":
            for account in task_config["accounts"]:
                log.logger.info("开始获取金价")
                checkin = CheckinGoldPrice(account)
                result = checkin.run_checkin()
                log.logger.info(result)
                
                # 发送通知
                notify(config["notify"], checkin.checkin_msg)
                time.sleep(5)


if __name__ == "__main__":
    main()

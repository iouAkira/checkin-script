# 自动签到脚本 (Checkin Script)

## 项目简介
这是一个自动化签本脚本，主要用于自动完成网站或平台的每日签到任务。目前支持：
- 两步路（2bulu）平台签到
- 水贝金属价格获取

## 功能特点
- 支持多账号签到
- 随机休眠机制，模拟真实用户行为
- 日志记录
- 签到结果通知
- 每日早8点获取金属价格

## 环境依赖
- Python 3.x
- 依赖库：
  - PyYAML
  - 其他依赖请查看 `requirements.txt`

## 安装步骤
1. 克隆仓库
```bash
git clone https://github.com/yourusername/checkin-script.git
cd checkin-script
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

## 配置文件
使用 `config-example.yaml` 作为模板创建 `config.yaml`。配置文件支持多个账号和签到类型。

### 配置示例
```yaml
2bulu:
  accounts:
    - name: "账号1"
      username: "your_username"
      password: "your_password"
    - name: "账号2"
      username: "another_username"
      password: "another_password"

notify:
  # 通知配置（可选）
```

## 运行脚本
### 直接运行
```bash
# 运行所有任务
python checkin.py

# 指定运行特定任务类型
python checkin.py 2bulu
python checkin.py gold_price
```

### 使用定时任务脚本
```bash
# 为两步路签到创建定时任务（默认每天7:40执行）
./iou-entry.sh -t 2bulu

# 为金价获取创建定时任务（可自定义执行时间）
./iou-entry.sh -t gold_price -c "0 8 * * *"
```

### 参数说明
- `-t, --task_type`：指定任务类型（2bulu, gold_price）
- `-c, --cron_time`：自定义定时任务执行时间（默认：40 7 * * *）
- `-h, --help`：显示帮助信息

## 高级使用
- 支持从系统环境变量 `MNT_DIR` 读取配置文件
- 随机休眠机制，避免被识别为机器人

## 日志
日志将记录每次签到的详细信息，方便追踪执行状态。

## 注意事项
- 请妥善保管 `config.yaml` 中的敏感信息
- 遵守各平台的使用条款

## 许可证
本项目基于 MIT 许可证开源。详情请查看 `LICENSE` 文件。

## 贡献
欢迎提交 Issues 和 Pull Requests！

# 自动签到脚本 (Checkin Script)

## 项目简介
这是一个自动化签到脚本，主要用于自动完成网站或平台的每日签到任务和信息获取。目前支持：
- 两步路（2bulu）平台签到
- 水贝金属价格获取
- 蓝鲸世界签到
- 壹方城签到

## 功能特点
- 支持多账号签到
- 灵活的任务类型选择
- 随机休眠机制，模拟真实用户行为
- 详细日志记录
- 签到结果通知
- 定时任务支持

## 环境依赖
- Python 3.x
- 依赖库：
  - PyYAML
  - requests
  - datetime
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

gold_price:
  accounts:
    - name: "水贝金价"
      cookie: "your_cookie"

lanjing:
  accounts:
    - name: "蓝鲸世界账号1"
      token: "your_access_token"
      mall_id: "1547404683667185667"

yifangcheng:
  accounts:
    - name: "壹方城账号1"
      token: "your_token"
      mall_id: "000001"

notify:
  # 通知配置（可选）
```

## 运行脚本
### 手动运行
```bash
# 执行两步路签到
python checkin.py 2bulu

# 获取金价
python checkin.py gold_price

# 蓝鲸世界签到
python checkin.py lanjing

# 壹方城签到
python checkin.py yifangcheng
```

### 定时任务
使用 `iou-entry.sh` 配置定时任务，默认：
- 两步路签到：每天 7:40 AM
- 金价获取：每天 8:10 AM

## 注意事项
- 请妥善保管 `config.yaml` 中的敏感信息
- 建议使用虚拟环境管理依赖
- 如遇网络问题，请检查网络连接和 API 状态

## 贡献与反馈
欢迎提交 Issues 和 Pull Requests！

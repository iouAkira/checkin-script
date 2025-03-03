echo "数据挂载目录： [$MNT_DIR]"
echo "仓库存放目录： [$REPOS_DIR]"
echo "本地挂载目录： [$LOCAL_DIR]"
echo "任务文件目录： [$CRON_FILE_DIR]"
echo "当前执行目录： [$PWD]"

checkin_DIR="$PWD"
checkin_DATA_DIR="$MNT_DIR/checkin"
checkin_CRON_FILE_PATH="$CRON_FILE_DIR/checkin_cron.sh"

if [ ! -d "$checkin_DATA_DIR" ]; then
    mkdir -p $checkin_DATA_DIR
fi

# 判断$checkin_DATA_DIR 里面如果没有config.yaml文件的话，就复制config-example.yaml到该目录
if [ ! -f "$checkin_DATA_DIR/config.yaml" ]; then
    cp "$checkin_DIR/config-example.yaml" "$checkin_DATA_DIR/config.yaml"
    echo "已复制 config-example.yaml 到 $checkin_DATA_DIR 并重命名为 config.yaml"
fi

# 判断 yaml 模块是否已安装，如果未安装则使用 pip3 安装
if ! python3 -c "import yaml" &>/dev/null; then
    pip3 install Pyyaml
fi

echo "仓库数据路径：$checkin_DATA_DIR"
echo "仓库定时任务文件：$checkin_CRON_FILE_PATH"
echo "同步配置文件..."

echo "" >$checkin_CRON_FILE_PATH
echo "#定时任务 checkin.py" >>$checkin_CRON_FILE_PATH
echo "40 7 * * * cd $checkin_DIR; python3 checkin.py 2bulu >$checkin_DATA_DIR/checkin.log " >>$checkin_CRON_FILE_PATH
echo "45 7 * * * cd $checkin_DIR; python3 checkin.py lanjing >$checkin_DATA_DIR/checkin.log " >>$checkin_CRON_FILE_PATH
echo "50 7 * * * cd $checkin_DIR; python3 checkin.py yifangcheng >$checkin_DATA_DIR/checkin.log " >>$checkin_CRON_FILE_PATH
echo "0 8 * * * cd $checkin_DIR; python3 checkin.py gold_price >$checkin_DATA_DIR/checkin.log " >>$checkin_CRON_FILE_PATH

#!/bin/bash

# 同步上游仓库并清洗数据的脚本

# 设置上游仓库地址（请替换为实际的上游仓库 URL）
UPSTREAM_URL="https://github.com/username/upstream-repo.git"
UPSTREAM_BRANCH="main"

# 如果还没有添加 upstream remote，取消下面注释并修改 URL
# git remote add upstream $UPSTREAM_URL

echo "正在从上游仓库获取最新数据..."
git fetch upstream || git fetch origin

# 合并上游更新（根据实际情况选择分支）
git merge upstream/$UPSTREAM_BRANCH || git merge origin/$UPSTREAM_BRANCH

echo "数据同步完成，开始清洗数据..."

# 运行 Python 清洗脚本
python3 clean_data.py

echo "数据清洗完成！"

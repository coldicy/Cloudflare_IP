#!/bin/bash

# 自动同步上游仓库并清洗数据的脚本
# 用法：./sync_and_clean.sh [upstream_url] [branch]

set -e

# 默认配置
UPSTREAM_URL="${1:-https://github.com/ORIGINAL_OWNER/ORIGINAL_REPO.git}"
UPSTREAM_BRANCH="${2:-main}"

echo "=========================================="
echo "自动同步并清洗数据"
echo "=========================================="
echo "上游仓库：$UPSTREAM_URL"
echo "分支：$UPSTREAM_BRANCH"
echo ""

# 检查是否已添加 upstream remote
if ! git remote | grep -q "^upstream$"; then
    echo "添加 upstream remote..."
    git remote add upstream "$UPSTREAM_URL" || true
fi

echo "正在从上游仓库获取最新数据..."
git fetch upstream || git fetch origin

# 合并上游更新
echo "正在合并上游更新..."
git merge upstream/$UPSTREAM_BRANCH || git merge origin/$UPSTREAM_BRANCH || echo "没有新的上游更新"

echo ""
echo "数据同步完成，开始清洗数据..."
echo ""

# 运行 Python 清洗脚本
python3 clean_data.py

echo ""
echo "=========================================="
echo "✅ 全部完成！"
echo "=========================================="

#!/bin/bash

# ============================================
# Git 提交脚本
# 用法: bash git-commit.sh "提交信息"
# ============================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_error() { echo -e "${RED}[ERROR]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }

# 检查参数
if [[ -z "$1" ]]; then
    print_error "请提供提交信息"
    echo "用法: bash $0 \"提交信息\""
    exit 1
fi

COMMIT_MSG="$1"

echo "========================================"
echo "Git 提交: $COMMIT_MSG"
echo "========================================"

# 检查是否是 git 仓库
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_error "当前目录不是 Git 仓库"
    exit 1
fi

# 显示变更状态
echo ""
print_info() { echo -e "[INFO] $1"; }
print_info "变更文件:"
git status --short

echo ""
read -p "确认提交? (y/n): " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "已取消"
    exit 0
fi

# 执行 git 操作
echo ""
print_info "执行 git add..."
git add .

print_info "执行 git commit..."
git commit -m "$COMMIT_MSG"

print_info "执行 git push..."
git push origin main

echo ""
print_success "提交完成!"

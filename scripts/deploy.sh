#!/bin/bash

# Deployment script for AI Stack Blog
# 部署脚本

set -e

echo "========================================"
echo "AI Stack Blog Deployment Script"
echo "========================================"

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo -e "${BLUE}Project root:${NC} $PROJECT_ROOT"

# 1. 生成内容
echo -e "\n${YELLOW}[1/3]${NC} Generating content..."
python3 scripts/generate_content.py
echo -e "${GREEN}✓ Content generation completed${NC}"

# 2. 构建 Hugo 站点
echo -e "\n${YELLOW}[2/3]${NC} Building Hugo site..."
cd blog
hugo --minify --cleanDestinationDir
echo -e "${GREEN}✓ Hugo site built${NC}"
cd ..

# 3. 部署到 GitHub Pages
echo -e "\n${YELLOW}[3/3]${NC} Deploying to GitHub Pages..."
echo "Please use GitHub Actions for automatic deployment"
echo "Or manually deploy with: gh-pages deploy"

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment preparation completed!${NC}"
echo -e "${GREEN}========================================${NC}"

#!/bin/bash

# Setup script for AI Stack Blog
# 环境设置脚本

set -e

echo "========================================"
echo "AI Stack Blog Setup Script"
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

# 1. 检查 Python 版本
echo -e "\n${YELLOW}[1/5]${NC} Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ Python found:${NC} $PYTHON_VERSION"
else
    echo -e "${YELLOW}⚠ Python 3 not found. Please install Python 3.11 or later.${NC}"
    exit 1
fi

# 2. 创建虚拟环境
echo -e "\n${YELLOW}[2/5]${NC} Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠ Virtual environment already exists${NC}"
fi

# 3. 激活虚拟环境
echo -e "\n${YELLOW}[3/5]${NC} Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# 4. 安装依赖
echo -e "\n${YELLOW}[4/5]${NC} Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# 5. 创建配置文件
echo -e "\n${YELLOW}[5/5]${NC} Creating configuration files..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
    else
        cat > .env << 'EOF'
ANTHROPIC_AUTH_TOKEN=your_anthropic_token
ANTHROPIC_BASE_URL=https://api.minimaxi.com/anthropic
ANTHROPIC_MODEL=MiniMax-M2.7-highspeed
EOF
    fi
    echo -e "${GREEN}✓ .env file created${NC}"
    echo -e "${YELLOW}⚠ Please edit .env with your API keys${NC}"
else
    echo -e "${YELLOW}⚠ .env file already exists${NC}"
fi

# 完成
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Setup completed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"

echo -e "\n${BLUE}Next steps:${NC}"
echo "1. Edit .env file with your API keys"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python3 scripts/preflight.py"
echo "4. Run: ./scripts/run_local.sh --skip-build"
echo "5. Run: ./scripts/run_local.sh --serve"

echo -e "\n${BLUE}For deployment:${NC}"
echo "1. Push to GitHub repository"
echo "2. Configure GitHub Actions secrets"
echo "3. GitHub Actions will auto-deploy"

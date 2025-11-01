#!/bin/bash

echo "🎮 Life Game System - Setup Script"
echo "=================================="
echo ""

# 检查 Docker
echo "🔍 Checking Docker..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker Desktop first."
    echo "   Download from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi
echo "✅ Docker is ready"
echo ""

# 检查 Python
echo "🔍 Checking Python..."

# 优先使用 Python 3.10-3.12（避免 3.13 的兼容性问题）
PYTHON_CMD=""
if command -v python3.12 &> /dev/null; then
    PYTHON_CMD="python3.12"
elif command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
elif command -v python3.10 &> /dev/null; then
    PYTHON_CMD="python3.10"
elif [ -f "/opt/homebrew/opt/python@3.12/bin/python3.12" ]; then
    PYTHON_CMD="/opt/homebrew/opt/python@3.12/bin/python3.12"
elif [ -f "/opt/homebrew/opt/python@3.11/bin/python3.11" ]; then
    PYTHON_CMD="/opt/homebrew/opt/python@3.11/bin/python3.11"
elif [ -f "/opt/homebrew/opt/python@3.10/bin/python3.10" ]; then
    PYTHON_CMD="/opt/homebrew/opt/python@3.10/bin/python3.10"
elif command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    if [[ "$PYTHON_VERSION" == "3.13" ]]; then
        echo "⚠️  Python 3.13 detected but some dependencies are not yet compatible."
        echo "   Please install Python 3.10, 3.11, or 3.12:"
        echo "   brew install python@3.12"
        exit 1
    fi
    PYTHON_CMD="python3"
else
    echo "❌ Python 3 not found. Please install Python 3.10-3.12."
    echo "   Recommended: brew install python@3.12"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version | cut -d' ' -f2)
echo "✅ Using Python $PYTHON_VERSION ($PYTHON_CMD)"
echo ""

# 检查 Node.js
echo "🔍 Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18 or higher."
    exit 1
fi
NODE_VERSION=$(node --version)
echo "✅ Node.js $NODE_VERSION found"
echo ""

# 设置后端
echo "📦 Setting up backend..."
cd backend

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "   Creating Python virtual environment with $PYTHON_CMD..."
    $PYTHON_CMD -m venv venv
fi

# 激活虚拟环境并安装依赖
source venv/bin/activate
echo "   Upgrading pip..."
pip install --upgrade pip
echo "   Installing Python dependencies (this may take a few minutes)..."
pip install -r requirements.txt

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  Creating .env file..."
    cat > .env << 'EOF'
# OpenAI API Key (必填)
OPENAI_API_KEY=your_openai_api_key_here

# Database URL
DATABASE_URL=postgresql://gameuser:gamepass@localhost:5432/life_game_db

# 如果使用 Anthropic Claude，取消下面这行注释并填入 API Key
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
EOF
    echo ""
    echo "✅ .env file created with OpenRouter configuration"
    echo "   Using model: qwen/qwen-max"
    echo "   See OPENROUTER_SETUP.md for more details"
    echo ""
fi

cd ..
echo "✅ Backend setup complete"
echo ""

# 设置前端
echo "📦 Setting up frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "   Installing Node.js dependencies (this may take a while)..."
    npm install
else
    echo "   Dependencies already installed"
fi

cd ..
echo "✅ Frontend setup complete"
echo ""

# 启动数据库
echo "🗄️  Starting PostgreSQL database..."
docker-compose up -d

echo "   Waiting for database to be ready..."
sleep 5

# 检查数据库状态
if docker-compose ps | grep -q "Up"; then
    echo "✅ Database is running"
else
    echo "❌ Database failed to start. Check Docker logs:"
    echo "   docker-compose logs postgres"
    exit 1
fi

echo ""
echo "=================================="
echo "✨ Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "  1. The system is configured to use OpenRouter (qwen/qwen-max)"
echo "  2. Run './start.sh' to start all services"
echo "  3. Open http://localhost:5173 in your browser"
echo "  4. API docs: http://localhost:8089/docs"
echo ""
echo "For more information, see QUICKSTART.md"
echo ""


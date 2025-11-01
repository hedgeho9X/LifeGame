#!/bin/bash

echo "🚀 Starting Backend Server..."
echo ""

# 检查虚拟环境
if [ ! -d "backend/venv" ]; then
    echo "❌ Virtual environment not found. Please run ./setup.sh first."
    exit 1
fi

# 检查环境变量文件
if [ ! -f "backend/.env" ]; then
    echo "⚠️  .env file not found. Please create backend/.env file with your API keys."
    echo "   See backend/.env.example for reference."
    exit 1
fi

# 检查数据库
if ! docker-compose ps | grep -q "Up"; then
    echo "⚠️  Database is not running. Starting it now..."
    docker-compose up -d
    echo "⏳ Waiting for database to be ready..."
    sleep 5
fi

# 启动后端
cd backend
source venv/bin/activate

echo "✅ Backend server starting at http://localhost:8089"
echo "📚 API docs at http://localhost:8089/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python main.py


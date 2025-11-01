#!/bin/bash

echo "🎮 Starting Life Game System..."
echo ""
echo "ℹ️  Note: For easier debugging, you can start services separately:"
echo "   Terminal 1: ./start-backend.sh"
echo "   Terminal 2: ./start-frontend.sh"
echo ""
echo "   Or continue with this script to start all services together."
echo ""
read -p "Continue with combined startup? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled. Please use start-backend.sh and start-frontend.sh separately."
    exit 0
fi
echo ""

# 检查 Docker 是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# 启动数据库
echo "📦 Starting PostgreSQL database..."
docker-compose up -d

# 等待数据库就绪
echo "⏳ Waiting for database to be ready..."
sleep 5

# 检查是否安装了 Python 依赖
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

# 启动后端
echo "🚀 Starting backend server..."
cd backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ..

# 等待后端启动
sleep 3

# 检查是否安装了前端依赖
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

# 启动前端
echo "🎨 Starting frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ All services started!"
echo ""
echo "📍 Access the application at: http://localhost:5173"
echo "📍 Backend API at: http://localhost:8089"
echo "📍 API docs at: http://localhost:8089/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# 等待用户中断
trap "kill $BACKEND_PID $FRONTEND_PID; docker-compose down; exit" INT
wait


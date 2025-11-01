#!/bin/bash

echo "🎨 Starting Frontend Server..."
echo ""

# 检查是否安装了前端依赖
if [ ! -d "frontend/node_modules" ]; then
    echo "❌ Frontend dependencies not found. Please run ./setup.sh first."
    exit 1
fi

# 启动前端
cd frontend

echo "✅ Frontend server starting at http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop"
echo ""

npm run dev


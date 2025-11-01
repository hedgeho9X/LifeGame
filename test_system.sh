#!/bin/bash

echo "🧪 Testing Life Game System"
echo "============================"
echo ""

# 测试数据库
echo "1️⃣  Testing Database..."
if docker-compose ps | grep -q "postgres.*Up"; then
    echo "   ✅ PostgreSQL is running"
    
    # 测试连接
    if docker-compose exec -T postgres pg_isready -U gameuser > /dev/null 2>&1; then
        echo "   ✅ Database connection OK"
    else
        echo "   ❌ Cannot connect to database"
        exit 1
    fi
else
    echo "   ❌ PostgreSQL is not running"
    echo "   Run: docker-compose up -d"
    exit 1
fi
echo ""

# 测试后端
echo "2️⃣  Testing Backend..."
BACKEND_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8089/ 2>/dev/null)

if [ "$BACKEND_RESPONSE" = "200" ]; then
    echo "   ✅ Backend server is responding"
    
    # 测试 API 文档
    DOCS_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8089/docs 2>/dev/null)
    if [ "$DOCS_RESPONSE" = "200" ]; then
        echo "   ✅ API documentation is available at http://localhost:8089/docs"
    fi
else
    echo "   ❌ Backend server is not responding"
    echo "   Is it running? Check: ps aux | grep uvicorn"
    exit 1
fi
echo ""

# 测试前端
echo "3️⃣  Testing Frontend..."
FRONTEND_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5173/ 2>/dev/null)

if [ "$FRONTEND_RESPONSE" = "200" ]; then
    echo "   ✅ Frontend server is responding"
    echo "   ✅ Application available at http://localhost:5173"
else
    echo "   ❌ Frontend server is not responding"
    echo "   Is it running? Check: ps aux | grep vite"
    exit 1
fi
echo ""

# 测试 API 创建用户
echo "4️⃣  Testing API Functionality..."
USER_RESPONSE=$(curl -s -X POST "http://localhost:8089/api/users" \
    -H "Content-Type: application/json" \
    -d '{"name":"测试用户","background":"测试背景"}' 2>/dev/null)

if echo "$USER_RESPONSE" | grep -q "id"; then
    echo "   ✅ User creation API works"
    USER_ID=$(echo "$USER_RESPONSE" | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
    echo "   Created test user with ID: $USER_ID"
else
    echo "   ⚠️  User creation API might have issues"
    echo "   Response: $USER_RESPONSE"
fi
echo ""

echo "============================"
echo "✨ System Test Complete!"
echo "============================"
echo ""
echo "All components are running. You can:"
echo "  • Visit the app: http://localhost:5173"
echo "  • Check API docs: http://localhost:8089/docs"
echo "  • View database: docker-compose exec postgres psql -U gameuser -d life_game_db"
echo ""


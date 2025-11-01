#!/usr/bin/env python3
"""
数据库迁移脚本 - 添加话疗券系统和夸赞弹幕功能
"""
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# 获取数据库连接信息
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://gameuser:gamepass@localhost:5432/life_game_db")

# 解析连接字符串
parts = DATABASE_URL.replace("postgresql://", "").split("@")
user_pass = parts[0].split(":")
host_db = parts[1].split("/")
host_port = host_db[0].split(":")

user = user_pass[0]
password = user_pass[1]
host = host_port[0]
port = host_port[1] if len(host_port) > 1 else "5432"
database = host_db[1]

print(f"🔗 连接数据库: {database}@{host}:{port}")

try:
    # 连接数据库
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    print("✅ 数据库连接成功")
    
    # 1. 添加 goals.praise_messages 字段
    print("\n📝 检查 goals 表的 praise_messages 字段...")
    cursor.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name='goals' AND column_name='praise_messages';
    """)
    
    if cursor.fetchone() is None:
        print("➕ 添加 praise_messages 字段到 goals 表...")
        cursor.execute("""
            ALTER TABLE goals 
            ADD COLUMN praise_messages JSON DEFAULT '[]';
        """)
        print("✅ praise_messages 字段添加成功")
    else:
        print("✅ praise_messages 字段已存在")
    
    # 2. 创建 therapy_tickets 表
    print("\n📝 检查 therapy_tickets 表...")
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'therapy_tickets'
        );
    """)
    
    if not cursor.fetchone()[0]:
        print("➕ 创建 therapy_tickets 表...")
        cursor.execute("""
            CREATE TABLE therapy_tickets (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id),
                goal_id INTEGER NOT NULL REFERENCES goals(id),
                used BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
                used_at TIMESTAMP WITHOUT TIME ZONE
            );
        """)
        print("✅ therapy_tickets 表创建成功")
    else:
        print("✅ therapy_tickets 表已存在")
    
    # 3. 创建 therapy_conversations 表
    print("\n📝 检查 therapy_conversations 表...")
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'therapy_conversations'
        );
    """)
    
    if not cursor.fetchone()[0]:
        print("➕ 创建 therapy_conversations 表...")
        cursor.execute("""
            CREATE TABLE therapy_conversations (
                id SERIAL PRIMARY KEY,
                ticket_id INTEGER NOT NULL REFERENCES therapy_tickets(id),
                role VARCHAR(50) NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
            );
        """)
        print("✅ therapy_conversations 表创建成功")
    else:
        print("✅ therapy_conversations 表已存在")
    
    print("\n🎉 数据库迁移完成！")
    print("\n新功能：")
    print("  ✨ 夸赞弹幕系统（goals.praise_messages）")
    print("  🎁 话疗券系统（therapy_tickets）")
    print("  💬 话疗对话（therapy_conversations）")
    
    cursor.close()
    conn.close()
    
except psycopg2.Error as e:
    print(f"❌ 数据库错误: {e}")
    print(f"\n💡 提示：请确保 PostgreSQL 正在运行，且连接信息正确")
    exit(1)
except Exception as e:
    print(f"❌ 错误: {e}")
    exit(1)


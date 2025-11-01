.PHONY: help setup start stop clean test logs db-shell

help:
	@echo "🎮 Life Game System - Make Commands"
	@echo "===================================="
	@echo ""
	@echo "Setup commands:"
	@echo "  make setup       - Initial setup (install dependencies)"
	@echo "  make start       - Start all services"
	@echo "  make stop        - Stop all services"
	@echo ""
	@echo "Development commands:"
	@echo "  make test        - Run system tests"
	@echo "  make logs        - View all logs"
	@echo "  make db-shell    - Open PostgreSQL shell"
	@echo ""
	@echo "Cleanup commands:"
	@echo "  make clean       - Stop services and clean data"
	@echo "  make reset       - Complete reset (delete all data)"
	@echo ""

setup:
	@echo "🔧 Running setup..."
	@./setup.sh

start:
	@echo "🚀 Starting all services..."
	@./start.sh

stop:
	@echo "⏹️  Stopping all services..."
	@pkill -f "uvicorn main:app" || true
	@pkill -f "vite" || true
	@docker-compose down
	@echo "✅ All services stopped"

test:
	@./test_system.sh

logs:
	@echo "📋 Showing logs..."
	@echo ""
	@echo "=== Database Logs ==="
	@docker-compose logs --tail=50 postgres
	@echo ""
	@echo "=== Backend Logs ==="
	@echo "Check terminal where backend is running"
	@echo ""
	@echo "=== Frontend Logs ==="
	@echo "Check terminal where frontend is running"

db-shell:
	@echo "🗄️  Opening database shell..."
	@docker-compose exec postgres psql -U gameuser -d life_game_db

clean:
	@echo "🧹 Cleaning up..."
	@make stop
	@echo "✅ Cleanup complete"

reset:
	@echo "⚠️  WARNING: This will delete all data!"
	@read -p "Are you sure? (yes/no): " confirm; \
	if [ "$$confirm" = "yes" ]; then \
		docker-compose down -v; \
		rm -rf backend/venv; \
		rm -rf frontend/node_modules; \
		echo "✅ Reset complete. Run 'make setup' to start fresh."; \
	else \
		echo "❌ Reset cancelled"; \
	fi

# Development helpers
dev-backend:
	@echo "🔧 Starting backend in dev mode..."
	@cd backend && source venv/bin/activate && uvicorn main:app --reload

dev-frontend:
	@echo "🎨 Starting frontend in dev mode..."
	@cd frontend && npm run dev

install-backend:
	@echo "📦 Installing backend dependencies..."
	@cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

install-frontend:
	@echo "📦 Installing frontend dependencies..."
	@cd frontend && npm install


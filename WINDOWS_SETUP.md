# Windows Setup Guide - Using Docker (Recommended)

## ⚠️ Important: Python 3.13 Compatibility Issue

If you're on Windows with Python 3.13, many packages don't have pre-built wheels yet and require compilation (Visual Studio Build Tools + Rust).

**Solution: Use Docker instead** - this project is designed to run in Docker anyway!

## Quick Start with Docker

### 1. Ensure Docker Desktop is Running

```bash
# Check Docker is installed
docker --version
docker-compose --version
```

### 2. Update .env File

Edit `.env` and add your credentials:
```bash
OPENAI_API_KEY=sk-proj-YOUR-ACTUAL-KEY
POSTGRES_PASSWORD=your_secure_password
```

### 3. Start Everything with Docker Compose

```bash
# Start all services (PostgreSQL, Kafka, API, Worker)
docker-compose up -d

# Wait for services to be ready (about 30 seconds)
docker-compose ps

# Initialize the database
docker-compose exec postgres psql -U fte_user -d fte_db -f /docker-entrypoint-initdb.d/01-schema.sql
```

### 4. Verify It's Working

```bash
# Check API health
curl http://localhost:8000/health

# View API documentation
start http://localhost:8000/docs

# View logs
docker-compose logs -f api
```

## Development Workflow with Docker

### Making Code Changes

Your code is mounted as a volume, so changes are reflected immediately:

```bash
# Edit files in production/ directory
# API will auto-reload on changes

# View logs to see changes
docker-compose logs -f api
```

### Running Commands Inside Containers

```bash
# Run Python commands
docker-compose exec api python -c "print('Hello')"

# Access Python shell
docker-compose exec api python

# Run tests
docker-compose exec api pytest tests/

# Access database
docker-compose exec postgres psql -U fte_user -d fte_db
```

### Useful Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart a service
docker-compose restart api

# View logs
docker-compose logs -f
docker-compose logs -f api
docker-compose logs -f worker

# Rebuild after dependency changes
docker-compose up -d --build

# Clean everything
docker-compose down -v
```

## Alternative: Local Python Development

If you want to develop without Docker, you need:

### Option A: Use Python 3.11 (Has Pre-built Wheels)

```bash
# Install Python 3.11 from python.org
# Then:
pip install -r requirements.txt
```

### Option B: Install Build Tools (For Python 3.13)

1. Install Visual Studio Build Tools:
   - Download from: https://visualstudio.microsoft.com/downloads/
   - Select "Desktop development with C++"
   - Install

2. Install Rust:
   - Download from: https://rustup.rs/
   - Run installer
   - Restart terminal

3. Then install:
```bash
pip install -r requirements.txt
```

## Recommended Approach

**Use Docker for everything** - it's simpler and matches the production environment:

```bash
# Development workflow
1. Edit code in your IDE
2. docker-compose restart api  # If needed
3. docker-compose logs -f api  # Watch logs
4. Test at http://localhost:8000
```

## Testing Your Setup

```bash
# 1. Start services
docker-compose up -d

# 2. Wait 30 seconds for everything to start

# 3. Test the API
curl http://localhost:8000/health

# 4. Submit a test support request
curl -X POST http://localhost:8000/support/submit \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "subject": "Test Request",
    "category": "general",
    "message": "This is a test message to verify the system works."
  }'

# 5. Check the response - you should get a ticket_id
```

## Troubleshooting

**Services won't start?**
```bash
# Check Docker is running
docker ps

# Check logs
docker-compose logs

# Restart everything
docker-compose down
docker-compose up -d
```

**Port conflicts?**
```bash
# Check what's using port 8000
netstat -ano | findstr :8000

# Stop the process or change port in docker-compose.yml
```

**Database connection issues?**
```bash
# Wait for PostgreSQL to be ready
docker-compose logs postgres

# Manually initialize if needed
docker-compose exec postgres psql -U fte_user -d fte_db -f /docker-entrypoint-initdb.d/01-schema.sql
```

## Summary

✅ **Use Docker** - Simplest and recommended
❌ **Local pip install** - Requires build tools on Windows with Python 3.13

Your project is ready to run with Docker! Just update `.env` and run `docker-compose up -d`.

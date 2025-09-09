#!/bin/bash

echo "🚀 Starting LLM Knowledge Extractor..."

# Run migrations
echo "🔄 Running database migrations..."
alembic upgrade head
echo "✅ Database migrations completed successfully"

# Start the application
echo "🚀 Starting FastAPI application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
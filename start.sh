#!/bin/bash

# ------------------------------------------
# 🚀 Crypto Trading Bot Startup Script
# ------------------------------------------

# Exit if any command fails
set -e

# 1. Print header
echo "=========================================="
echo "🚀 Launching Crypto Trading Bot with Python"
echo "=========================================="

# 2. Load environment variables from .env
if [ -f .env ]; then
  echo "🔧 Loading environment variables from .env..."
  export $(grep -v '^#' .env | xargs)
else
  echo "⚠️  .env file not found. Skipping environment loading."
fi

# 3. Set up Python virtual environment
if [ ! -d "venv" ]; then
  echo "📦 Creating new Python virtual environment..."
  python3 -m venv venv
fi

echo "🐍 Activating virtual environment..."
source venv/bin/activate

# 4. Install Python dependencies
if [ -f "requirements.txt" ]; then
  echo "📚 Installing dependencies from requirements.txt..."
  pip install --upgrade pip
  pip install -r requirements.txt
else
  echo "❌ requirements.txt not found!"
  exit 1
fi

# 5. Run the bot
if [ -f "main.py" ]; then
  echo "🤖 Starting trading bot..."
  python3 main.py
else
  echo "❌ main.py not found. Please check your entry point."
  exit 1
fi

# 6. Done
echo "✅ Bot has stopped (or crashed). Check logs if needed."
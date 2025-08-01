#!/bin/bash

# Title: Start Script for Crypto Trading Bot
# Description: Initializes environment, installs dependencies, and launches the bot.

echo "🚀 Starting Crypto Trading Bot..."

# Fail on any error
set -e

# Load environment variables from .env if exists
if [ -f .env ]; then
  echo "🔧 Loading environment variables..."
  export $(grep -v '^#' .env | xargs)
else
  echo "⚠️  .env file not found. Proceeding without loading environment variables."
fi

# Create virtual environment if not present
if [ ! -d "venv" ]; then
  echo "📦 Creating Python virtual environment..."
  python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run the trading bot
echo "🤖 Launching bot..."
python3 main.py

# End of script

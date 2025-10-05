#!/bin/bash

echo "========================================"
echo "🎮 LLM Rock-Paper-Scissors Dev Setup"  
echo "========================================"
echo

echo "[1/4] 🔍 Checking virtual environment..."
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Creating..."
    python -m venv .venv
    if [ $? -ne 0 ]; then
        echo "❌ Error: Failed to create virtual environment"
        exit 1
    fi
    echo "✅ Virtual environment created"
else
    echo "✅ Existing virtual environment found"
fi

echo
echo "[2/4] 🔧 Activating virtual environment..."
source .venv/Scripts/activate
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to activate virtual environment"
    exit 1
fi
echo "✅ Virtual environment activated"

echo
echo "[3/4] 📦 Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install dependencies"
    exit 1
fi
echo "✅ Dependencies installation completed"

echo
echo "[4/4] 🧪 Running tests..."
python -m unittest discover tests -v
if [ $? -ne 0 ]; then
    echo "⚠️  Warning: Some tests failed"
else
    echo "✅ All tests passed"
fi

echo
echo "========================================"
echo "🎉 Setup completed!"
echo "========================================"
echo
echo "📝 How to start development:"
echo "  1. source .venv/Scripts/activate"
echo "  2. python main.py"
echo
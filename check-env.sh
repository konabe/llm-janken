#!/bin/bash

echo "🔍 Development Environment Check"
echo "================================"

# 1. Virtual environment status check
if [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ Virtual Environment: Active ($VIRTUAL_ENV)"
else
    echo "❌ Virtual Environment: Inactive"
    echo "💡 Please run: source .venv/Scripts/activate"
    exit 1
fi

# 2. Python check
echo -n "🐍 Python: "
python --version
if [ $? -ne 0 ]; then
    echo "❌ Python not found"
    exit 1
fi

# 3. OpenAI package check
python -c "import openai; print('✅ OpenAI: Available')" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ OpenAI: Package available"
else
    echo "❌ OpenAI: Package not found"
    echo "💡 Please run: pip install -r requirements.txt"
fi

# 4. Project files check
files=("src/ai/player.py" "main.py" "requirements.txt")
echo "📁 Important files check..."
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file not found"
    fi
done

echo
echo "🎉 Environment check completed"
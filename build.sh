#!/bin/bash
# Build script for magika-sdk-python
# Cross-platform build automation

set -e

echo "================================================"
echo "Magika SDK Python - Build Script"
echo "================================================"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

echo -e "${GREEN}[1/5]${NC} Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true

echo -e "${GREEN}[2/5]${NC} Installing dependencies..."
pip install --upgrade pip
pip install -e ".[dev]"

echo -e "${GREEN}[3/5]${NC} Running tests..."
pytest tests/ -v --cov=magika_sdk --cov-report=term-missing

echo -e "${GREEN}[4/5]${NC} Building distribution packages..."
python setup.py sdist bdist_wheel

echo -e "${GREEN}[5/5]${NC} Verifying build artifacts..."
if [ -d "dist" ]; then
    echo "Build artifacts:"
    ls -lh dist/
    echo ""
    echo -e "${YELLOW}Build completed successfully!${NC}"
    echo "To upload to PyPI, run: twine upload dist/*"
else
    echo -e "${YELLOW}Warning: dist/ directory not found${NC}"
fi

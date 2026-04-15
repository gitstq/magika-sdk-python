@echo off
REM Build script for magika-sdk-python (Windows)
REM Run this script in PowerShell or Command Prompt

echo ================================================
echo Magika SDK Python - Build Script (Windows)
echo ================================================

cd /d "%~dp0"

echo [1/5] Cleaning previous builds...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.egg-info rmdir /s /q *.egg-info
del /s /q "__pycache__" 2>nul
del /s /q "*.pyc" 2>nul

echo [2/5] Installing dependencies...
pip install --upgrade pip
pip install -e ".[dev]"

echo [3/5] Running tests...
pytest tests/ -v --cov=magika_sdk --cov-report=term-missing

echo [4/5] Building distribution packages...
python setup.py sdist bdist_wheel

echo [5/5] Verifying build artifacts...
if exist dist (
    echo Build artifacts:
    dir dist
    echo.
    echo Build completed successfully!
    echo To upload to PyPI, run: twine upload dist\*
) else (
    echo Warning: dist directory not found
)

pause

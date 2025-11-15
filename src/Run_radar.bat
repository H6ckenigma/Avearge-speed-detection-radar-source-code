@echo off
setlocal enabledelayedexpansion
title Radar Enigma Launcher

echo ============================================
echo    RADAR ENIGMA - Starting...
echo ============================================
echo.

REM Try to find Python
set PYTHON_CMD=

echo Searching for Python...
where python >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto :found
)

where py >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    goto :found
)

REM Check common installation paths
if exist "C:\Python39\python.exe" (
    set PYTHON_CMD=C:\Python39\python.exe
    goto :found
)

if exist "C:\Python310\python.exe" (
    set PYTHON_CMD=C:\Python310\python.exe
    goto :found
)

if exist "C:\Python311\python.exe" (
    set PYTHON_CMD=C:\Python311\python.exe
    goto :found
)

if exist "%LOCALAPPDATA%\Programs\Python\Python39\python.exe" (
    set PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python39\python.exe
    goto :found
)

if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" (
    set PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python310\python.exe
    goto :found
)

if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python311\python.exe
    goto :found
)

REM Python not found anywhere
echo.
echo ========================================
echo   ERROR: Python Not Found!
echo ========================================
echo.
echo Python is not installed or not in PATH.
echo.
echo Please download and install Python from:
echo https://www.python.org/downloads/
echo.
echo IMPORTANT: During installation, check the box:
echo "Add Python to PATH"
echo.
pause
exit /b 1

:found
echo Found: !PYTHON_CMD!
!PYTHON_CMD! --version
echo.

REM Check Python version
for /f "tokens=2" %%i in ('!PYTHON_CMD! --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python version: %PYTHON_VERSION%
echo.

REM Check if requirements are installed
echo Checking requirements...
!PYTHON_CMD! -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing PyQt6...
    !PYTHON_CMD! -m pip install --upgrade pip
    !PYTHON_CMD! -m pip install PyQt6 pandas numpy
    echo.
    echo Installation complete!
    echo.
)

REM Check if gui.py exists
if not exist "gui.py" (
    echo ERROR: gui.py not found in current directory!
    echo Current directory: %CD%
    echo.
    echo Please run this batch file from the src folder.
    pause
    exit /b 1
)

REM Run the application
echo ============================================
echo    Launching Radar Enigma...
echo ============================================
echo.
!PYTHON_CMD! gui.py

REM Check exit code
if errorlevel 1 (
    echo.
    echo ========================================
    echo   Program exited with an error
    echo ========================================
    echo.
    pause
) else (
    echo.
    echo Program closed successfully.
)

endlocal
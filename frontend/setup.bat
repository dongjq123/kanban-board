@echo off
REM Frontend setup script for Windows

echo Setting up Visual Task Board Frontend...

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Node.js is not installed. Please install Node.js 16+ first.
    pause
    exit /b 1
)

echo Node.js version:
node --version
echo npm version:
npm --version

REM Install dependencies
echo Installing dependencies...
npm install

echo Frontend setup complete!
echo To start the development server, run: npm run serve
echo To run tests, run: npm run test:unit
pause

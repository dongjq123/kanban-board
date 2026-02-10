@echo off
REM Backend setup script for Windows

echo Setting up Visual Task Board Backend...

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo Please update .env with your database configuration
)

echo Backend setup complete!
echo To activate the virtual environment, run: venv\Scripts\activate.bat
echo To start the server, run: python app.py
pause

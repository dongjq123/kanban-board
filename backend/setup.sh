#!/bin/bash
# Backend setup script

echo "Setting up Visual Task Board Backend..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please update .env with your database configuration"
fi

echo "Backend setup complete!"
echo "To activate the virtual environment, run: source venv/bin/activate"
echo "To start the server, run: python app.py"

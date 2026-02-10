#!/bin/bash
# Frontend setup script

echo "Setting up Visual Task Board Frontend..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

echo "Node.js version: $(node --version)"
echo "npm version: $(npm --version)"

# Install dependencies
echo "Installing dependencies..."
npm install

echo "Frontend setup complete!"
echo "To start the development server, run: npm run serve"
echo "To run tests, run: npm run test:unit"

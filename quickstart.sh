#!/bin/bash

# Quick start script for AG-UI Agent with MCP
# This script helps you get started quickly with the agent

set -e

echo "=================================="
echo "AG-UI Agent Quick Start"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
echo "✓ Dependencies installed"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  No .env file found"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "=================================="
    echo "IMPORTANT: Configure your .env file"
    echo "=================================="
    echo ""
    echo "Please edit .env and set:"
    echo "  1. AZURE_AI_PROJECT_CONNECTION_STRING"
    echo "  2. Other configuration as needed"
    echo ""
    echo "After configuration, run this script again or:"
    echo "  source venv/bin/activate"
    echo "  python agent.py"
    echo ""
    exit 0
fi

# Check if Azure connection string is set
if ! grep -q "AZURE_AI_PROJECT_CONNECTION_STRING=.*[^=]" .env; then
    echo ""
    echo "⚠️  AZURE_AI_PROJECT_CONNECTION_STRING not configured in .env"
    echo ""
    echo "Please edit .env and set your Azure AI Project connection string"
    echo "Then run this script again or:"
    echo "  source venv/bin/activate"
    echo "  python agent.py"
    echo ""
    exit 0
fi

# Check Azure authentication
echo ""
echo "Checking Azure authentication..."
if az account show &>/dev/null; then
    ACCOUNT=$(az account show --query name -o tsv)
    echo "✓ Logged in to Azure as: $ACCOUNT"
else
    echo "⚠️  Not logged in to Azure"
    echo ""
    read -p "Would you like to login now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        az login
    else
        echo "You can login later with: az login"
    fi
fi

# Ready to start
echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Starting the agent..."
echo "The AG-UI endpoint will be available at: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "----------------------------------"
echo ""

# Run the agent
python agent.py

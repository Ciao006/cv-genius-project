#!/bin/bash

# 🚀 CV Genius Deployment Script
# Automates the deployment process for the complete CV platform

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Node.js
    if ! command_exists node; then
        print_error "Node.js is not installed. Please install Node.js first."
        exit 1
    fi
    
    # Check npm
    if ! command_exists npm; then
        print_error "npm is not installed. Please install npm first."
        exit 1
    fi
    
    # Check Python
    if ! command_exists python3; then
        print_error "Python 3 is not installed. Please install Python 3 first."
        exit 1
    fi
    
    print_success "All basic prerequisites met!"
}

# Setup environment
setup_environment() {
    print_status "Setting up environment..."
    
    # Check if .env exists
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            print_warning ".env file not found. Copying from .env.example..."
            cp .env.example .env
            print_warning "Please edit .env file with your actual values before deploying to production!"
        else
            print_error ".env.example file not found. Please create environment configuration."
            exit 1
        fi
    fi
    
    print_success "Environment setup complete!"
}

# Install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    
    # Install root dependencies
    npm install
    
    # Install backend dependencies
    if [ -d "backend" ]; then
        print_status "Installing backend dependencies..."
        cd backend
        if [ ! -d "venv" ]; then
            python3 -m venv venv
        fi
        source venv/bin/activate
        pip install -r requirements.txt
        cd ..
    fi
    
    # Install frontend dependencies
    if [ -d "frontend" ]; then
        print_status "Installing frontend dependencies..."
        cd frontend
        npm install
        cd ..
    fi
    
    print_success "Dependencies installed!"
}

# Test local deployment
test_local() {
    print_status "Testing local deployment..."
    
    # Test backend
    if [ -d "backend" ]; then
        print_status "Testing backend..."
        cd backend
        source venv/bin/activate
        python -c "
import sys
sys.path.append('.')
try:
    from app.main import app
    print('✅ Backend imports successfully')
except Exception as e:
    print(f'❌ Backend import error: {e}')
    sys.exit(1)
"
        cd ..
    fi
    
    # Test frontend build
    if [ -d "frontend" ]; then
        print_status "Testing frontend build..."
        cd frontend
        npm run build
        cd ..
    fi
    
    print_success "Local tests passed!"
}

# Deploy to cloud
deploy_cloud() {
    print_status "Starting cloud deployment..."
    
    # Check if gcloud is installed for backend deployment
    if command_exists gcloud; then
        print_status "Deploying backend to Google Cloud Run..."
        npm run deploy:backend
        print_success "Backend deployed!"
    else
        print_warning "gcloud CLI not found. Skipping backend deployment."
        print_warning "Install gcloud CLI to deploy backend: https://cloud.google.com/sdk/docs/install"
    fi
    
    # Check if vercel is installed for frontend deployment
    if command_exists vercel; then
        print_status "Deploying frontend to Vercel..."
        npm run deploy:frontend
        print_success "Frontend deployed!"
    else
        print_warning "Vercel CLI not found. Skipping frontend deployment."
        print_warning "Install Vercel CLI: npm install -g vercel"
    fi
}

# Start local development
start_local() {
    print_status "Starting local development servers..."
    npm run dev
}

# Main deployment function
deploy() {
    local deployment_type=$1
    
    echo "🚀 CV Genius Deployment Script"
    echo "================================"
    
    check_prerequisites
    setup_environment
    install_dependencies
    
    case $deployment_type in
        "local")
            test_local
            start_local
            ;;
        "cloud")
            test_local
            deploy_cloud
            ;;
        "test")
            test_local
            print_success "All tests passed! Ready for deployment."
            ;;
        *)
            print_status "Available deployment options:"
            echo "  ./deploy.sh local  - Start local development"
            echo "  ./deploy.sh cloud  - Deploy to cloud (Google Cloud + Vercel)"
            echo "  ./deploy.sh test   - Test the application locally"
            ;;
    esac
}

# Show help if no arguments
if [ $# -eq 0 ]; then
    deploy
else
    deploy $1
fi 
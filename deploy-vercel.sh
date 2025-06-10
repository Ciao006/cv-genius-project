#!/bin/bash

# CV Genius - Vercel Deployment Script
# This script deploys both frontend and backend to Vercel

set -e

echo "🚀 Starting CV Genius Vercel Deployment"
echo "======================================="

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Ensure we're logged in to Vercel
echo "🔐 Checking Vercel authentication..."
vercel whoami || {
    echo "Please login to Vercel:"
    vercel login
}

# Set environment variables
echo "🔧 Setting up environment variables..."
echo "Please ensure you have the following environment variables set in Vercel:"
echo "- GEMINI_API_KEY (for AI functionality)"
echo "- SECRET_KEY (for backend security)"
echo "- DATABASE_URL (if using a database)"
echo ""

# Deploy Backend
echo "🔧 Deploying Backend to Vercel..."
cd backend

echo "Installing backend dependencies..."
pip install -r requirements.txt

echo "Deploying backend..."
vercel --prod --yes

# Get backend URL
BACKEND_URL=$(vercel ls | grep cvgenius-backend | head -1 | awk '{print $2}')
if [ -z "$BACKEND_URL" ]; then
    echo "⚠️  Could not automatically detect backend URL. Please set it manually."
    echo "You can find it in your Vercel dashboard."
    read -p "Enter your backend URL (https://your-backend.vercel.app): " BACKEND_URL
fi

echo "✅ Backend deployed successfully!"
echo "Backend URL: https://$BACKEND_URL"

cd ..

# Deploy Frontend
echo "🎨 Deploying Frontend to Vercel..."
cd frontend

echo "Installing frontend dependencies..."
npm install

echo "Building frontend..."
npm run build

echo "Deploying frontend..."
vercel --prod --yes

# Get frontend URL
FRONTEND_URL=$(vercel ls | grep cvgenius-frontend | head -1 | awk '{print $2}')
if [ -z "$FRONTEND_URL" ]; then
    echo "⚠️  Could not automatically detect frontend URL. Please set it manually."
    read -p "Enter your frontend URL (https://your-frontend.vercel.app): " FRONTEND_URL
fi

echo "✅ Frontend deployed successfully!"
echo "Frontend URL: https://$FRONTEND_URL"

cd ..

# Set environment variables for production
echo "🔧 Setting production environment variables..."

# Set backend URL in frontend
vercel env add NEXT_PUBLIC_API_URL production "https://$BACKEND_URL" --cwd frontend

# Set frontend URL in backend CORS settings
vercel env add ALLOWED_ORIGINS production "https://$FRONTEND_URL,http://localhost:3000" --cwd backend

echo ""
echo "🎉 Deployment Complete!"
echo "======================"
echo "Frontend: https://$FRONTEND_URL"
echo "Backend:  https://$BACKEND_URL"
echo ""
echo "📋 Next Steps:"
echo "1. Add your Gemini API key: vercel env add GEMINI_API_KEY production YOUR_KEY --cwd backend"
echo "2. Add your Gemini API key for frontend: vercel env add NEXT_PUBLIC_GEMINI_API_KEY production YOUR_KEY --cwd frontend"
echo "3. Test your application at https://$FRONTEND_URL"
echo "4. Check API health at https://$BACKEND_URL/health"
echo ""
echo "🔧 Environment Variables to Set:"
echo "Backend:"
echo "- GEMINI_API_KEY: Your Google Gemini API key"
echo "- SECRET_KEY: Random secret for JWT tokens"
echo "- DATABASE_URL: Your database connection string (if needed)"
echo ""
echo "Frontend:"
echo "- NEXT_PUBLIC_GEMINI_API_KEY: Your Google Gemini API key"
echo "- NEXT_PUBLIC_API_URL: Set automatically to backend URL"
echo "- NEXT_PUBLIC_APP_URL: Set automatically to frontend URL"
echo ""
echo "Use 'vercel env add KEY_NAME production VALUE --cwd DIRECTORY' to set them." 
#!/bin/bash

# CV Genius - Update Vercel Deployment Script
# Use this script to update your existing Vercel deployments

set -e

echo "🔄 Updating CV Genius Vercel Deployment"
echo "======================================="

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Please install it first:"
    echo "npm install -g vercel"
    exit 1
fi

echo "🔧 Updating Backend..."
cd backend
vercel --prod
echo "✅ Backend updated successfully!"

cd ..

echo "🎨 Updating Frontend..."
cd frontend
vercel --prod
echo "✅ Frontend updated successfully!"

cd ..

echo ""
echo "🎉 Update Complete!"
echo "==================="
echo "Your CV Genius application has been updated!"
echo ""
echo "Check your deployment status:"
echo "- Vercel Dashboard: https://vercel.com/dashboard"
echo "- Backend Health: Check your backend URL + /health"
echo "- Frontend: Check your frontend URL"
echo ""
echo "If you made changes to environment variables, make sure to set them:"
echo "vercel env add KEY_NAME production VALUE --cwd [backend|frontend]" 
# 🚀 CV Genius Vercel Deployment Guide

This guide will help you deploy both the frontend and backend of CV Genius to Vercel.

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI**: Install globally with `npm install -g vercel`
3. **Google Gemini API Key**: Get one from [Google AI Studio](https://makersuite.google.com/app/apikey)
4. **Git Repository**: Your code should be in a Git repository

## 🚀 Quick Deployment

### Option 1: Automated Script

Run the automated deployment script:

```bash
./deploy-vercel.sh
```

This script will:
- Install Vercel CLI if needed
- Deploy both backend and frontend
- Configure environment variables
- Provide you with deployment URLs

### Option 2: Manual Deployment

#### Step 1: Deploy Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Login to Vercel (if not already logged in):
```bash
vercel login
```

3. Deploy the backend:
```bash
vercel --prod
```

4. Note the deployed URL (e.g., `https://cvgenius-backend-xyz.vercel.app`)

#### Step 2: Deploy Frontend

1. Navigate to the frontend directory:
```bash
cd ../frontend
```

2. Deploy the frontend:
```bash
vercel --prod
```

3. Note the deployed URL (e.g., `https://cvgenius-frontend-abc.vercel.app`)

## 🔧 Environment Variables

### Backend Environment Variables

Set these in your Vercel backend project:

```bash
# Required
vercel env add GEMINI_API_KEY production "your_gemini_api_key_here" --cwd backend
vercel env add SECRET_KEY production "your_secret_key_here" --cwd backend

# Optional
vercel env add DATABASE_URL production "your_database_url" --cwd backend
vercel env add ALLOWED_ORIGINS production "https://your-frontend-url.vercel.app,http://localhost:3000" --cwd backend
vercel env add DEBUG production "false" --cwd backend
```

### Frontend Environment Variables

Set these in your Vercel frontend project:

```bash
# Required
vercel env add NEXT_PUBLIC_GEMINI_API_KEY production "your_gemini_api_key_here" --cwd frontend
vercel env add NEXT_PUBLIC_API_URL production "https://your-backend-url.vercel.app" --cwd frontend

# Optional
vercel env add NEXT_PUBLIC_APP_URL production "https://your-frontend-url.vercel.app" --cwd frontend
```

## 📝 Configuration Files

### Backend Configuration (`backend/vercel.json`)

```json
{
  "name": "cvgenius-backend",
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ],
  "env": {
    "GEMINI_API_KEY": "@gemini-api-key",
    "SECRET_KEY": "@secret-key",
    "DATABASE_URL": "@database-url",
    "ALLOWED_ORIGINS": "@allowed-origins",
    "DEBUG": "false"
  },
  "regions": ["iad1"],
  "functions": {
    "main.py": {
      "maxDuration": 60
    }
  }
}
```

### Frontend Configuration (`frontend/vercel.json`)

```json
{
  "name": "cvgenius-frontend",
  "version": 2,
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "installCommand": "npm install",
  "devCommand": "npm run dev",
  "env": {
    "NEXT_PUBLIC_API_URL": "@cvgenius-api-url",
    "NEXT_PUBLIC_GEMINI_API_KEY": "@gemini-api-key",
    "NEXT_PUBLIC_APP_URL": "@app-url"
  },
  "regions": ["iad1"],
  "functions": {
    "app/**": {
      "maxDuration": 30
    }
  }
}
```

## 🔗 Linking Frontend and Backend

After deploying both applications:

1. **Update Frontend API URL**: Set the backend URL in your frontend environment:
```bash
vercel env add NEXT_PUBLIC_API_URL production "https://your-backend-url.vercel.app" --cwd frontend
```

2. **Update Backend CORS**: Allow your frontend domain in the backend:
```bash
vercel env add ALLOWED_ORIGINS production "https://your-frontend-url.vercel.app" --cwd backend
```

3. **Redeploy both applications** to apply the changes:
```bash
vercel --prod --cwd backend
vercel --prod --cwd frontend
```

## 🧪 Testing Your Deployment

### 1. Test Backend Health

Visit your backend URL and check the health endpoint:
```
https://your-backend-url.vercel.app/health
```

You should see:
```json
{
  "status": "healthy",
  "service": "cvgenius-api",
  "version": "2.0.0",
  "endpoints": {
    "basic": "/api/v1",
    "advanced": "/api/v1/advanced"
  }
}
```

### 2. Test Frontend

Visit your frontend URL:
```
https://your-frontend-url.vercel.app
```

### 3. Test AI Integration

Try using the AI features in the application to ensure the Gemini API is working correctly.

## 🛠️ Troubleshooting

### Common Issues

1. **Build Failures**
   - Check that all dependencies are listed in `requirements.txt` (backend) or `package.json` (frontend)
   - Ensure Python version compatibility (Vercel supports Python 3.9+)

2. **Environment Variable Issues**
   - Double-check that all required environment variables are set
   - Use `vercel env ls` to list current environment variables
   - Redeploy after adding new environment variables

3. **CORS Issues**
   - Ensure `ALLOWED_ORIGINS` includes your frontend URL
   - Check that the frontend is using the correct backend URL

4. **API Timeouts**
   - Vercel serverless functions have a timeout limit
   - Consider optimizing long-running operations
   - Check function duration in Vercel dashboard

### Debug Commands

```bash
# List all deployments
vercel ls

# View deployment logs
vercel logs [deployment-url]

# List environment variables
vercel env ls

# Remove deployment
vercel rm [deployment-url]
```

## 📊 Monitoring and Analytics

### Vercel Analytics

Enable analytics in your Vercel dashboard for:
- Performance monitoring
- Error tracking
- Usage statistics

### Application Monitoring

Your application includes:
- Health check endpoints
- Error logging
- Performance metrics

## 🔄 Continuous Deployment

### Git Integration

Connect your GitHub repository to Vercel for automatic deployments:

1. Go to your Vercel dashboard
2. Import your Git repository
3. Configure build settings
4. Set environment variables
5. Enable automatic deployments

### Manual Updates

To update your deployment:

```bash
# Update backend
cd backend
vercel --prod

# Update frontend
cd ../frontend
vercel --prod
```

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Python on Vercel](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python)

## 🆘 Support

If you encounter issues:

1. Check the Vercel dashboard for deployment logs
2. Review environment variables
3. Test locally first with `vercel dev`
4. Check the health endpoints
5. Review CORS configuration

Your CV Genius application should now be successfully deployed on Vercel! 🎉 
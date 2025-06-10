# 🚀 Quick Deploy to Vercel

## Prerequisites
- Vercel account and CLI: `npm install -g vercel`
- Google Gemini API key

## One-Command Deployment

```bash
./deploy-vercel.sh
```

## Manual Steps

### 1. Deploy Backend
```bash
cd backend
vercel --prod
```

### 2. Deploy Frontend
```bash
cd frontend
vercel --prod
```

### 3. Set Environment Variables

**Backend:**
```bash
vercel env add GEMINI_API_KEY production "YOUR_KEY" --cwd backend
vercel env add SECRET_KEY production "random_secret_123" --cwd backend
```

**Frontend:**
```bash
vercel env add NEXT_PUBLIC_GEMINI_API_KEY production "YOUR_KEY" --cwd frontend
vercel env add NEXT_PUBLIC_API_URL production "https://your-backend.vercel.app" --cwd frontend
```

### 4. Link Apps
```bash
# Update frontend to use backend URL
vercel env add NEXT_PUBLIC_API_URL production "https://cvgenius-backend-xyz.vercel.app" --cwd frontend

# Update backend CORS for frontend
vercel env add ALLOWED_ORIGINS production "https://cvgenius-frontend-abc.vercel.app" --cwd backend

# Redeploy both
vercel --prod --cwd backend
vercel --prod --cwd frontend
```

## Test Your Deployment

- Frontend: `https://your-frontend.vercel.app`
- Backend Health: `https://your-backend.vercel.app/health`

## Get Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy and use in environment variables

Done! 🎉 
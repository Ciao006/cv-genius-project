# 🚀 CV Genius Deployment Guide

## Quick Deploy Options

### Option 1: One-Command Deploy (Recommended)
```bash
# Deploy both frontend and backend
npm run deploy:full
```

### Option 2: Deploy Separately
```bash
# Deploy backend to Google Cloud Run
npm run deploy:backend

# Deploy frontend to Vercel
npm run deploy:frontend
```

### Option 3: Local Development
```bash
# Start both services locally
npm run dev
```

## 📋 Prerequisites

### For Cloud Deployment
1. **Google Cloud SDK** (for backend)
   ```bash
   # Install gcloud CLI
   curl https://sdk.cloud.google.com | bash
   source ~/.bashrc
   gcloud init
   ```

2. **Vercel CLI** (for frontend)
   ```bash
   npm install -g vercel
   vercel login
   ```

3. **Required Environment Variables**
   - Copy `.env.example` to `.env` and fill in your values
   - Set up Google Cloud AI Platform credentials
   - Configure any API keys needed

## 🌐 Deployment Methods

### A. Production Deployment (Cloud)

#### 1. Backend to Google Cloud Run
```bash
# Authenticate with Google Cloud
gcloud auth login

# Set your project ID
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable aiplatform.googleapis.com

# Deploy backend
cd backend
gcloud run deploy cvgenius-backend \
  --source . \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --concurrency 80 \
  --min-instances 0 \
  --max-instances 10
```

#### 2. Frontend to Vercel
```bash
# From project root
cd frontend

# Deploy to Vercel
vercel --prod

# Or use the npm script
npm run deploy:frontend
```

### B. Alternative: Docker Compose (Self-Hosted)

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - PORT=8000
      - ENVIRONMENT=production
    env_file:
      - .env
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      - backend

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - frontend
      - backend
```

Deploy with:
```bash
docker-compose up -d
```

### C. Manual Server Setup (VPS/Dedicated Server)

#### 1. Setup Backend
```bash
# Clone and setup
git clone <your-repo>
cd cvgenius/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

#### 2. Setup Frontend
```bash
cd ../frontend

# Install dependencies
npm install

# Build production version
npm run build

# Start production server
npm start
```

## 🔧 Configuration

### Environment Variables

Create `.env` file in the root:
```env
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json

# Database (if using)
DATABASE_URL=postgresql://user:password@localhost/cvgenius

# API Keys
OPENAI_API_KEY=your-openai-key
LINKEDIN_API_KEY=your-linkedin-key

# Security
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret

# External Services
SENDGRID_API_KEY=your-sendgrid-key
STRIPE_SECRET_KEY=your-stripe-key
```

### Frontend Environment (frontend/.env.local)
```env
NEXT_PUBLIC_API_URL=https://your-backend-url.com
NEXT_PUBLIC_GOOGLE_ANALYTICS_ID=GA_MEASUREMENT_ID
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...
```

## 🚨 Production Checklist

### Backend
- [ ] Set `DEBUG=False` in production
- [ ] Configure proper CORS origins
- [ ] Set up database with connection pooling
- [ ] Configure logging and monitoring
- [ ] Set up health checks
- [ ] Enable HTTPS/SSL
- [ ] Configure rate limiting
- [ ] Set up backup strategy

### Frontend
- [ ] Build optimized production bundle
- [ ] Configure CDN for static assets
- [ ] Set up proper caching headers
- [ ] Enable compression (gzip/brotli)
- [ ] Configure analytics
- [ ] Set up error monitoring (Sentry)
- [ ] Test mobile responsiveness
- [ ] Verify SEO optimization

## 📊 Monitoring & Maintenance

### Health Checks
- Backend: `https://your-backend-url.com/health`
- Frontend: Check if app loads properly

### Logs
- Google Cloud Run: `gcloud logs read --service cvgenius-backend`
- Vercel: Check dashboard at vercel.com

### Updates
```bash
# Update backend
cd backend
git pull
gcloud run deploy cvgenius-backend --source .

# Update frontend
cd frontend
git pull
vercel --prod
```

## 🔒 Security Considerations

1. **API Security**
   - Use HTTPS everywhere
   - Implement proper authentication
   - Set up CORS correctly
   - Use environment variables for secrets

2. **Frontend Security**
   - Sanitize user inputs
   - Implement CSP headers
   - Use secure cookies
   - Regular dependency updates

## 💰 Cost Estimation

### Google Cloud Run (Backend)
- ~$0-10/month for low traffic
- Scales automatically
- Pay-per-use model

### Vercel (Frontend)
- Free tier: 100GB bandwidth
- Pro: $20/month for unlimited
- Built-in CDN and analytics

### Total Monthly Cost
- Development: **Free**
- Small business: **$0-30/month**
- Enterprise: **$50-200/month**

## 🆘 Troubleshooting

### Common Issues

1. **Backend deployment fails**
   ```bash
   # Check logs
   gcloud logs read --service cvgenius-backend --limit 50
   
   # Check service status
   gcloud run services describe cvgenius-backend --region europe-west1
   ```

2. **Frontend build fails**
   ```bash
   # Clear cache and rebuild
   cd frontend
   rm -rf .next node_modules
   npm install
   npm run build
   ```

3. **Environment variables not loading**
   - Check `.env` file exists
   - Verify variable names match exactly
   - Restart services after changes

### Getting Help
- Check logs first
- Verify all environment variables
- Test locally before deploying
- Check service status dashboards

---

🎉 **Your CV Genius platform is ready for deployment!** 

Choose your preferred method and follow the steps above. For quick deployment, just run `npm run deploy:full` after setting up your cloud accounts. 
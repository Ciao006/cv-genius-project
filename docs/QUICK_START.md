# 🚀 Quick Start - Deploy CV Genius in 5 Minutes

## 🎯 Super Quick Deploy (One Command)

```bash
# Make script executable and deploy
chmod +x deploy.sh && ./deploy.sh cloud
```

## 📝 Step-by-Step Quick Deploy

### 1. Local Testing (30 seconds)
```bash
./deploy.sh test
```

### 2. Start Local Development (instant)
```bash
./deploy.sh local
# or
npm run dev
```
Visit: `http://localhost:3000`

### 3. Deploy to Cloud (2 minutes)

#### Prerequisites (one-time setup):
```bash
# Install Google Cloud CLI
curl https://sdk.cloud.google.com | bash

# Install Vercel CLI
npm install -g vercel

# Login to services
gcloud auth login
vercel login
```

#### Deploy:
```bash
./deploy.sh cloud
# or
npm run deploy:full
```

## 🔧 Environment Setup

1. **Copy environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your values:**
   ```env
   GOOGLE_CLOUD_PROJECT=your-project-id
   OPENAI_API_KEY=your-openai-key
   # ... other keys
   ```

## ✅ That's It!

Your CV Genius platform is now:
- ✅ Running locally at `http://localhost:3000`
- ✅ Deployed to cloud (if you ran cloud deploy)
- ✅ Ready for users

## 🎉 What You Get

A complete CV platform with:
- ✅ AI-powered CV generation
- ✅ 20+ professional templates
- ✅ ATS compatibility checker
- ✅ Real-time collaboration
- ✅ Multi-format export (PDF, DOCX, etc.)
- ✅ Performance analytics
- ✅ Mobile-responsive design
- ✅ LinkedIn import
- ✅ Industry-specific optimization

## 🔗 URLs After Deployment

- **Local Frontend:** http://localhost:3000
- **Local Backend:** http://localhost:8000
- **Production:** Your Vercel deployment URL
- **API Docs:** http://localhost:8000/docs (local)

## 🆘 Need Help?

- **Local issues:** Check `./deploy.sh test`
- **Cloud issues:** Check logs in Google Cloud Console / Vercel Dashboard
- **Environment issues:** Verify `.env` file
- **Dependencies:** Run `npm install` and `pip install -r backend/requirements.txt`

---

**🎊 Congratulations! Your enterprise-grade CV platform is live!** 
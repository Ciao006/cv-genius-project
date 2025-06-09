# CVGenius Deployment Guide

This guide covers the complete deployment process for CVGenius to production environments.

## Prerequisites

- Google Cloud account with billing enabled
- Vercel account (for frontend)
- GitHub repository
- Domain name (optional but recommended)

## Environment Setup

### 1. Google Cloud Setup

1. **Create a new Google Cloud project:**
   ```bash
   gcloud projects create cvgenius-prod --name="CVGenius Production"
   gcloud config set project cvgenius-prod
   ```

2. **Enable required APIs:**
   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable artifactregistry.googleapis.com
   gcloud services enable aiplatform.googleapis.com
   gcloud services enable secretmanager.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   ```

3. **Create Artifact Registry repository:**
   ```bash
   gcloud artifacts repositories create cvgenius \
     --repository-format=docker \
     --location=us-central1 \
     --description="CVGenius container images"
   ```

4. **Create service account:**
   ```bash
   gcloud iam service-accounts create cvgenius-service \
     --description="CVGenius service account" \
     --display-name="CVGenius Service"
   
   # Grant necessary roles
   gcloud projects add-iam-policy-binding cvgenius-prod \
     --member="serviceAccount:cvgenius-service@cvgenius-prod.iam.gserviceaccount.com" \
     --role="roles/aiplatform.user"
   
   gcloud projects add-iam-policy-binding cvgenius-prod \
     --member="serviceAccount:cvgenius-service@cvgenius-prod.iam.gserviceaccount.com" \
     --role="roles/secretmanager.secretAccessor"
   ```

5. **Get Gemini API key and store in Secret Manager:**
   ```bash
   # Store the API key
   echo "your-gemini-api-key" | gcloud secrets create GEMINI_API_KEY --data-file=-
   
   # Grant access to service account
   gcloud secrets add-iam-policy-binding GEMINI_API_KEY \
     --member="serviceAccount:cvgenius-service@cvgenius-prod.iam.gserviceaccount.com" \
     --role="roles/secretmanager.secretAccessor"
   ```

### 2. GitHub Secrets Setup

Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):

```
GOOGLE_CLOUD_PROJECT=cvgenius-prod
GOOGLE_APPLICATION_CREDENTIALS=[service account JSON key]
GEMINI_API_KEY=[your gemini api key]
NEXT_PUBLIC_API_URL=https://your-backend-url.run.app
NEXT_PUBLIC_GA_ID=[google analytics id]
NEXT_PUBLIC_ADSENSE_ID=[google adsense id]
```

To get the service account JSON:
```bash
gcloud iam service-accounts keys create key.json \
  --iam-account=cvgenius-service@cvgenius-prod.iam.gserviceaccount.com
```

## Deployment Process

### 1. Backend Deployment (Google Cloud Run)

The GitHub Actions workflow will automatically:
1. Run tests
2. Build Docker image
3. Push to Artifact Registry
4. Deploy to Cloud Run

Manual deployment (if needed):
```bash
cd backend

# Build and tag image
docker build -t us-central1-docker.pkg.dev/cvgenius-prod/cvgenius/backend:latest .

# Configure Docker for Artifact Registry
gcloud auth configure-docker us-central1-docker.pkg.dev

# Push image
docker push us-central1-docker.pkg.dev/cvgenius-prod/cvgenius/backend:latest

# Deploy to Cloud Run
gcloud run deploy cvgenius-backend \
  --image=us-central1-docker.pkg.dev/cvgenius-prod/cvgenius/backend:latest \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated \
  --service-account=cvgenius-service@cvgenius-prod.iam.gserviceaccount.com \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=cvgenius-prod" \
  --set-secrets="GEMINI_API_KEY=GEMINI_API_KEY:latest" \
  --memory=2Gi \
  --cpu=2 \
  --timeout=3600 \
  --max-instances=10 \
  --min-instances=0
```

### 2. Frontend Deployment (Vercel)

1. **Connect GitHub repository to Vercel:**
   - Go to vercel.com and create new project
   - Import your GitHub repository
   - Select the `frontend` directory as root

2. **Configure environment variables in Vercel:**
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.run.app
   NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
   NEXT_PUBLIC_ADSENSE_ID=ca-pub-XXXXXXXXXXXXXXXX
   ```

3. **Deploy settings:**
   - Framework: Next.js
   - Root Directory: frontend
   - Build Command: `npm run build`
   - Output Directory: `.next`

## Domain Configuration

### Custom Domain Setup

1. **Add domain to Vercel:**
   - Go to project settings → Domains
   - Add your domain (e.g., cvgenius.com)
   - Follow DNS configuration instructions

2. **Update CORS settings:**
   Update `backend/app/core/config.py` ALLOWED_ORIGINS to include your domain:
   ```python
   ALLOWED_ORIGINS: List[str] = [
       "http://localhost:3000",
       "https://cvgenius.vercel.app",
       "https://www.cvgenius.com",  # Your domain
       "https://cvgenius.com"       # Your domain
   ]
   ```

## Monitoring and Logging

### 1. Google Cloud Monitoring

Set up monitoring dashboards for:
- Cloud Run instances
- API response times
- Error rates
- Resource usage

### 2. Log Analysis

View logs:
```bash
# Cloud Run logs
gcloud logs read "resource.type=cloud_run_revision" --limit=50

# Filter by severity
gcloud logs read "resource.type=cloud_run_revision AND severity>=ERROR" --limit=50
```

### 3. Alerts

Set up alerting policies for:
- High error rates (>5%)
- High latency (>2s p95)
- Resource exhaustion
- Budget alerts

## Security Configuration

### 1. IAM Best Practices

- Use principle of least privilege
- Regular audit of service account permissions
- Enable audit logging

### 2. Network Security

- Use VPC if needed for high-security environments
- Configure firewall rules
- Enable DDoS protection

### 3. Data Security

- Ensure no PII is logged
- Regular security audits
- Implement rate limiting

## Scaling Configuration

### 1. Cloud Run Scaling

```bash
gcloud run services update cvgenius-backend \
  --region=us-central1 \
  --min-instances=1 \
  --max-instances=100 \
  --concurrency=80
```

### 2. Load Testing

Use tools like Artillery or Apache Bench:
```bash
# Install Artillery
npm install -g artillery

# Run load test
artillery quick --count 10 --num 5 https://your-api-url.run.app/health
```

## Cost Optimization

### 1. Cloud Run Optimization

- Set appropriate CPU and memory limits
- Use minimum instances = 0 for cost savings
- Monitor and adjust based on usage

### 2. Monitoring Costs

Set up billing alerts:
```bash
gcloud billing budgets create \
  --billing-account=BILLING_ACCOUNT_ID \
  --display-name="CVGenius Budget" \
  --budget-amount=50 \
  --threshold-rule=percent-of-budget=90
```

## Backup and Recovery

### 1. Configuration Backup

- Store all configuration in version control
- Backup environment variables securely
- Document all manual configurations

### 2. Disaster Recovery Plan

1. Re-deploy from GitHub Actions
2. Restore environment variables
3. Update DNS if needed
4. Verify all services

## Maintenance

### 1. Regular Updates

- Update dependencies monthly
- Monitor security advisories
- Update base Docker images

### 2. Performance Monitoring

- Monitor API response times
- Check resource utilization
- Optimize based on usage patterns

## Troubleshooting

### Common Issues

1. **Container fails to start:**
   - Check logs: `gcloud logs read "resource.type=cloud_run_revision"`
   - Verify environment variables
   - Check service account permissions

2. **High latency:**
   - Check cold start times
   - Consider increasing min-instances
   - Optimize application code

3. **CORS errors:**
   - Verify ALLOWED_ORIGINS configuration
   - Check frontend URL configuration

### Health Checks

```bash
# Backend health
curl https://your-backend-url.run.app/health

# Frontend health  
curl https://your-frontend-url.vercel.app/
```

## Support

For deployment issues:
1. Check GitHub Actions logs
2. Review Cloud Run logs
3. Verify environment variables
4. Contact support if needed

---

This deployment guide ensures a production-ready setup with proper security, monitoring, and scalability configurations.
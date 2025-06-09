# 🎯 CVGenius - AI-Powered CV Generator for Dublin Job Market

**Professional CV and Cover Letter Generator optimized for Irish employment standards**

[![Live Demo](https://img.shields.io/badge/Live-Demo-green?style=for-the-badge)](https://cvgenius-nine.vercel.app)
[![Backend API](https://img.shields.io/badge/API-Documentation-blue?style=for-the-badge)](https://cvgenius-backend-2fm63lpf4q-ew.a.run.app/docs)

## 🌟 Features

### ✨ **Intelligent CV Creation**
- **AI-Powered Generation**: Uses Google Gemini AI trained on Dublin CV standards
- **ATS Optimization**: Formatted for Applicant Tracking Systems used by Irish employers
- **Dual Workflows**: Create from scratch or update existing CVs
- **Professional Templates**: Clean, Dublin-compliant formatting

### 🇮🇪 **Dublin/Irish Market Optimized**
- **Irish CV Standards**: 1-2 page limit, no photos, professional formatting
- **Local Requirements**: Irish phone formats (+353), Dublin address optimization
- **Business Culture**: Professional tone matching Irish workplace expectations
- **Compliance**: Follows Irish employment and GDPR regulations

### 📄 **Document Generation**
- **PDF Generation**: High-quality, print-ready CV and cover letters
- **Cover Letter AI**: Automatically generates tailored cover letters
- **File Support**: Upload existing CVs (PDF/DOCX) for enhancement
- **Template System**: Professional, ATS-friendly design

### 🔧 **Technical Excellence**
- **Modern Stack**: Next.js frontend, FastAPI backend
- **Cloud Native**: Deployed on Vercel and Google Cloud Run
- **Type Safety**: Full TypeScript implementation
- **Performance**: Optimized for speed and reliability

## 🚀 Live Application

**🌐 Application**: [https://cvgenius-nine.vercel.app](https://cvgenius-nine.vercel.app)
**🔧 API Docs**: [Backend Documentation](https://cvgenius-backend-2fm63lpf4q-ew.a.run.app/docs)

## 🛠️ Technology Stack

### Frontend
- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS for responsive design
- **Forms**: React Hook Form with validation
- **Icons**: Lucide React icon library
- **Deployment**: Vercel Edge Network

### Backend
- **Framework**: FastAPI (Python) with async support
- **AI Integration**: Google Gemini API for content generation
- **PDF Generation**: WeasyPrint for high-quality documents
- **File Processing**: Support for PDF and DOCX uploads
- **Deployment**: Google Cloud Run

### Infrastructure
- **Frontend Hosting**: Vercel (Global CDN)
- **Backend Hosting**: Google Cloud Run (Europe West)
- **Security**: HTTPS, CORS, rate limiting
- **Monitoring**: Cloud logging and health checks

## 🔧 Local Development

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- Google Gemini API key

### Environment Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/cvgenius.git
cd cvgenius
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
```

3. **Frontend Setup**
```bash
cd frontend
npm install

# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

### Running Locally

1. **Start Backend**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. **Start Frontend**
```bash
cd frontend
npm run dev
```

3. **Access Application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 🚀 Deployment

### Quick Deploy

```bash
# Deploy everything (requires setup)
npm run deploy:full

# Deploy frontend only
npm run deploy:frontend

# Deploy backend only
npm run deploy:backend
```

### Environment Variables

#### Backend (.env)
```
GEMINI_API_KEY=your_gemini_api_key
PORT=8000
```

#### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=your_backend_url
NEXT_PUBLIC_GA_ID=your_google_analytics_id (optional)
NEXT_PUBLIC_ADSENSE_ID=your_adsense_id (optional)
```

## 📋 API Documentation

### Core Endpoints

#### Generate CV from Form
```http
POST /api/v1/generate-from-form
Content-Type: application/json

{
  "personal_details": { ... },
  "work_experience": [ ... ],
  "education": [ ... ],
  "skills": "...",
  "job_description": "..."
}
```

#### Update Existing CV
```http
POST /api/v1/generate-from-upload
Content-Type: multipart/form-data

cv_file: [PDF/DOCX file]
job_description: "target job description"
```

Full API documentation available at `/docs` endpoint.

## 🔒 Security & Privacy

### Data Protection
- **No Data Storage**: CVs are processed in real-time, not stored
- **HTTPS Only**: All communications encrypted
- **Rate Limiting**: Protection against abuse
- **Input Validation**: Comprehensive security checks

### Privacy Compliance
- **GDPR Compliant**: EU privacy regulation adherence
- **No Tracking**: Optional analytics, user choice
- **Transparent**: Clear privacy policy and terms

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Code Standards
- **TypeScript**: Strict type checking enabled
- **ESLint**: Code quality enforcement
- **Prettier**: Code formatting
- **Comments**: English language, descriptive

## 🐛 Troubleshooting

### Common Issues

**Build Errors**
- Ensure all environment variables are set
- Check Node.js and Python versions
- Verify API key configuration

**PDF Generation Issues**
- Install system dependencies for WeasyPrint
- Check font availability on deployment platform
- Verify template syntax

**API Connection**
- Confirm backend URL in environment variables
- Check CORS configuration
- Verify API key validity

## 📞 Support

### Getting Help
- **Issues**: [GitHub Issues](https://github.com/yourusername/cvgenius/issues)
- **Documentation**: [API Docs](https://cvgenius-backend-2fm63lpf4q-ew.a.run.app/docs)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI**: Powering intelligent content generation
- **Irish Job Market Research**: Based on official Dublin CV standards
- **Open Source Community**: Built with amazing open-source tools

---

**CVGenius** - Transforming job applications with AI-powered CV generation optimized for the Dublin job market.

[![Made with ❤️ for Dublin Job Seekers](https://img.shields.io/badge/Made%20with%20❤️%20for-Dublin%20Job%20Seekers-green)](#)
# 🎯 CVGenius - AI-Powered CV Generator for Dublin Job Market

**Professional CV and Cover Letter Generator optimized for Irish employment standards**

[![Live Demo](https://img.shields.io/badge/Live-Demo-green?style=for-the-badge)](https://cvgenius-nine.vercel.app)
[![Backend API](https://img.shields.io/badge/API-Documentation-blue?style=for-the-badge)](https://cvgenius-backend-2fm63lpf4q-ew.a.run.app/docs)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 Features

### ✨ **AI-Powered Content Generation**
- **Google Gemini AI Integration**: Advanced content optimization and enhancement
- **ATS Optimization**: Formatted for Applicant Tracking Systems used by Irish employers
- **Grammar & Clarity Analysis**: Intelligent content improvement suggestions
- **Industry Keywords**: 500+ keywords across multiple industries
- **Impact-Focused Writing**: Transform descriptions into achievement statements

### 🇮🇪 **Dublin/Irish Market Optimized**
- **Irish CV Standards**: 1-2 page limit, no photos, professional formatting
- **Local Requirements**: Irish phone formats (+353), Dublin address optimization
- **Business Culture**: Professional tone matching Irish workplace expectations
- **Compliance**: Follows Irish employment and GDPR regulations

### 📄 **Comprehensive Document Generation**
- **PDF Generation**: High-quality, print-ready CV and cover letters
- **Cover Letter AI**: Automatically generates tailored cover letters
- **Multiple Templates**: Professional, Executive, Creative, Academic designs
- **File Support**: Upload existing CVs (PDF/DOCX) for enhancement
- **Multi-Format Export**: PDF, DOCX, TXT, HTML formats

### 📱 **Mobile-First Experience**
- **Step-by-Step Mobile Editor**: Touch-optimized editing experience
- **Responsive Preview**: Mobile-friendly CV preview and real-time updates
- **Auto-Save Functionality**: Never lose your work
- **Offline Capability**: Work without internet connection

### 📊 **Advanced Analytics & Optimization**
- **ATS Scoring System**: Comprehensive 0-100 compatibility scoring
- **Performance Tracking**: Monitor application success rates
- **Job Description Matching**: Optimize for specific job postings
- **Industry Benchmarking**: Compare against market standards

### 🚀 **Dual Creation Workflows**
1. **From Scratch**: Guided step-by-step CV creation with AI assistance
2. **Update Existing**: Upload and enhance existing CVs with AI optimization

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

### Advanced Features
- `POST /api/v1/advanced/optimize/content` - AI content optimization
- `POST /api/v1/advanced/ats/analyze` - ATS compatibility analysis
- `POST /api/v1/advanced/export/multi-format` - Multi-format export

Full API documentation available at `/docs` endpoint.

## 🎯 Use Cases

### For Job Seekers
- Create professional CVs with AI assistance
- Optimize for ATS systems and specific job postings
- Generate tailored cover letters automatically
- Track application success and improve over time

### For Career Coaches
- Help clients with guided CV creation
- Provide structured feedback and improvements
- Use analytics to track client success rates
- Leverage AI-powered content suggestions

### For HR Professionals
- Understand ATS optimization requirements
- Benchmark CV quality standards
- Process and analyze CV formats efficiently

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

## 🎯 Roadmap

### Version 2.1 (Coming Soon)
- [ ] Advanced collaboration features
- [ ] LinkedIn auto-apply integration
- [ ] Enhanced AI coaching
- [ ] Custom branding options

### Version 2.2 (Future)
- [ ] Multi-language support
- [ ] Voice-to-text CV creation
- [ ] Interview preparation tools
- [ ] Salary negotiation insights

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI**: Powering intelligent content generation
- **Irish Job Market Research**: Based on official Dublin CV standards
- **Open Source Community**: Built with amazing open-source tools

---

**CVGenius** - Transforming job applications with AI-powered CV generation optimized for the Dublin job market.

[![Made with ❤️ for Dublin Job Seekers](https://img.shields.io/badge/Made%20with%20❤️%20for-Dublin%20Job%20Seekers-green)](#)
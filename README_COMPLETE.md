# CV Genius - Complete Open Source CV Platform 🚀

**Free & Open Source Alternative to Premium CV Platforms like Enhancv**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-blue.svg)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14.0-black.svg)](https://nextjs.org)
[![Python](https://img.shields.io/badge/Python-3.9+-green.svg)](https://python.org)

## 🎯 Overview

CV Genius is a comprehensive, production-ready CV creation platform that rivals premium services like Enhancv, Zety, and Resume.io - but completely **free and open source**. Built with modern technologies and AI-powered features for professional CV creation, optimization, and collaboration.

## ✨ Features

### 🤖 AI-Powered Content Optimization
- **Grammar & Clarity Analysis** - Intelligent content improvement suggestions
- **Action Verb Enhancement** - Replace weak phrases with impactful action verbs  
- **Quantification Suggestions** - Add metrics and numbers to achievements
- **Industry Keyword Optimization** - 500+ keywords across multiple industries
- **Impact-Focused Writing** - Transform task descriptions into achievement statements

### 📊 ATS Compatibility System
- **Comprehensive ATS Scoring** (0-100) with detailed breakdown
- **Keyword Density Analysis** - Industry-specific keyword matching
- **Format Validation** - Ensure ATS-friendly structure and formatting
- **Parsing Simulation** - Test how ATS systems will read your CV
- **Job Description Matching** - Optimize for specific job postings

### 🎨 Professional Template Library
- **20+ Industry-Specific Templates** - Modern, Executive, Creative, Academic
- **Intelligent Auto-Layout** - Optimal formatting for different page sizes
- **Responsive Design** - Templates work on all devices
- **Color Scheme Customization** - Multiple professional color combinations
- **Typography Optimization** - ATS-friendly fonts and spacing

### 🔄 Real-Time Collaboration
- **Multi-User Editing** - Real-time collaborative CV editing
- **Operational Transform** - Conflict resolution for concurrent edits
- **Comment System** - Review and feedback functionality
- **Share Links** - Customizable permissions (view, edit, comment)
- **Version History** - Track changes and revisions

### 📈 Performance Analytics
- **CV Performance Tracking** - Views, downloads, application success rates
- **Interview Rate Analysis** - Track job application outcomes
- **ATS Score Monitoring** - Historical performance trends
- **Industry Benchmarking** - Compare against market standards
- **Actionable Insights** - AI-generated improvement recommendations

### 📱 Mobile-First Interface
- **Step-by-Step Mobile Editor** - Touch-optimized editing experience
- **Responsive Preview** - Mobile-friendly CV preview
- **Auto-Save Functionality** - Never lose your work
- **Touch-Friendly Controls** - Optimized for mobile devices
- **Offline Capability** - Work without internet connection

### 📥 Advanced Import System
- **LinkedIn Profile Import** - Extract data from LinkedIn profiles
- **PDF Resume Parsing** - Intelligent extraction from existing PDFs
- **DOCX Document Import** - Parse Microsoft Word documents
- **NLP-Powered Extraction** - Accurate section and content identification
- **Structured Data Output** - Clean, organized CV data

### 📤 Multi-Format Export
- **PDF Generation** - Professional, print-ready PDFs
- **Microsoft Word (DOCX)** - Editable Word documents
- **Plain Text (TXT)** - ATS-optimized text format
- **HTML Export** - Standalone web pages
- **JSON Data Export** - Structured data for portability

## 🏗️ Architecture

### Backend Services
```
├── 🤖 AI Optimization Service      # Content analysis and enhancement
├── 📊 ATS Compatibility Service   # Applicant tracking system optimization  
├── 🎨 Template Library Service    # Dynamic template generation
├── 📐 Layout Optimization Service # Intelligent page layout
├── 🔄 Collaboration Service       # Real-time editing and sharing
├── 📈 Analytics Service           # Performance tracking and insights
├── 📥 Import Service              # Document parsing and extraction
└── 📤 Export Service              # Multi-format document generation
```

### Frontend Components
```
├── 📱 Mobile Editor              # Touch-optimized editing interface
├── 👁️ Mobile Preview            # Responsive CV preview
├── 📊 Mobile Dashboard           # Analytics and CV management
├── 🖥️ Desktop Editor            # Full-featured desktop editing
├── 🔄 Collaboration Interface   # Real-time editing and comments
└── 📈 Analytics Dashboard       # Performance insights and reports
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- npm or yarn

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Access the Application
- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Advanced Features**: http://localhost:8000/api/v1/advanced

## 📖 API Documentation

### Core Endpoints
- `POST /api/v1/generate-from-form` - Generate CV from form data
- `POST /api/v1/generate-from-upload` - Update CV from uploaded file
- `GET /api/v1/health` - Service health check

### Advanced Features
- `POST /api/v1/advanced/import/linkedin` - Import LinkedIn profile
- `POST /api/v1/advanced/optimize/content` - AI content optimization
- `POST /api/v1/advanced/ats/analyze` - ATS compatibility analysis
- `POST /api/v1/advanced/export/multi-format` - Multi-format export
- `POST /api/v1/advanced/collaboration/session/create` - Start collaboration
- `GET /api/v1/advanced/analytics/dashboard/{user_id}` - Analytics dashboard

## 🎯 Use Cases

### For Job Seekers
- Create professional CVs with AI assistance
- Optimize for ATS systems and specific job postings
- Track application success and improve over time
- Collaborate with career coaches or mentors

### For Career Coaches
- Help multiple clients with collaborative editing
- Provide real-time feedback and suggestions
- Track client progress and success rates
- Use analytics to improve coaching strategies

### For Enterprises
- White-label CV platform for HR departments
- Bulk CV processing and analysis
- Integration with applicant tracking systems
- Employee career development programs

## 🔧 Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **Pydantic** - Data validation
- **Jinja2** - Template rendering
- **WeasyPrint** - PDF generation
- **spaCy** - Natural language processing
- **WebSockets** - Real-time collaboration

### Frontend  
- **Next.js** - React framework
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first styling
- **React Hook Form** - Form management
- **Socket.IO** - Real-time communication

### AI & Analytics
- **Google Gemini** - AI content generation
- **OpenAI Compatible APIs** - Alternative AI providers
- **Custom NLP Models** - Content analysis
- **Statistical Analysis** - Performance insights

## 📦 Deployment

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build
```

### Cloud Deployment
- **Frontend**: Vercel, Netlify, or any static hosting
- **Backend**: Railway, Render, DigitalOcean, or AWS
- **Database**: PostgreSQL, MySQL, or SQLite

### Environment Variables
```bash
# Backend
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=your_database_url
ALLOWED_ORIGINS=http://localhost:3000

# Frontend  
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Commit**: `git commit -m 'Add amazing feature'`
5. **Push**: `git push origin feature/amazing-feature`
6. **Create a Pull Request**

### Development Guidelines
- Follow PEP 8 for Python code
- Use TypeScript for frontend development
- Add unit tests for new features
- Update documentation for API changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by premium CV platforms like Enhancv and Zety
- Built with open source technologies
- Community-driven development

## 📞 Support

- **Documentation**: [Full API Docs](http://localhost:8000/docs)
- **Issues**: [GitHub Issues](https://github.com/yourusername/cv-genius/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/cv-genius/discussions)

## 🎯 Roadmap

### Version 2.1 (Coming Soon)
- [ ] Video CV generation
- [ ] LinkedIn auto-apply integration
- [ ] Advanced AI coaching
- [ ] Custom branding options

### Version 2.2 (Future)
- [ ] Multi-language support
- [ ] Voice-to-text CV creation
- [ ] Interview preparation tools
- [ ] Salary negotiation insights

---

**Made with ❤️ by the open source community**

*Turn your career potential into reality with CV Genius - the complete, free, and open source CV platform.*
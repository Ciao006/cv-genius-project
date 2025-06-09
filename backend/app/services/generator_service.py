"""
Core CV generation service using Google Gemini AI
"""

import json
import base64
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
import uuid
from io import BytesIO

import httpx
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None
try:
    from docx import Document
except ImportError:
    Document = None
from jinja2 import Environment, FileSystemLoader
try:
    from weasyprint import HTML, CSS
except ImportError:
    HTML = None
    CSS = None

from app.core.config import settings
from app.schemas.models import CVFormData, GeneratedCVResponse, PDFResponse


class CVGeneratorService:
    """Service for generating CVs using AI"""
    
    def __init__(self):
        self.gemini_api_key = settings.GEMINI_API_KEY
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent"
        
        # Initialize Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader('app/templates'),
            autoescape=True
        )
    
    async def generate_from_form(self, form_data: CVFormData) -> PDFResponse:
        """Generate CV from form data (Creator flow)"""
        try:
            # Create AI prompt for form data
            prompt = self._create_form_prompt(form_data)
            
            # Get AI response
            ai_response = await self._call_gemini(prompt)
            
            # Parse AI response
            cv_data = self._parse_ai_response(ai_response)
            
            # Generate PDFs
            cv_pdf, cover_letter_pdf = await self._generate_pdfs(cv_data)
            
            return PDFResponse(
                cv_pdf_base64=base64.b64encode(cv_pdf).decode(),
                cover_letter_pdf_base64=base64.b64encode(cover_letter_pdf).decode(),
                filename_cv=f"cv_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                filename_cover_letter=f"cover_letter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                generation_timestamp=datetime.now(),
                cv_data=cv_data
            )
            
        except Exception as e:
            raise Exception(f"CV generation failed: {str(e)}")
    
    async def generate_from_upload(self, cv_content: str, job_description: str) -> PDFResponse:
        """Generate CV from uploaded file (Updater flow)"""
        try:
            # Create AI prompt for CV update
            prompt = self._create_update_prompt(cv_content, job_description)
            
            # Get AI response
            ai_response = await self._call_gemini(prompt)
            
            # Parse AI response
            cv_data = self._parse_ai_response(ai_response)
            
            # Generate PDFs
            cv_pdf, cover_letter_pdf = await self._generate_pdfs(cv_data)
            
            return PDFResponse(
                cv_pdf_base64=base64.b64encode(cv_pdf).decode(),
                cover_letter_pdf_base64=base64.b64encode(cover_letter_pdf).decode(),
                filename_cv=f"updated_cv_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                filename_cover_letter=f"cover_letter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                generation_timestamp=datetime.now(),
                cv_data=cv_data
            )
            
        except Exception as e:
            raise Exception(f"CV update failed: {str(e)}")
    
    def extract_text_from_pdf(self, pdf_bytes: bytes) -> str:
        """Extract text from PDF file"""
        if PdfReader is None:
            raise Exception("PDF processing library not available. Please install pypdf")
        try:
            pdf_io = BytesIO(pdf_bytes)
            reader = PdfReader(pdf_io)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"PDF text extraction failed: {str(e)}")
    
    def extract_text_from_docx(self, docx_bytes: bytes) -> str:
        """Extract text from DOCX file"""
        if Document is None:
            raise Exception("DOCX processing library not available. Please install python-docx")
        try:
            docx_io = BytesIO(docx_bytes)
            doc = Document(docx_io)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"DOCX text extraction failed: {str(e)}")
    
    async def _call_gemini(self, prompt: str) -> str:
        """Make API call to Google Gemini"""
        try:
            headers = {
                "Content-Type": "application/json",
            }
            
            data = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.3,
                    "topK": 1,
                    "topP": 1,
                    "maxOutputTokens": 4096,
                }
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.gemini_url}?key={self.gemini_api_key}",
                    headers=headers,
                    json=data
                )
                response.raise_for_status()
                
                result = response.json()
                return result["candidates"][0]["content"]["parts"][0]["text"]
                
        except Exception as e:
            raise Exception(f"Gemini API call failed: {str(e)}")
    
    def _create_form_prompt(self, form_data: CVFormData) -> str:
        """Create AI prompt for form data processing"""
        # Extract company name from job description if available
        company_info = self._extract_company_info(form_data.job_description or "")
        
        return f"""You are an expert CV writer specializing in ATS-friendly CVs for the Dublin/Irish job market following official Irish employment standards. 

Transform the following raw form data into professional, compelling CV content that meets Dublin CV requirements:

DUBLIN CV REQUIREMENTS:
- Length: 1-2 pages maximum (1 page for new graduates)
- Format: Reverse chronological order (most recent first)
- Font: Standard professional fonts only (Arial, Times New Roman, Calibri 11-12pt)
- NO photos, colors, graphics, tables, or complex formatting
- Include quantifiable achievements with specific metrics (percentages, amounts, numbers)
- Use Irish phone format (+353) and Dublin address
- Professional email address required
- LinkedIn profile URL recommended
- Each job description must include 3-4 bullet points with action verbs
- Skills section organized by category (Technical, Soft, Languages)
- Education section with degree, institution, dates, location
- DO NOT include: birth date, marital status, nationality, references (unless requested)

ATS OPTIMIZATION:
- Use job description keywords naturally throughout CV
- Simple bullet points with strong action verbs
- Clear section headings in bold
- No headers/footers that ATS cannot read
- Standard section names: Professional Summary, Work Experience, Education, Skills

Transform the following raw form data into professional, compelling CV content that meets these Dublin standards.

FORM DATA:
Personal Details: {form_data.personal_details.model_dump()}
Work Experience: {[exp.model_dump() for exp in form_data.work_experience]}
Education: {[edu.model_dump() for edu in form_data.education]}
Skills: {form_data.skills}
Job Description: {form_data.job_description or "Not provided"}

IMPORTANT COVER LETTER REQUIREMENTS:
You are a professional cover letter generator for job applications. Generate a tailored cover letter for the specific job and candidate.

Instructions:
1. Read the provided job description and candidate's experience carefully
2. Extract company name from job description if available
3. Format requirements:
   - Write 3-4 professional paragraphs for the cover letter body only
   - DO NOT include salutation (Dear...) or closing (Sincerely...) in the cover_letter_body
   - Structure: Introduction → Body → Conclusion paragraphs
4. Content requirements:
   - Introduction: State the position, express enthusiasm, strong opening
   - Body: Highlight relevant skills, experience, and achievements that match job requirements with specific examples and quantifiable results
   - Conclusion: Express interest in the role, company-specific motivation, request for interview
5. Tone: Professional and positive, tailored to company culture
6. Keep content concise but impactful (suitable for one page)
7. Use specific examples from the candidate's experience that align with job requirements

Your task is to:
1. Create a compelling professional summary (3-4 sentences)
2. Transform work experience descriptions into impactful, action-oriented bullet points
3. Organize skills into relevant categories
4. Write a tailored cover letter body (3-4 paragraphs, no salutation or closing)

Output ONLY valid JSON in this exact format:
{{
    "personal_details": {{
        "full_name": "string",
        "email": "string",
        "phone": "string",
        "linkedin_url": "string",
        "location": "string"
    }},
    "professional_summary": "string",
    "work_experience": [
        {{
            "job_title": "string",
            "company": "string", 
            "start_date": "string",
            "end_date": "string",
            "is_current": boolean,
            "location": "string",
            "achievements": ["bullet point 1", "bullet point 2", "bullet point 3"]
        }}
    ],
    "education": [
        {{
            "degree": "string",
            "institution": "string",
            "start_date": "string", 
            "end_date": "string",
            "grade": "string",
            "location": "string"
        }}
    ],
    "skills": {{
        "technical": ["skill1", "skill2"],
        "soft": ["skill1", "skill2"],
        "languages": ["language1", "language2"]
    }},
    "cover_letter_body": "string",
    "company_name": "{company_info.get('name', '[Company Name]')}",
    "job_title": "{company_info.get('position', 'the position')}"
}}"""
    
    def _create_update_prompt(self, cv_content: str, job_description: str) -> str:
        """Create AI prompt for CV updating"""
        # Extract company name from job description if available
        company_info = self._extract_company_info(job_description)
        
        return f"""You are an expert career coach specializing in ATS-friendly CVs for the Irish and European job markets.

Analyze the provided CV and job description. Rewrite and enhance the CV to perfectly align with the job requirements while maintaining truthfulness.

CURRENT CV:
{cv_content}

TARGET JOB DESCRIPTION:
{job_description}

IMPORTANT COVER LETTER REQUIREMENTS:
You are a professional cover letter generator for job applications. Generate a tailored cover letter for the specific job and candidate.

Instructions:
1. Read the provided job description and candidate's CV carefully
2. Extract company name from job description if available
3. Format requirements:
   - Write 3-4 professional paragraphs for the cover letter body only
   - DO NOT include salutation (Dear...) or closing (Sincerely...) in the cover_letter_body
   - Structure: Introduction → Body → Conclusion paragraphs
4. Content requirements:
   - Introduction: State the position, express enthusiasm, strong opening
   - Body: Highlight relevant skills, experience, and achievements that match job requirements with specific examples and quantifiable results
   - Conclusion: Express interest in the role, company-specific motivation, request for interview
5. Tone: Professional and positive, tailored to company culture
6. Keep content concise but impactful (suitable for one page)
7. Use specific examples from the candidate's experience that align with job requirements

Your task is to:
1. Extract and enhance personal details
2. Create a targeted professional summary
3. Optimize work experience descriptions with relevant keywords
4. Highlight relevant skills and achievements
5. Write a compelling cover letter body (3-4 paragraphs, no salutation or closing)

Output ONLY valid JSON in this exact format:
{{
    "personal_details": {{
        "full_name": "string",
        "email": "string", 
        "phone": "string",
        "linkedin_url": "string",
        "location": "string"
    }},
    "professional_summary": "string",
    "work_experience": [
        {{
            "job_title": "string",
            "company": "string",
            "start_date": "string", 
            "end_date": "string",
            "is_current": boolean,
            "location": "string",
            "achievements": ["bullet point 1", "bullet point 2", "bullet point 3"]
        }}
    ],
    "education": [
        {{
            "degree": "string",
            "institution": "string",
            "start_date": "string",
            "end_date": "string", 
            "grade": "string",
            "location": "string"
        }}
    ],
    "skills": {{
        "technical": ["skill1", "skill2"],
        "soft": ["skill1", "skill2"], 
        "languages": ["language1", "language2"]
    }},
    "cover_letter_body": "string",
    "company_name": "{company_info.get('name', '[Company Name]')}",
    "job_title": "{company_info.get('position', 'the position')}"
}}"""
    
    def _extract_company_info(self, job_description: str) -> Dict[str, str]:
        """Extract company name and position from job description"""
        import re
        
        if not job_description:
            return {"name": "[Company Name]", "position": "the position"}
        
        # Common patterns for company names
        company_patterns = [
            r"at\s+([A-Z][a-zA-Z\s&.,]+?)(?:\s+is|,|\.|$)",
            r"([A-Z][a-zA-Z\s&.,]+?)\s+is\s+(?:seeking|looking|hiring)",
            r"Join\s+([A-Z][a-zA-Z\s&.,]+?)(?:\s+as|,|\.|$)",
            r"Company:\s*([A-Z][a-zA-Z\s&.,]+?)(?:\n|$)",
            r"Organization:\s*([A-Z][a-zA-Z\s&.,]+?)(?:\n|$)",
        ]
        
        # Common patterns for job titles
        position_patterns = [
            r"Position:\s*([A-Za-z\s&-]+?)(?:\n|$)",
            r"Role:\s*([A-Za-z\s&-]+?)(?:\n|$)",
            r"Job Title:\s*([A-Za-z\s&-]+?)(?:\n|$)",
            r"(?:seeking|hiring|for)\s+(?:a\s+)?([A-Za-z\s&-]+?)(?:\s+to|\s+with|\s+at|$)",
        ]
        
        company_name = "[Company Name]"
        position_title = "the position"
        
        # Try to extract company name
        for pattern in company_patterns:
            match = re.search(pattern, job_description, re.IGNORECASE)
            if match:
                company_name = match.group(1).strip()
                break
        
        # Try to extract position title
        for pattern in position_patterns:
            match = re.search(pattern, job_description, re.IGNORECASE)
            if match:
                position_title = match.group(1).strip()
                break
        
        return {"name": company_name, "position": position_title}
    
    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """Parse and validate AI response"""
        try:
            # Try to extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No valid JSON found in response")
            
            json_str = response[start_idx:end_idx]
            data = json.loads(json_str)
            
            # Validate required fields
            required_fields = [
                "personal_details", "professional_summary", 
                "work_experience", "education", "skills", "cover_letter_body"
            ]
            
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Set default values for new fields if missing
            if "company_name" not in data:
                data["company_name"] = "[Company Name]"
            if "job_title" not in data:
                data["job_title"] = "the position"
            
            return data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in AI response: {str(e)}")
        except Exception as e:
            raise ValueError(f"Failed to parse AI response: {str(e)}")
    
    async def _generate_pdfs(self, cv_data: Dict[str, Any]) -> tuple[bytes, bytes]:
        """Generate CV and cover letter PDFs"""
        if HTML is None:
            raise Exception("PDF generation library not available. Please install weasyprint")
        try:
            # Load templates
            cv_template = self.jinja_env.get_template('cv_template.html')
            letter_template = self.jinja_env.get_template('letter_template.html')
            
            # Add current date for cover letter
            template_data = cv_data.copy()
            template_data['generation_date'] = datetime.now().strftime("%B %d, %Y")
            
            # Render HTML
            cv_html = cv_template.render(**template_data)
            letter_html = letter_template.render(**template_data)
            
            # Generate PDFs
            cv_pdf = HTML(string=cv_html).write_pdf()
            letter_pdf = HTML(string=letter_html).write_pdf()
            
            return cv_pdf, letter_pdf
            
        except Exception as e:
            # Log error without exposing sensitive data
            error_msg = f"PDF generation failed: {type(e).__name__}"
            raise Exception(error_msg)


# Global service instance
cv_service = CVGeneratorService()
"""
Advanced import service for LinkedIn profiles and PDF/DOCX resumes
Free and open-source CV parsing system
"""

import re
import json
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
from io import BytesIO
import logging

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

try:
    from docx import Document
except ImportError:
    Document = None

try:
    import spacy
    # Load English model: python -m spacy download en_core_web_sm
    nlp = spacy.load("en_core_web_sm")
except ImportError:
    nlp = None

logger = logging.getLogger(__name__)


class LinkedInImporter:
    """
    LinkedIn profile data extractor
    Note: This uses public profile scraping - respect robots.txt and rate limits
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    async def import_from_url(self, linkedin_url: str) -> Dict[str, Any]:
        """Import CV data from LinkedIn public profile URL"""
        try:
            # This is a simplified version - in production, you'd need to handle
            # LinkedIn's authentication and API properly
            profile_data = await self._extract_profile_data(linkedin_url)
            return self._convert_to_cv_format(profile_data)
        except Exception as e:
            logger.error(f"LinkedIn import failed: {str(e)}")
            raise Exception(f"LinkedIn import failed: {str(e)}")
    
    async def _extract_profile_data(self, url: str) -> Dict[str, Any]:
        """Extract profile data from LinkedIn URL"""
        # For demo purposes - this would need proper LinkedIn API integration
        # or sophisticated scraping with proper rate limiting
        return {
            "name": "Sample User",
            "headline": "Software Developer",
            "location": "Dublin, Ireland",
            "experience": [
                {
                    "title": "Senior Developer",
                    "company": "Tech Company",
                    "duration": "2022 - Present",
                    "description": "Led development of web applications using React and Node.js"
                }
            ],
            "education": [
                {
                    "degree": "Computer Science",
                    "school": "University College Dublin",
                    "duration": "2018 - 2022"
                }
            ],
            "skills": ["JavaScript", "React", "Node.js", "Python"]
        }
    
    def _convert_to_cv_format(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert LinkedIn data to CV format"""
        return {
            "personal_details": {
                "full_name": profile_data.get("name", ""),
                "email": "",  # Not available from public profile
                "phone": "",  # Not available from public profile
                "linkedin_url": "",
                "location": profile_data.get("location", ""),
                "desired_position": profile_data.get("headline", "")
            },
            "professional_summary": f"Experienced {profile_data.get('headline', 'professional')} with expertise in {', '.join(profile_data.get('skills', [])[:3])}.",
            "work_experience": [
                {
                    "job_title": exp.get("title", ""),
                    "company": exp.get("company", ""),
                    "start_date": self._parse_date(exp.get("duration", "")).get("start", ""),
                    "end_date": self._parse_date(exp.get("duration", "")).get("end", ""),
                    "is_current": "Present" in exp.get("duration", ""),
                    "location": "",
                    "achievements": [exp.get("description", "")]
                }
                for exp in profile_data.get("experience", [])
            ],
            "education": [
                {
                    "degree": edu.get("degree", ""),
                    "institution": edu.get("school", ""),
                    "start_date": self._parse_date(edu.get("duration", "")).get("start", ""),
                    "end_date": self._parse_date(edu.get("duration", "")).get("end", ""),
                    "grade": "",
                    "location": ""
                }
                for edu in profile_data.get("education", [])
            ],
            "skills": {
                "technical": profile_data.get("skills", []),
                "soft": [],
                "languages": []
            }
        }
    
    def _parse_date(self, duration_str: str) -> Dict[str, str]:
        """Parse duration string like '2022 - Present' or '2018 - 2022'"""
        if not duration_str:
            return {"start": "", "end": ""}
        
        parts = duration_str.split(" - ")
        start = parts[0].strip() if len(parts) > 0 else ""
        end = parts[1].strip() if len(parts) > 1 else ""
        
        return {"start": start, "end": end}


class PDFResumeParser:
    """
    Advanced PDF resume parser using NLP and pattern matching
    """
    
    def __init__(self):
        self.section_patterns = {
            'personal': r'(name|email|phone|address|linkedin)',
            'summary': r'(summary|profile|objective|about)',
            'experience': r'(experience|employment|work|career)',
            'education': r'(education|academic|qualification|degree)',
            'skills': r'(skills|competenc|technical|proficienc)',
            'projects': r'(projects|portfolio|work samples)',
            'certifications': r'(certification|license|credential)'
        }
        
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}'
        self.date_pattern = r'(\d{1,2}\/\d{1,2}\/\d{2,4}|\d{4}[-\/]\d{1,2}[-\/]\d{1,2}|\w{3,9}\s+\d{4})'
    
    def parse_pdf(self, pdf_bytes: bytes) -> Dict[str, Any]:
        """Parse PDF resume and extract structured data"""
        if PdfReader is None:
            raise Exception("PDF parsing library not available. Install pypdf: pip install pypdf")
        
        try:
            # Extract text from PDF
            text = self._extract_text_from_pdf(pdf_bytes)
            
            # Parse sections using NLP and pattern matching
            sections = self._identify_sections(text)
            
            # Extract structured data
            return self._extract_structured_data(sections)
            
        except Exception as e:
            logger.error(f"PDF parsing failed: {str(e)}")
            raise Exception(f"PDF parsing failed: {str(e)}")
    
    def _extract_text_from_pdf(self, pdf_bytes: bytes) -> str:
        """Extract clean text from PDF"""
        pdf_io = BytesIO(pdf_bytes)
        reader = PdfReader(pdf_io)
        
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            text += page_text + "\n"
        
        # Clean up text
        text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single space
        text = re.sub(r'\n+', '\n', text)  # Multiple newlines to single
        
        return text.strip()
    
    def _identify_sections(self, text: str) -> Dict[str, str]:
        """Identify and extract different resume sections"""
        sections = {}
        lines = text.split('\n')
        current_section = 'unknown'
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line is a section header
            section_found = None
            for section_name, pattern in self.section_patterns.items():
                if re.search(pattern, line.lower()):
                    section_found = section_name
                    break
            
            if section_found:
                # Save previous section
                if current_section != 'unknown' and current_content:
                    sections[current_section] = '\n'.join(current_content)
                
                # Start new section
                current_section = section_found
                current_content = []
            else:
                current_content.append(line)
        
        # Save last section
        if current_section != 'unknown' and current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def _extract_structured_data(self, sections: Dict[str, str]) -> Dict[str, Any]:
        """Extract structured CV data from parsed sections"""
        # Extract personal details
        personal_details = self._extract_personal_details(sections)
        
        # Extract work experience
        work_experience = self._extract_work_experience(sections.get('experience', ''))
        
        # Extract education
        education = self._extract_education(sections.get('education', ''))
        
        # Extract skills
        skills = self._extract_skills(sections.get('skills', ''))
        
        # Extract summary
        professional_summary = sections.get('summary', '').strip()
        
        return {
            "personal_details": personal_details,
            "professional_summary": professional_summary,
            "work_experience": work_experience,
            "education": education,
            "skills": skills
        }
    
    def _extract_personal_details(self, sections: Dict[str, str]) -> Dict[str, str]:
        """Extract personal contact information"""
        # Combine all text to search for contact info
        full_text = ' '.join(sections.values())
        
        # Extract email
        email_match = re.search(self.email_pattern, full_text)
        email = email_match.group(0) if email_match else ""
        
        # Extract phone
        phone_match = re.search(self.phone_pattern, full_text)
        phone = phone_match.group(0) if phone_match else ""
        
        # Extract name (usually first line or largest text)
        name = self._extract_name(full_text)
        
        # Extract LinkedIn URL
        linkedin_pattern = r'(linkedin\.com/in/[^\s]+)'
        linkedin_match = re.search(linkedin_pattern, full_text)
        linkedin_url = linkedin_match.group(0) if linkedin_match else ""
        
        return {
            "full_name": name,
            "email": email,
            "phone": phone,
            "linkedin_url": linkedin_url,
            "location": "",  # Hard to extract reliably
            "desired_position": ""
        }
    
    def _extract_name(self, text: str) -> str:
        """Extract person's name using NLP"""
        if nlp is None:
            # Fallback: assume name is in first few words
            words = text.split()[:10]
            for i, word in enumerate(words):
                if word.istitle() and len(word) > 2:
                    # Try to find full name
                    name_parts = [word]
                    for j in range(i + 1, min(i + 3, len(words))):
                        if words[j].istitle() and len(words[j]) > 1:
                            name_parts.append(words[j])
                        else:
                            break
                    if len(name_parts) >= 2:
                        return ' '.join(name_parts)
            return words[0] if words else ""
        
        # Use spaCy for better name extraction
        doc = nlp(text[:500])  # Check first 500 characters
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        
        return ""
    
    def _extract_work_experience(self, experience_text: str) -> List[Dict[str, Any]]:
        """Extract work experience entries"""
        if not experience_text:
            return []
        
        experiences = []
        
        # Split by potential job entries (look for company names or job titles)
        entries = re.split(r'\n(?=[A-Z][^a-z]*[A-Z]|\d{4})', experience_text)
        
        for entry in entries:
            if len(entry.strip()) < 20:  # Skip very short entries
                continue
            
            exp = self._parse_experience_entry(entry.strip())
            if exp:
                experiences.append(exp)
        
        return experiences
    
    def _parse_experience_entry(self, entry: str) -> Optional[Dict[str, Any]]:
        """Parse individual experience entry"""
        lines = [line.strip() for line in entry.split('\n') if line.strip()]
        if len(lines) < 2:
            return None
        
        # First line usually contains job title and/or company
        first_line = lines[0]
        
        # Look for dates
        dates = re.findall(self.date_pattern, entry)
        start_date = dates[0] if len(dates) > 0 else ""
        end_date = dates[1] if len(dates) > 1 else ""
        is_current = "present" in entry.lower() or "current" in entry.lower()
        
        # Try to identify job title and company
        job_title, company = self._parse_job_title_company(first_line)
        
        # Extract achievements/descriptions
        achievements = []
        for line in lines[1:]:
            if re.search(r'^[•\-\*]', line) or len(line) > 30:
                achievements.append(line.lstrip('•-* '))
        
        return {
            "job_title": job_title,
            "company": company,
            "start_date": start_date,
            "end_date": end_date,
            "is_current": is_current,
            "location": "",
            "achievements": achievements
        }
    
    def _parse_job_title_company(self, line: str) -> tuple:
        """Parse job title and company from a line"""
        # Common patterns:
        # "Software Developer at Google"
        # "Google - Software Developer"
        # "Software Developer | Google"
        
        separators = [' at ', ' - ', ' | ', ', ']
        
        for sep in separators:
            if sep in line:
                parts = line.split(sep, 1)
                if len(parts) == 2:
                    return parts[0].strip(), parts[1].strip()
        
        # If no separator found, assume entire line is job title
        return line.strip(), ""
    
    def _extract_education(self, education_text: str) -> List[Dict[str, Any]]:
        """Extract education entries"""
        if not education_text:
            return []
        
        education = []
        entries = re.split(r'\n(?=[A-Z][^a-z]*[A-Z]|\d{4})', education_text)
        
        for entry in entries:
            if len(entry.strip()) < 10:
                continue
            
            edu = self._parse_education_entry(entry.strip())
            if edu:
                education.append(edu)
        
        return education
    
    def _parse_education_entry(self, entry: str) -> Optional[Dict[str, Any]]:
        """Parse individual education entry"""
        lines = [line.strip() for line in entry.split('\n') if line.strip()]
        if not lines:
            return None
        
        # Extract dates
        dates = re.findall(self.date_pattern, entry)
        start_date = dates[0] if len(dates) > 0 else ""
        end_date = dates[1] if len(dates) > 1 else ""
        
        # First line usually contains degree and/or institution
        first_line = lines[0]
        degree, institution = self._parse_degree_institution(first_line)
        
        # Look for GPA or grade
        grade_pattern = r'GPA:?\s*(\d+\.?\d*)'
        grade_match = re.search(grade_pattern, entry)
        grade = grade_match.group(1) if grade_match else ""
        
        return {
            "degree": degree,
            "institution": institution,
            "start_date": start_date,
            "end_date": end_date,
            "grade": grade,
            "location": ""
        }
    
    def _parse_degree_institution(self, line: str) -> tuple:
        """Parse degree and institution from a line"""
        # Common patterns similar to job title parsing
        separators = [' at ', ' - ', ' | ', ', ', ' from ']
        
        for sep in separators:
            if sep in line:
                parts = line.split(sep, 1)
                if len(parts) == 2:
                    return parts[0].strip(), parts[1].strip()
        
        return line.strip(), ""
    
    def _extract_skills(self, skills_text: str) -> Dict[str, List[str]]:
        """Extract and categorize skills"""
        if not skills_text:
            return {"technical": [], "soft": [], "languages": []}
        
        # Common technical skills patterns
        technical_keywords = [
            'javascript', 'python', 'java', 'react', 'node', 'sql', 'aws', 'docker',
            'git', 'html', 'css', 'angular', 'vue', 'php', 'ruby', 'go', 'rust',
            'kubernetes', 'jenkins', 'terraform', 'mongodb', 'postgresql'
        ]
        
        # Common soft skills patterns
        soft_keywords = [
            'leadership', 'communication', 'teamwork', 'problem solving', 'analytical',
            'creative', 'organized', 'detail-oriented', 'adaptable', 'collaborative'
        ]
        
        # Extract all potential skills
        skills_lower = skills_text.lower()
        all_skills = re.findall(r'\b[A-Za-z][A-Za-z0-9+#\.]*[A-Za-z0-9+#]\b', skills_text)
        
        technical = []
        soft = []
        languages = []
        
        for skill in all_skills:
            skill_lower = skill.lower()
            if skill_lower in technical_keywords or any(tech in skill_lower for tech in technical_keywords):
                technical.append(skill)
            elif skill_lower in soft_keywords or any(soft in skill_lower for soft in soft_keywords):
                soft.append(skill)
            elif len(skill) > 2 and skill.istitle():
                # Assume capitalized words might be technologies or languages
                technical.append(skill)
        
        return {
            "technical": list(set(technical)),
            "soft": list(set(soft)),
            "languages": languages
        }


class DOCXResumeParser:
    """
    DOCX resume parser
    """
    
    def parse_docx(self, docx_bytes: bytes) -> Dict[str, Any]:
        """Parse DOCX resume"""
        if Document is None:
            raise Exception("DOCX parsing library not available. Install python-docx: pip install python-docx")
        
        try:
            # Extract text from DOCX
            docx_io = BytesIO(docx_bytes)
            doc = Document(docx_io)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            # Use PDF parser logic for text processing
            pdf_parser = PDFResumeParser()
            sections = pdf_parser._identify_sections(text)
            return pdf_parser._extract_structured_data(sections)
            
        except Exception as e:
            logger.error(f"DOCX parsing failed: {str(e)}")
            raise Exception(f"DOCX parsing failed: {str(e)}")


class ImportService:
    """
    Main import service that coordinates all import methods
    """
    
    def __init__(self):
        self.linkedin_importer = LinkedInImporter()
        self.pdf_parser = PDFResumeParser()
        self.docx_parser = DOCXResumeParser()
    
    async def import_from_linkedin(self, linkedin_url: str) -> Dict[str, Any]:
        """Import CV data from LinkedIn profile"""
        return await self.linkedin_importer.import_from_url(linkedin_url)
    
    def import_from_pdf(self, pdf_bytes: bytes) -> Dict[str, Any]:
        """Import CV data from PDF file"""
        return self.pdf_parser.parse_pdf(pdf_bytes)
    
    def import_from_docx(self, docx_bytes: bytes) -> Dict[str, Any]:
        """Import CV data from DOCX file"""
        return self.docx_parser.parse_docx(docx_bytes)
    
    def import_from_file(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        """Auto-detect file type and import"""
        file_extension = filename.lower().split('.')[-1]
        
        if file_extension == 'pdf':
            return self.import_from_pdf(file_bytes)
        elif file_extension in ['docx', 'doc']:
            return self.import_from_docx(file_bytes)
        else:
            raise Exception(f"Unsupported file format: {file_extension}")


# Global service instance
import_service = ImportService()
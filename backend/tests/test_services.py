"""
Test cases for service layer
"""

import pytest
from unittest.mock import patch, MagicMock
import json
from io import BytesIO

from app.services.generator_service import CVGeneratorService
from app.schemas.models import CVFormData, PersonalDetails, WorkExperience, Education


class TestCVGeneratorService:
    """Test CVGeneratorService functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.service = CVGeneratorService()
        
        self.sample_personal = PersonalDetails(
            full_name="John Doe",
            email="john.doe@example.com",
            phone="+353 1 234 5678",
            linkedin_url="https://linkedin.com/in/johndoe",
            location="Dublin, Ireland"
        )
        
        self.sample_experience = [WorkExperience(
            job_title="Software Engineer",
            company="Tech Corp",
            start_date="Jan 2020",
            end_date="Dec 2023",
            is_current=False,
            description="Developed web applications using Python and React",
            location="Dublin, Ireland"
        )]
        
        self.sample_education = [Education(
            degree="BSc Computer Science",
            institution="Trinity College Dublin",
            start_date="Sep 2016",
            end_date="Jun 2020",
            grade="First Class Honours",
            location="Dublin, Ireland"
        )]
        
        self.sample_form_data = CVFormData(
            personal_details=self.sample_personal,
            work_experience=self.sample_experience,
            education=self.sample_education,
            skills="Python, JavaScript, React, Node.js, PostgreSQL",
            job_description="We are looking for a skilled software engineer..."
        )


class TestPromptGeneration(TestCVGeneratorService):
    """Test AI prompt generation"""
    
    def test_create_form_prompt(self):
        """Test form prompt creation"""
        prompt = self.service._create_form_prompt(self.sample_form_data)
        
        assert "expert CV writer" in prompt
        assert "Irish and European job markets" in prompt
        assert self.sample_personal.full_name in prompt
        assert self.sample_experience[0].job_title in prompt
        assert self.sample_education[0].degree in prompt
        assert self.sample_form_data.skills in prompt
        assert "JSON" in prompt
    
    def test_create_update_prompt(self):
        """Test CV update prompt creation"""
        cv_content = "John Doe\nSoftware Engineer at Tech Corp\nExperience with Python..."
        job_description = "Senior Developer position requiring Python and React..."
        
        prompt = self.service._create_update_prompt(cv_content, job_description)
        
        assert "career coach" in prompt
        assert "ATS-friendly" in prompt
        assert cv_content in prompt
        assert job_description in prompt
        assert "JSON" in prompt


class TestResponseParsing(TestCVGeneratorService):
    """Test AI response parsing"""
    
    def test_parse_valid_ai_response(self):
        """Test parsing valid AI response"""
        valid_response = """
        Here is the CV data:
        {
            "personal_details": {
                "full_name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+353 1 234 5678",
                "linkedin_url": "https://linkedin.com/in/johndoe",
                "location": "Dublin, Ireland"
            },
            "professional_summary": "Experienced software engineer...",
            "work_experience": [{
                "job_title": "Software Engineer",
                "company": "Tech Corp",
                "start_date": "Jan 2020",
                "end_date": "Dec 2023",
                "is_current": false,
                "location": "Dublin, Ireland",
                "achievements": ["Built scalable web applications", "Led team of 3 developers"]
            }],
            "education": [{
                "degree": "BSc Computer Science",
                "institution": "Trinity College Dublin",
                "start_date": "Sep 2016",
                "end_date": "Jun 2020",
                "grade": "First Class Honours",
                "location": "Dublin, Ireland"
            }],
            "skills": {
                "technical": ["Python", "JavaScript", "React"],
                "soft": ["Leadership", "Communication"],
                "languages": ["English", "Irish"]
            },
            "cover_letter_body": "Dear Hiring Manager, I am excited to apply..."
        }
        """
        
        result = self.service._parse_ai_response(valid_response)
        
        assert "personal_details" in result
        assert "professional_summary" in result
        assert "work_experience" in result
        assert "education" in result
        assert "skills" in result
        assert "cover_letter_body" in result
        
        assert result["personal_details"]["full_name"] == "John Doe"
        assert len(result["work_experience"]) == 1
        assert len(result["education"]) == 1
    
    def test_parse_invalid_json_response(self):
        """Test parsing invalid JSON response"""
        invalid_response = "This is not valid JSON {broken"
        
        with pytest.raises(ValueError, match="Invalid JSON"):
            self.service._parse_ai_response(invalid_response)
    
    def test_parse_missing_fields_response(self):
        """Test parsing response with missing required fields"""
        incomplete_response = """
        {
            "personal_details": {
                "full_name": "John Doe",
                "email": "john.doe@example.com"
            },
            "professional_summary": "Summary here"
        }
        """
        
        with pytest.raises(ValueError, match="Missing required field"):
            self.service._parse_ai_response(incomplete_response)


class TestFileProcessing(TestCVGeneratorService):
    """Test file processing functionality"""
    
    def test_extract_text_from_pdf_success(self):
        """Test successful PDF text extraction"""
        # This would require a real PDF file for full testing
        # For now, test that the method exists and handles errors
        with pytest.raises(Exception):
            self.service.extract_text_from_pdf(b"not a pdf")
    
    def test_extract_text_from_docx_success(self):
        """Test successful DOCX text extraction"""
        # This would require a real DOCX file for full testing
        # For now, test that the method exists and handles errors
        with pytest.raises(Exception):
            self.service.extract_text_from_docx(b"not a docx")


class TestAIIntegration(TestCVGeneratorService):
    """Test AI service integration"""
    
    @patch('httpx.AsyncClient.post')
    async def test_call_gemini_success(self, mock_post):
        """Test successful Gemini API call"""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "candidates": [{
                "content": {
                    "parts": [{
                        "text": "Generated CV content here"
                    }]
                }
            }]
        }
        mock_post.return_value.__aenter__.return_value = mock_response
        
        result = await self.service._call_gemini("Test prompt")
        
        assert result == "Generated CV content here"
        mock_post.assert_called_once()
    
    @patch('httpx.AsyncClient.post')
    async def test_call_gemini_api_error(self, mock_post):
        """Test Gemini API error handling"""
        # Mock API error
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("API Error")
        mock_post.return_value.__aenter__.return_value = mock_response
        
        with pytest.raises(Exception, match="Gemini API call failed"):
            await self.service._call_gemini("Test prompt")


class TestPDFGeneration(TestCVGeneratorService):
    """Test PDF generation functionality"""
    
    @patch('app.services.generator_service.HTML')
    async def test_generate_pdfs_success(self, mock_html):
        """Test successful PDF generation"""
        # Mock WeasyPrint HTML class
        mock_pdf_content = b"fake pdf content"
        mock_html_instance = MagicMock()
        mock_html_instance.write_pdf.return_value = mock_pdf_content
        mock_html.return_value = mock_html_instance
        
        sample_data = {
            "personal_details": self.sample_personal.dict(),
            "professional_summary": "Test summary",
            "work_experience": [exp.dict() for exp in self.sample_experience],
            "education": [edu.dict() for edu in self.sample_education],
            "skills": {"technical": ["Python"], "soft": ["Leadership"], "languages": ["English"]},
            "cover_letter_body": "Test cover letter"
        }
        
        cv_pdf, letter_pdf = await self.service._generate_pdfs(sample_data)
        
        assert cv_pdf == mock_pdf_content
        assert letter_pdf == mock_pdf_content
        
        # Verify HTML was called twice (CV and cover letter)
        assert mock_html.call_count == 2


class TestEndToEndService(TestCVGeneratorService):
    """Test end-to-end service functionality"""
    
    @patch('app.services.generator_service.cv_service._call_gemini')
    @patch('app.services.generator_service.cv_service._generate_pdfs')
    async def test_generate_from_form_complete_flow(self, mock_pdf, mock_gemini):
        """Test complete form generation flow"""
        # Mock AI response
        mock_ai_response = json.dumps({
            "personal_details": self.sample_personal.dict(),
            "professional_summary": "Experienced software engineer...",
            "work_experience": [{
                "job_title": "Software Engineer",
                "company": "Tech Corp",
                "start_date": "Jan 2020",
                "end_date": "Dec 2023",
                "is_current": False,
                "location": "Dublin, Ireland",
                "achievements": ["Built applications", "Led team"]
            }],
            "education": [edu.dict() for edu in self.sample_education],
            "skills": {
                "technical": ["Python", "JavaScript"],
                "soft": ["Leadership"],
                "languages": ["English"]
            },
            "cover_letter_body": "Dear Hiring Manager..."
        })
        mock_gemini.return_value = mock_ai_response
        
        # Mock PDF generation
        mock_pdf.return_value = (b"cv content", b"letter content")
        
        result = await self.service.generate_from_form(self.sample_form_data)
        
        # Verify result structure
        assert hasattr(result, 'cv_pdf_base64')
        assert hasattr(result, 'cover_letter_pdf_base64')
        assert hasattr(result, 'filename_cv')
        assert hasattr(result, 'filename_cover_letter')
        assert hasattr(result, 'generation_timestamp')
        
        # Verify methods were called
        mock_gemini.assert_called_once()
        mock_pdf.assert_called_once()
    
    @patch('app.services.generator_service.cv_service._call_gemini')
    @patch('app.services.generator_service.cv_service._generate_pdfs')
    async def test_generate_from_upload_complete_flow(self, mock_pdf, mock_gemini):
        """Test complete upload generation flow"""
        cv_content = "John Doe\nSoftware Engineer\nExperience with Python..."
        job_description = "Senior Developer position..."
        
        # Mock AI response
        mock_ai_response = json.dumps({
            "personal_details": self.sample_personal.dict(),
            "professional_summary": "Updated summary...",
            "work_experience": [{
                "job_title": "Senior Software Engineer",
                "company": "Tech Corp",
                "start_date": "Jan 2020",
                "end_date": "Present",
                "is_current": True,
                "location": "Dublin, Ireland",
                "achievements": ["Optimized for new role", "Enhanced skills"]
            }],
            "education": [edu.dict() for edu in self.sample_education],
            "skills": {
                "technical": ["Python", "JavaScript", "React"],
                "soft": ["Leadership", "Communication"],
                "languages": ["English"]
            },
            "cover_letter_body": "Tailored cover letter..."
        })
        mock_gemini.return_value = mock_ai_response
        
        # Mock PDF generation
        mock_pdf.return_value = (b"updated cv", b"tailored letter")
        
        result = await self.service.generate_from_upload(cv_content, job_description)
        
        # Verify result structure
        assert hasattr(result, 'cv_pdf_base64')
        assert hasattr(result, 'cover_letter_pdf_base64')
        assert result.filename_cv.startswith('updated_cv_')
        
        # Verify methods were called
        mock_gemini.assert_called_once()
        mock_pdf.assert_called_once()


# Test fixtures and utilities
@pytest.fixture
def mock_cv_service():
    """Fixture providing a mocked CV service"""
    with patch('app.services.generator_service.cv_service') as mock:
        yield mock


@pytest.fixture
def sample_pdf_response():
    """Fixture providing sample PDF response"""
    return {
        "cv_pdf_base64": "base64encodedcv",
        "cover_letter_pdf_base64": "base64encodedletter",
        "filename_cv": "cv_20240101_120000.pdf",
        "filename_cover_letter": "cover_letter_20240101_120000.pdf",
        "generation_timestamp": "2024-01-01T12:00:00Z"
    }
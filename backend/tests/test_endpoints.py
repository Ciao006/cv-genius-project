"""
Test cases for API endpoints
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import json

from main import app
from app.schemas.models import CVFormData, PersonalDetails, WorkExperience, Education

client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns expected response"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "CVGenius API is running"
        assert data["version"] == "1.0.0"
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "cvgenius-api"


class TestSupportEndpoints:
    """Test support endpoints"""
    
    def test_supported_formats(self):
        """Test supported formats endpoint"""
        response = client.get("/api/v1/supported-formats")
        assert response.status_code == 200
        data = response.json()
        assert "supported_formats" in data
        assert "max_file_size" in data
        assert len(data["supported_formats"]) >= 2  # PDF and DOCX


class TestFormValidation:
    """Test form validation endpoints"""
    
    def test_validate_form_valid_data(self):
        """Test form validation with valid data"""
        valid_data = {
            "personal_details": {
                "full_name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+353 1 234 5678",
                "linkedin_url": "https://linkedin.com/in/johndoe",
                "location": "Dublin, Ireland"
            },
            "work_experience": [{
                "job_title": "Software Engineer",
                "company": "Tech Corp",
                "start_date": "Jan 2020",
                "end_date": "Dec 2023",
                "is_current": False,
                "description": "Developed web applications using Python and React",
                "location": "Dublin, Ireland"
            }],
            "education": [{
                "degree": "BSc Computer Science",
                "institution": "Trinity College Dublin",
                "start_date": "Sep 2016",
                "end_date": "Jun 2020",
                "grade": "First Class Honours",
                "location": "Dublin, Ireland"
            }],
            "skills": "Python, JavaScript, React, Node.js, PostgreSQL",
            "job_description": "We are looking for a skilled software engineer to join our team..."
        }
        
        response = client.post("/api/v1/validate-form", json=valid_data)
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is True
    
    def test_validate_form_invalid_email(self):
        """Test form validation with invalid email"""
        invalid_data = {
            "personal_details": {
                "full_name": "John Doe",
                "email": "invalid-email",  # Invalid email
                "phone": "+353 1 234 5678"
            },
            "work_experience": [{
                "job_title": "Software Engineer",
                "company": "Tech Corp",
                "start_date": "Jan 2020",
                "is_current": True,
                "description": "Developed web applications"
            }],
            "education": [{
                "degree": "BSc Computer Science",
                "institution": "Trinity College Dublin",
                "start_date": "Sep 2016"
            }],
            "skills": "Python, JavaScript"
        }
        
        response = client.post("/api/v1/validate-form", json=invalid_data)
        assert response.status_code == 422  # Validation error


class TestCVGeneration:
    """Test CV generation endpoints with mocked AI service"""
    
    @patch('app.services.generator_service.cv_service.generate_from_form')
    def test_generate_from_form_success(self, mock_generate):
        """Test successful CV generation from form"""
        # Mock the service response
        mock_response = {
            "cv_pdf_base64": "base64encodedpdf",
            "cover_letter_pdf_base64": "base64encodedletter",
            "filename_cv": "cv_20240101_120000.pdf",
            "filename_cover_letter": "cover_letter_20240101_120000.pdf",
            "generation_timestamp": "2024-01-01T12:00:00"
        }
        mock_generate.return_value = mock_response
        
        valid_form_data = {
            "personal_details": {
                "full_name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+353 1 234 5678"
            },
            "work_experience": [{
                "job_title": "Software Engineer",
                "company": "Tech Corp",
                "start_date": "Jan 2020",
                "is_current": True,
                "description": "Developed web applications using modern technologies"
            }],
            "education": [{
                "degree": "BSc Computer Science",
                "institution": "Trinity College Dublin",
                "start_date": "Sep 2016",
                "end_date": "Jun 2020"
            }],
            "skills": "Python, JavaScript, React, Node.js"
        }
        
        response = client.post("/api/v1/generate-from-form", json=valid_form_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "cv_pdf_base64" in data
        assert "cover_letter_pdf_base64" in data
        assert data["filename_cv"].endswith(".pdf")
        
        # Verify the service was called
        mock_generate.assert_called_once()
    
    def test_generate_from_form_missing_name(self):
        """Test CV generation with missing required field"""
        invalid_data = {
            "personal_details": {
                "full_name": "",  # Empty name
                "email": "john.doe@example.com",
                "phone": "+353 1 234 5678"
            },
            "work_experience": [{
                "job_title": "Software Engineer",
                "company": "Tech Corp",
                "start_date": "Jan 2020",
                "is_current": True,
                "description": "Developed applications"
            }],
            "education": [{
                "degree": "BSc Computer Science",
                "institution": "Trinity College Dublin",
                "start_date": "Sep 2016"
            }],
            "skills": "Python, JavaScript"
        }
        
        response = client.post("/api/v1/generate-from-form", json=invalid_data)
        assert response.status_code == 400
    
    def test_generate_from_upload_no_file(self):
        """Test CV generation from upload without file"""
        response = client.post(
            "/api/v1/generate-from-upload",
            data={"job_description": "Software engineer position..."}
        )
        assert response.status_code == 422  # Missing file


class TestRateLimiting:
    """Test rate limiting functionality"""
    
    def test_rate_limit_health_endpoint(self):
        """Test that health endpoints are not rate limited"""
        # Make multiple requests quickly
        for _ in range(20):
            response = client.get("/api/v1/health")
            assert response.status_code == 200
    
    # Note: Actual rate limiting tests would require multiple requests
    # and are better suited for integration tests


@pytest.fixture
def sample_form_data():
    """Fixture providing sample form data for tests"""
    return {
        "personal_details": {
            "full_name": "Jane Smith",
            "email": "jane.smith@example.com",
            "phone": "+353 1 987 6543",
            "linkedin_url": "https://linkedin.com/in/janesmith",
            "location": "Cork, Ireland"
        },
        "work_experience": [{
            "job_title": "Senior Developer",
            "company": "Innovation Ltd",
            "start_date": "Mar 2021",
            "end_date": "Present",
            "is_current": True,
            "description": "Led development of cloud-native applications using microservices architecture",
            "location": "Cork, Ireland"
        }],
        "education": [{
            "degree": "MSc Software Engineering",
            "institution": "University College Cork",
            "start_date": "Sep 2019",
            "end_date": "Jun 2021",
            "grade": "Distinction",
            "location": "Cork, Ireland"
        }],
        "skills": "Python, AWS, Docker, Kubernetes, React, TypeScript",
        "job_description": "Senior full-stack developer role requiring experience with cloud technologies..."
    }


class TestEndToEnd:
    """End-to-end test scenarios"""
    
    @patch('app.services.generator_service.cv_service._call_gemini')
    def test_complete_cv_generation_flow(self, mock_gemini, sample_form_data):
        """Test complete CV generation flow with mocked AI"""
        # Mock AI response
        mock_ai_response = json.dumps({
            "personal_details": sample_form_data["personal_details"],
            "professional_summary": "Experienced software engineer...",
            "work_experience": [{
                "job_title": "Senior Developer",
                "company": "Innovation Ltd",
                "start_date": "Mar 2021",
                "end_date": "Present",
                "is_current": True,
                "location": "Cork, Ireland",
                "achievements": [
                    "Led development of cloud-native applications",
                    "Improved system performance by 40%",
                    "Mentored junior developers"
                ]
            }],
            "education": sample_form_data["education"],
            "skills": {
                "technical": ["Python", "AWS", "Docker"],
                "soft": ["Leadership", "Communication"],
                "languages": ["English", "Irish"]
            },
            "cover_letter_body": "Dear Hiring Manager, I am writing to express my interest..."
        })
        mock_gemini.return_value = mock_ai_response
        
        # Mock PDF generation to avoid WeasyPrint dependencies in tests
        with patch('app.services.generator_service.cv_service._generate_pdfs') as mock_pdf:
            mock_pdf.return_value = (b"fake pdf content", b"fake letter content")
            
            response = client.post("/api/v1/generate-from-form", json=sample_form_data)
            
            assert response.status_code == 200
            data = response.json()
            
            # Verify response structure
            assert "cv_pdf_base64" in data
            assert "cover_letter_pdf_base64" in data
            assert "filename_cv" in data
            assert "filename_cover_letter" in data
            assert "generation_timestamp" in data
            
            # Verify mocks were called
            mock_gemini.assert_called_once()
            mock_pdf.assert_called_once()
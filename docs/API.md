# CVGenius API Documentation

## Base URL
- **Development**: `http://localhost:8000`
- **Production**: `https://cvgenius-backend-449239631634.europe-west1.run.app`

## Authentication
No authentication required. All endpoints are public.

## Endpoints

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-09T12:00:00Z",
  "version": "1.0.0"
}
```

### Generate CV from Form Data
```http
POST /api/v1/generate-cv
```

**Request Body:**
```json
{
  "personal_details": {
    "full_name": "string",
    "email": "string",
    "phone": "string",
    "linkedin_url": "string",
    "location": "string"
  },
  "work_experience": [
    {
      "job_title": "string",
      "company": "string",
      "start_date": "string",
      "end_date": "string",
      "is_current": boolean,
      "location": "string",
      "description": "string"
    }
  ],
  "education": [
    {
      "degree": "string",
      "institution": "string",
      "start_date": "string",
      "end_date": "string",
      "grade": "string",
      "location": "string"
    }
  ],
  "skills": ["string"],
  "job_description": "string"
}
```

**Response:**
```json
{
  "cv_pdf_base64": "string",
  "cover_letter_pdf_base64": "string",
  "filename_cv": "string",
  "filename_cover_letter": "string",
  "generation_timestamp": "2025-01-09T12:00:00Z",
  "cv_data": {
    "personal_details": {},
    "professional_summary": "string",
    "work_experience": [],
    "education": [],
    "skills": {},
    "cover_letter_body": "string",
    "company_name": "string",
    "job_title": "string"
  }
}
```

### Generate CV from Upload
```http
POST /api/v1/generate-from-upload
```

**Request:**
- Multipart form data
- `cv_file`: PDF or DOCX file
- `job_description`: Text

**Response:** Same as generate-cv

### Generate Cover Letter PDF
```http
POST /api/v1/generate-cover-letter-pdf
```

**Request Body:**
```json
{
  "personal_details": {},
  "cover_letter_body": "string",
  "company_name": "string",
  "job_title": "string",
  "generation_date": "string"
}
```

**Response:**
```json
{
  "cover_letter_pdf_base64": "string",
  "filename_cover_letter": "string"
}
```

### Regenerate Cover Letter
```http
POST /api/v1/regenerate-cover-letter
```

**Request Body:**
```json
{
  "cv_data": {},
  "job_description": "string"
}
```

**Response:**
```json
{
  "personal_details": {},
  "professional_summary": "string",
  "work_experience": [],
  "education": [],
  "skills": {},
  "cover_letter_body": "string",
  "company_name": "string",
  "job_title": "string"
}
```

### Configuration Info
```http
GET /api/v1/config
```

**Response:**
```json
{
  "supported_file_types": ["pdf", "docx"],
  "max_file_size": 5242880,
  "max_file_size_mb": 5.0
}
```

## Error Handling

### Error Response Format
```json
{
  "detail": "Error message description"
}
```

### Status Codes
- `200`: Success
- `400`: Bad Request (validation error)
- `413`: Payload Too Large (file too big)
- `422`: Unprocessable Entity (invalid data)
- `429`: Too Many Requests (rate limit exceeded)
- `500`: Internal Server Error

## Rate Limiting
- **Limit**: 10 requests per minute per IP
- **Headers**: 
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

## File Upload Limits
- **Maximum file size**: 5MB
- **Supported formats**: PDF, DOCX
- **Content types**: `application/pdf`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`

## Examples

### cURL Examples

#### Generate CV from form:
```bash
curl -X POST "http://localhost:8000/api/v1/generate-cv" \
  -H "Content-Type: application/json" \
  -d '{"personal_details": {"full_name": "John Doe", "email": "john@example.com"}, "work_experience": [], "education": [], "skills": [], "job_description": ""}'
```

#### Upload CV file:
```bash
curl -X POST "http://localhost:8000/api/v1/generate-from-upload" \
  -F "cv_file=@resume.pdf" \
  -F "job_description=Software Engineer position..."
``` 
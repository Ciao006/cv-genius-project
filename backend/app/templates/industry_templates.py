"""
Industry-specific CV template library
20+ professional templates for different industries and career levels
Free and open-source
"""

from typing import Dict, List, Any

# Color schemes for different industries
COLOR_SCHEMES = {
    "tech": {
        "primary": "#3182ce",
        "secondary": "#2d3748", 
        "accent": "#4299e1",
        "text": "#1a202c",
        "background": "#ffffff"
    },
    "creative": {
        "primary": "#6b46c1",
        "secondary": "#553c9a",
        "accent": "#805ad5",
        "text": "#2d3748",
        "background": "#fefefe"
    },
    "business": {
        "primary": "#2b6cb0",
        "secondary": "#1e4a72",
        "accent": "#3182ce",
        "text": "#1a202c",
        "background": "#ffffff"
    },
    "healthcare": {
        "primary": "#38a169",
        "secondary": "#2f855a",
        "accent": "#48bb78",
        "text": "#1a202c",
        "background": "#ffffff"
    },
    "finance": {
        "primary": "#1a365d",
        "secondary": "#2c5282",
        "accent": "#3182ce",
        "text": "#1a202c",
        "background": "#ffffff"
    },
    "education": {
        "primary": "#d69e2e",
        "secondary": "#b7791f",
        "accent": "#ed8936",
        "text": "#1a202c",
        "background": "#ffffff"
    },
    "minimal": {
        "primary": "#000000",
        "secondary": "#4a5568",
        "accent": "#718096",
        "text": "#000000",
        "background": "#ffffff"
    }
}

# Font combinations
FONT_COMBINATIONS = {
    "professional": {
        "header": "'Playfair Display', serif",
        "body": "'Source Sans Pro', sans-serif",
        "accent": "'Source Sans Pro', sans-serif"
    },
    "modern": {
        "header": "'Inter', sans-serif",
        "body": "'Inter', sans-serif", 
        "accent": "'Inter', sans-serif"
    },
    "classic": {
        "header": "'Times New Roman', serif",
        "body": "'Times New Roman', serif",
        "accent": "'Times New Roman', serif"
    },
    "tech": {
        "header": "'Roboto', sans-serif",
        "body": "'Roboto', sans-serif",
        "accent": "'Roboto Mono', monospace"
    },
    "creative": {
        "header": "'Montserrat', sans-serif",
        "body": "'Open Sans', sans-serif",
        "accent": "'Montserrat', sans-serif"
    }
}

class TemplateLibrary:
    """
    Comprehensive library of industry-specific CV templates
    """
    
    def __init__(self):
        self.templates = self._initialize_templates()
    
    def get_template(self, template_id: str) -> Dict[str, Any]:
        """Get specific template by ID"""
        return self.templates.get(template_id, self.templates["modern_tech"])
    
    def get_templates_by_industry(self, industry: str) -> List[Dict[str, Any]]:
        """Get all templates for a specific industry"""
        return [template for template in self.templates.values() 
                if template["industry"] == industry]
    
    def get_all_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get all available templates"""
        return self.templates
    
    def _initialize_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize all template definitions"""
        return {
            # TECHNOLOGY TEMPLATES
            "modern_tech": {
                "id": "modern_tech",
                "name": "Modern Tech",
                "industry": "technology",
                "level": "mid-senior",
                "description": "Clean, modern design perfect for software developers and tech professionals",
                "colors": COLOR_SCHEMES["tech"],
                "fonts": FONT_COMBINATIONS["tech"],
                "layout": "single_column",
                "sections": ["header", "summary", "skills", "experience", "education", "projects"],
                "features": ["skills_bars", "project_links", "github_integration"]
            },
            
            "minimal_developer": {
                "id": "minimal_developer", 
                "name": "Minimal Developer",
                "industry": "technology",
                "level": "senior",
                "description": "Ultra-clean minimal design for senior developers",
                "colors": COLOR_SCHEMES["minimal"],
                "fonts": FONT_COMBINATIONS["modern"],
                "layout": "single_column",
                "sections": ["header", "summary", "experience", "skills", "education"],
                "features": ["ats_optimized", "minimal_design", "skills_grid"]
            },
            
            "startup_engineer": {
                "id": "startup_engineer",
                "name": "Startup Engineer", 
                "industry": "technology",
                "level": "junior-mid",
                "description": "Dynamic design for startup and fast-paced environments",
                "colors": {"primary": "#ff6b35", "secondary": "#f7931e", "accent": "#ffaa44", "text": "#1a202c", "background": "#ffffff"},
                "fonts": FONT_COMBINATIONS["modern"],
                "layout": "single_column",
                "sections": ["header", "summary", "skills", "experience", "projects", "education"],
                "features": ["skills_cloud", "project_showcase", "startup_focus"]
            },
            
            "data_scientist": {
                "id": "data_scientist",
                "name": "Data Scientist",
                "industry": "technology", 
                "level": "mid-senior",
                "description": "Data-focused template with analytics emphasis",
                "colors": {"primary": "#2563eb", "secondary": "#1e40af", "accent": "#3b82f6", "text": "#1a202c", "background": "#ffffff"},
                "fonts": FONT_COMBINATIONS["professional"],
                "layout": "two_column",
                "sections": ["header", "summary", "skills", "experience", "education", "publications", "certifications"],
                "features": ["skills_charts", "publication_list", "certification_badges"]
            },
            
            "devops_engineer": {
                "id": "devops_engineer",
                "name": "DevOps Engineer",
                "industry": "technology",
                "level": "mid-senior", 
                "description": "Infrastructure-focused template for DevOps professionals",
                "colors": {"primary": "#059669", "secondary": "#047857", "accent": "#10b981", "text": "#1a202c", "background": "#ffffff"},
                "fonts": FONT_COMBINATIONS["tech"],
                "layout": "single_column",
                "sections": ["header", "summary", "technical_skills", "experience", "certifications", "education"],
                "features": ["tech_stack_icons", "cloud_badges", "automation_focus"]
            },
            
            # BUSINESS TEMPLATES
            "executive_professional": {
                "id": "executive_professional",
                "name": "Executive Professional",
                "industry": "business",
                "level": "senior-executive",
                "description": "Premium design for C-level executives and senior management",
                "colors": COLOR_SCHEMES["business"],
                "fonts": FONT_COMBINATIONS["professional"],
                "layout": "two_column",
                "sections": ["header", "executive_summary", "key_achievements", "experience", "education", "board_positions"],
                "features": ["executive_summary", "achievement_highlights", "leadership_focus"]
            },
            
            "business_consultant": {
                "id": "business_consultant",
                "name": "Business Consultant",
                "industry": "business",
                "level": "mid-senior",
                "description": "Professional consulting-focused template",
                "colors": COLOR_SCHEMES["business"],
                "fonts": FONT_COMBINATIONS["professional"],
                "layout": "single_column", 
                "sections": ["header", "summary", "expertise", "experience", "education", "certifications"],
                "features": ["expertise_areas", "client_logos", "case_studies"]
            },
            
            "sales_professional": {
                "id": "sales_professional",
                "name": "Sales Professional",
                "industry": "business",
                "level": "mid",
                "description": "Results-driven template for sales professionals",
                "colors": {"primary": "#dc2626", "secondary": "#b91c1c", "accent": "#ef4444", "text": "#1a202c", "background": "#ffffff"},
                "fonts": FONT_COMBINATIONS["modern"],
                "layout": "single_column",
                "sections": ["header", "summary", "achievements", "experience", "education", "awards"],
                "features": ["metrics_highlights", "achievement_numbers", "sales_focus"]
            },
            
            "marketing_manager": {
                "id": "marketing_manager", 
                "name": "Marketing Manager",
                "industry": "business",
                "level": "mid",
                "description": "Creative marketing-focused template",
                "colors": {"primary": "#7c3aed", "secondary": "#6d28d9", "accent": "#8b5cf6", "text": "#1a202c", "background": "#ffffff"},
                "fonts": FONT_COMBINATIONS["creative"],
                "layout": "two_column",
                "sections": ["header", "summary", "skills", "experience", "education", "campaigns"],
                "features": ["campaign_showcase", "brand_colors", "creative_elements"]
            },
            
            "project_manager": {
                "id": "project_manager",
                "name": "Project Manager",
                "industry": "business",
                "level": "mid-senior",
                "description": "Organized template for project management professionals", 
                "colors": COLOR_SCHEMES["business"],
                "fonts": FONT_COMBINATIONS["professional"],
                "layout": "single_column",
                "sections": ["header", "summary", "methodologies", "experience", "education", "certifications"],
                "features": ["methodology_badges", "project_timeline", "team_leadership"]
            },
            
            # CREATIVE TEMPLATES
            "creative_director": {
                "id": "creative_director",
                "name": "Creative Director",
                "industry": "creative",
                "level": "senior",
                "description": "Bold creative template for design professionals",
                "colors": COLOR_SCHEMES["creative"],
                "fonts": FONT_COMBINATIONS["creative"],
                "layout": "portfolio_style",
                "sections": ["header", "summary", "portfolio", "experience", "education", "awards"],
                "features": ["portfolio_grid", "color_accent", "creative_layout"]
            },
            
            "graphic_designer": {
                "id": "graphic_designer",
                "name": "Graphic Designer", 
                "industry": "creative",
                "level": "junior-mid",
                "description": "Visual-focused template for graphic designers",
                "colors": {"primary": "#ec4899", "secondary": "#db2777", "accent": "#f472b6", "text": "#1a202c", "background": "#ffffff"},
                "fonts": FONT_COMBINATIONS["creative"],
                "layout": "visual_portfolio",
                "sections": ["header", "summary", "skills", "portfolio", "experience", "education"],
                "features": ["visual_portfolio", "design_skills", "creative_showcase"]
            },
            
            "ux_designer": {
                "id": "ux_designer",
                "name": "UX Designer",
                "industry": "creative",
                "level": "mid",
                "description": "User-experience focused design template",
                "colors": {"primary": "#0891b2", "secondary": "#0e7490", "accent": "#06b6d4", "text": "#1a202c", "background": "#ffffff"},
                "fonts": FONT_COMBINATIONS["modern"],
                "layout": "user_focused",
                "sections": ["header", "summary", "design_process", "experience", "education", "tools"],
                "features": ["design_process", "user_research", "prototype_links"]
            },
            
            "content_writer": {
                "id": "content_writer",
                "name": "Content Writer",
                "industry": "creative",
                "level": "junior-mid", 
                "description": "Editorial-style template for writers and content creators",
                "colors": {"primary": "#1f2937", "secondary": "#374151", "accent": "#6b7280", "text": "#1a202c", "background": "#ffffff"},
                "fonts": {"header": "'Playfair Display', serif", "body": "'Crimson Text', serif", "accent": "'Source Sans Pro', sans-serif"},
                "layout": "editorial",
                "sections": ["header", "summary", "writing_samples", "experience", "education", "publications"],
                "features": ["writing_samples", "publication_list", "editorial_style"]
            },
            
            # HEALTHCARE TEMPLATES
            "medical_doctor": {
                "id": "medical_doctor",
                "name": "Medical Doctor",
                "industry": "healthcare",
                "level": "senior",
                "description": "Professional medical template for physicians",
                "colors": COLOR_SCHEMES["healthcare"],
                "fonts": FONT_COMBINATIONS["professional"],
                "layout": "medical_professional",
                "sections": ["header", "summary", "specializations", "experience", "education", "publications", "licenses"],
                "features": ["medical_specializations", "publication_list", "license_tracker"]
            },
            
            "nurse_practitioner": {
                "id": "nurse_practitioner",
                "name": "Nurse Practitioner", 
                "industry": "healthcare",
                "level": "mid-senior",
                "description": "Caring professional template for nursing professionals",
                "colors": COLOR_SCHEMES["healthcare"],
                "fonts": FONT_COMBINATIONS["professional"],
                "layout": "healthcare_focused",
                "sections": ["header", "summary", "clinical_experience", "education", "certifications", "specialties"],
                "features": ["clinical_focus", "certification_badges", "patient_care"]
            },
            
            "healthcare_admin": {
                "id": "healthcare_admin",
                "name": "Healthcare Administrator",
                "industry": "healthcare",
                "level": "mid-senior",
                "description": "Administrative template for healthcare management",
                "colors": COLOR_SCHEMES["healthcare"],
                "fonts": FONT_COMBINATIONS["professional"], 
                "layout": "administrative",
                "sections": ["header", "summary", "management_experience", "education", "certifications", "achievements"],
                "features": ["management_focus", "healthcare_metrics", "administrative_skills"]
            },
            
            # FINANCE TEMPLATES
            "financial_analyst": {
                "id": "financial_analyst",
                "name": "Financial Analyst",
                "industry": "finance",
                "level": "junior-mid",
                "description": "Numbers-focused template for financial professionals",
                "colors": COLOR_SCHEMES["finance"],
                "fonts": FONT_COMBINATIONS["professional"],
                "layout": "analytical",
                "sections": ["header", "summary", "technical_skills", "experience", "education", "certifications"],
                "features": ["financial_metrics", "analytical_skills", "certification_focus"]
            },
            
            "investment_banker": {
                "id": "investment_banker",
                "name": "Investment Banker",
                "industry": "finance", 
                "level": "senior",
                "description": "High-finance template for investment banking",
                "colors": COLOR_SCHEMES["finance"],
                "fonts": FONT_COMBINATIONS["classic"],
                "layout": "executive_finance",
                "sections": ["header", "summary", "deal_experience", "education", "achievements", "licenses"],
                "features": ["deal_highlights", "transaction_focus", "prestige_layout"]
            },
            
            "accountant": {
                "id": "accountant",
                "name": "Accountant",
                "industry": "finance",
                "level": "mid",
                "description": "Professional accounting template with compliance focus",
                "colors": COLOR_SCHEMES["finance"],
                "fonts": FONT_COMBINATIONS["professional"],
                "layout": "compliance_focused",
                "sections": ["header", "summary", "expertise", "experience", "education", "certifications"],
                "features": ["compliance_focus", "cpa_highlight", "tax_expertise"]
            },
            
            # EDUCATION TEMPLATES  
            "teacher": {
                "id": "teacher",
                "name": "Teacher",
                "industry": "education",
                "level": "junior-mid",
                "description": "Educational template for teaching professionals",
                "colors": COLOR_SCHEMES["education"],
                "fonts": FONT_COMBINATIONS["professional"],
                "layout": "educational",
                "sections": ["header", "teaching_philosophy", "experience", "education", "certifications", "achievements"],
                "features": ["teaching_focus", "student_outcomes", "educational_approach"]
            },
            
            "academic_researcher": {
                "id": "academic_researcher",
                "name": "Academic Researcher",
                "industry": "education",
                "level": "senior",
                "description": "Research-focused template for academics",
                "colors": COLOR_SCHEMES["education"],
                "fonts": FONT_COMBINATIONS["classic"],
                "layout": "academic",
                "sections": ["header", "research_interests", "publications", "experience", "education", "grants"],
                "features": ["publication_list", "research_focus", "academic_achievements"]
            }
        }

def generate_template_css(template: Dict[str, Any]) -> str:
    """Generate CSS for a specific template"""
    colors = template["colors"]
    fonts = template["fonts"]
    
    css = f"""
    /* {template['name']} Template CSS */
    .template-{template['id']} {{
        font-family: {fonts['body']};
        color: {colors['text']};
        background-color: {colors['background']};
        line-height: 1.6;
    }}
    
    .template-{template['id']} .header {{
        background-color: {colors['primary']};
        color: {colors['background']};
        padding: 20px;
    }}
    
    .template-{template['id']} .header-name {{
        font-family: {fonts['header']};
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }}
    
    .template-{template['id']} .header-title {{
        font-size: 1.25rem;
        opacity: 0.9;
        margin-bottom: 1rem;
    }}
    
    .template-{template['id']} .section-title {{
        font-family: {fonts['accent']};
        color: {colors['primary']};
        font-size: 1.5rem;
        font-weight: 600;
        border-bottom: 2px solid {colors['primary']};
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    .template-{template['id']} .experience-item {{
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #e5e7eb;
    }}
    
    .template-{template['id']} .job-title {{
        font-size: 1.125rem;
        font-weight: 600;
        color: {colors['secondary']};
        margin-bottom: 0.25rem;
    }}
    
    .template-{template['id']} .company {{
        font-size: 1rem;
        color: {colors['primary']};
        font-weight: 500;
        margin-bottom: 0.5rem;
    }}
    
    .template-{template['id']} .achievement {{
        margin-bottom: 0.5rem;
        position: relative;
        padding-left: 1.5rem;
    }}
    
    .template-{template['id']} .achievement::before {{
        content: "•";
        color: {colors['accent']};
        font-weight: bold;
        position: absolute;
        left: 0;
    }}
    
    .template-{template['id']} .skills-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 0.75rem;
        margin-top: 1rem;
    }}
    
    .template-{template['id']} .skill-item {{
        background-color: {colors['accent']};
        color: {colors['background']};
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        text-align: center;
        font-size: 0.875rem;
        font-weight: 500;
    }}
    
    .template-{template['id']} .contact-info {{
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        justify-content: center;
        margin-top: 1rem;
    }}
    
    .template-{template['id']} .contact-item {{
        font-size: 0.875rem;
        opacity: 0.9;
    }}
    
    /* Layout-specific styles */
    {_get_layout_css(template)}
    
    /* Feature-specific styles */
    {_get_feature_css(template)}
    
    /* Print styles */
    @media print {{
        .template-{template['id']} {{
            print-color-adjust: exact;
            -webkit-print-color-adjust: exact;
        }}
    }}
    """
    
    return css

def _get_layout_css(template: Dict[str, Any]) -> str:
    """Get layout-specific CSS"""
    layout = template['layout']
    template_id = template['id']
    
    if layout == "two_column":
        return f"""
        .template-{template_id} .content {{
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 2rem;
        }}
        
        .template-{template_id} .sidebar {{
            background-color: #f9fafb;
            padding: 1.5rem;
            border-radius: 0.5rem;
        }}
        """
    
    elif layout == "portfolio_style":
        return f"""
        .template-{template_id} .portfolio-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }}
        
        .template-{template_id} .portfolio-item {{
            border-radius: 0.5rem;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        """
    
    else:  # single_column (default)
        return f"""
        .template-{template_id} .content {{
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }}
        """

def _get_feature_css(template: Dict[str, Any]) -> str:
    """Get feature-specific CSS"""
    features = template.get('features', [])
    template_id = template['id']
    colors = template['colors']
    
    css = ""
    
    if "skills_bars" in features:
        css += f"""
        .template-{template_id} .skill-bar {{
            margin-bottom: 1rem;
        }}
        
        .template-{template_id} .skill-bar-fill {{
            height: 8px;
            background-color: {colors['primary']};
            border-radius: 4px;
            transition: width 0.3s ease;
        }}
        """
    
    if "metrics_highlights" in features:
        css += f"""
        .template-{template_id} .metric {{
            display: inline-block;
            background-color: {colors['accent']};
            color: {colors['background']};
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-size: 0.875rem;
            font-weight: 600;
            margin-right: 0.5rem;
            margin-bottom: 0.5rem;
        }}
        """
    
    if "certification_badges" in features:
        css += f"""
        .template-{template_id} .certification {{
            display: inline-flex;
            align-items: center;
            background-color: {colors['secondary']};
            color: {colors['background']};
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            margin-right: 0.75rem;
            margin-bottom: 0.75rem;
            font-size: 0.875rem;
            font-weight: 500;
        }}
        
        .template-{template_id} .certification::before {{
            content: "✓";
            margin-right: 0.5rem;
            font-weight: bold;
        }}
        """
    
    return css

# Global template library instance
template_library = TemplateLibrary()
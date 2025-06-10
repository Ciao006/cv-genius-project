"""
Advanced ATS (Applicant Tracking System) Compatibility Service
Free and open-source ATS optimization and scoring system
"""

import re
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class ATSIssueType(Enum):
    FORMATTING = "formatting"
    KEYWORDS = "keywords"
    STRUCTURE = "structure"
    CONTENT = "content"
    PARSING = "parsing"

@dataclass
class ATSIssue:
    type: ATSIssueType
    severity: str  # critical, high, medium, low
    title: str
    description: str
    recommendation: str
    section: Optional[str] = None
    impact_score: int = 0  # 0-100

@dataclass
class ATSAnalysisResult:
    overall_score: int  # 0-100
    issues: List[ATSIssue]
    strengths: List[str]
    recommendations: List[str]
    keyword_analysis: Dict[str, Any]
    parsing_analysis: Dict[str, Any]
    compatibility_rating: str  # excellent, good, fair, poor

class ATSKeywordAnalyzer:
    """
    Analyzes keyword usage and density for ATS optimization
    """
    
    def __init__(self):
        # Common ATS keywords by category
        self.ats_friendly_keywords = {
            "action_verbs": [
                "achieved", "administered", "advised", "analyzed", "applied", "assigned",
                "attained", "chaired", "collaborated", "collected", "communicated", "completed",
                "composed", "computed", "conceived", "conducted", "constructed", "consulted",
                "coordinated", "created", "delegated", "demonstrated", "designed", "developed",
                "devised", "directed", "edited", "educated", "eliminated", "established",
                "evaluated", "executed", "facilitated", "generated", "guided", "identified",
                "implemented", "improved", "increased", "influenced", "initiated", "inspected",
                "installed", "instituted", "instructed", "interpreted", "interviewed", "introduced",
                "invented", "launched", "led", "maintained", "managed", "modified", "monitored",
                "motivated", "negotiated", "operated", "organized", "originated", "participated",
                "performed", "planned", "prepared", "presented", "prioritized", "processed",
                "produced", "programmed", "promoted", "proposed", "provided", "purchased",
                "recommended", "reduced", "reinforced", "reported", "researched", "resolved",
                "responded", "restored", "reviewed", "revised", "scheduled", "selected",
                "simplified", "solved", "streamlined", "strengthened", "supervised", "supported",
                "trained", "transformed", "updated", "upgraded", "utilized", "validated"
            ],
            "soft_skills": [
                "adaptable", "analytical", "articulate", "collaborative", "creative",
                "customer-focused", "detail-oriented", "efficient", "flexible", "innovative",
                "interpersonal", "leadership", "motivated", "organized", "problem-solving",
                "reliable", "resourceful", "results-driven", "strategic", "team-oriented"
            ],
            "measurement_words": [
                "percentage", "percent", "dollar", "revenue", "profit", "budget", "cost",
                "savings", "increase", "decrease", "improvement", "growth", "reduction",
                "efficiency", "productivity", "performance", "results", "outcomes", "metrics"
            ]
        }
        
        # Industry-specific critical keywords
        self.industry_critical_keywords = {
            "technology": [
                "software", "development", "programming", "coding", "database", "system",
                "application", "web", "mobile", "cloud", "api", "integration", "testing",
                "deployment", "agile", "scrum", "devops", "cybersecurity", "data", "analytics"
            ],
            "business": [
                "management", "strategy", "operations", "business", "corporate", "enterprise",
                "commercial", "sales", "marketing", "finance", "accounting", "administration",
                "procurement", "vendor", "client", "customer", "stakeholder", "roi", "kpi"
            ],
            "healthcare": [
                "patient", "clinical", "medical", "healthcare", "treatment", "diagnosis",
                "therapy", "care", "nursing", "hospital", "clinic", "health", "safety",
                "compliance", "regulation", "quality", "standards", "certification", "license"
            ],
            "finance": [
                "financial", "investment", "portfolio", "analysis", "risk", "compliance",
                "audit", "accounting", "banking", "trading", "markets", "securities",
                "derivatives", "valuation", "modeling", "forecasting", "budgeting", "reporting"
            ],
            "marketing": [
                "marketing", "brand", "campaign", "advertising", "promotion", "digital",
                "social", "content", "seo", "sem", "analytics", "conversion", "engagement",
                "acquisition", "retention", "segmentation", "targeting", "positioning"
            ]
        }
    
    def analyze_keywords(self, cv_data: Dict[str, Any], 
                        job_description: str = "", 
                        industry: str = "general") -> Dict[str, Any]:
        """Comprehensive keyword analysis for ATS optimization"""
        
        # Extract all text from CV
        cv_text = self._extract_all_text(cv_data)
        cv_text_lower = cv_text.lower()
        
        # Analyze different keyword categories
        action_verb_analysis = self._analyze_action_verbs(cv_text_lower)
        soft_skills_analysis = self._analyze_soft_skills(cv_text_lower)
        measurement_analysis = self._analyze_measurements(cv_text_lower)
        industry_analysis = self._analyze_industry_keywords(cv_text_lower, industry)
        
        # Job description matching (if provided)
        job_matching = {}
        if job_description:
            job_matching = self._analyze_job_description_match(cv_text_lower, job_description.lower())
        
        # Calculate keyword density and distribution
        density_analysis = self._calculate_keyword_density(cv_text, cv_data)
        
        # Generate keyword score
        keyword_score = self._calculate_keyword_score(
            action_verb_analysis, soft_skills_analysis, measurement_analysis,
            industry_analysis, job_matching, density_analysis
        )
        
        return {
            "overall_score": keyword_score,
            "action_verbs": action_verb_analysis,
            "soft_skills": soft_skills_analysis,
            "measurements": measurement_analysis,
            "industry_keywords": industry_analysis,
            "job_matching": job_matching,
            "density_analysis": density_analysis,
            "recommendations": self._generate_keyword_recommendations(
                cv_text_lower, action_verb_analysis, soft_skills_analysis,
                measurement_analysis, industry_analysis, job_matching
            )
        }
    
    def _extract_all_text(self, cv_data: Dict[str, Any]) -> str:
        """Extract all text content from CV data"""
        text_parts = []
        
        # Personal details
        if "personal_details" in cv_data:
            personal = cv_data["personal_details"]
            text_parts.extend([
                personal.get("full_name", ""),
                personal.get("desired_position", "")
            ])
        
        # Professional summary
        if "professional_summary" in cv_data:
            text_parts.append(cv_data["professional_summary"])
        
        # Work experience
        if "work_experience" in cv_data:
            for exp in cv_data["work_experience"]:
                text_parts.extend([
                    exp.get("job_title", ""),
                    exp.get("company", ""),
                    " ".join(exp.get("achievements", []))
                ])
        
        # Education
        if "education" in cv_data:
            for edu in cv_data["education"]:
                text_parts.extend([
                    edu.get("degree", ""),
                    edu.get("institution", "")
                ])
        
        # Skills
        if "skills" in cv_data and isinstance(cv_data["skills"], dict):
            for skill_list in cv_data["skills"].values():
                if isinstance(skill_list, list):
                    text_parts.extend(skill_list)
        
        return " ".join([part for part in text_parts if part])
    
    def _analyze_action_verbs(self, text: str) -> Dict[str, Any]:
        """Analyze action verb usage"""
        action_verbs = self.ats_friendly_keywords["action_verbs"]
        found_verbs = []
        
        for verb in action_verbs:
            if verb in text:
                found_verbs.append(verb)
        
        return {
            "count": len(found_verbs),
            "found_verbs": found_verbs[:10],  # Top 10
            "percentage": round((len(found_verbs) / len(action_verbs)) * 100, 1),
            "score": min(100, len(found_verbs) * 2)  # 2 points per verb, max 100
        }
    
    def _analyze_soft_skills(self, text: str) -> Dict[str, Any]:
        """Analyze soft skills keywords"""
        soft_skills = self.ats_friendly_keywords["soft_skills"]
        found_skills = []
        
        for skill in soft_skills:
            if skill.replace("-", " ") in text or skill.replace("-", "-") in text:
                found_skills.append(skill)
        
        return {
            "count": len(found_skills),
            "found_skills": found_skills,
            "percentage": round((len(found_skills) / len(soft_skills)) * 100, 1),
            "score": min(100, len(found_skills) * 5)  # 5 points per skill, max 100
        }
    
    def _analyze_measurements(self, text: str) -> Dict[str, Any]:
        """Analyze quantitative measurements and metrics"""
        measurement_patterns = [
            r'\d+%',  # percentages
            r'\$[\d,]+',  # dollar amounts
            r'\d+[kKmMbB]',  # thousands/millions/billions
            r'\d+\+?\s*(?:years?|months?)',  # time periods
            r'\d+\+?\s*(?:people|members|employees|users|customers)',  # quantities
            r'\d+\+?\s*(?:projects?|initiatives?|campaigns?)',  # project counts
            r'increased?\s+by\s+\d+',  # increase patterns
            r'reduced?\s+by\s+\d+',  # reduction patterns
            r'improved?\s+by\s+\d+',  # improvement patterns
        ]
        
        found_measurements = []
        for pattern in measurement_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            found_measurements.extend(matches)
        
        measurement_words = self.ats_friendly_keywords["measurement_words"]
        found_measurement_words = [word for word in measurement_words if word in text]
        
        return {
            "metric_count": len(found_measurements),
            "found_metrics": found_measurements[:10],  # Top 10
            "measurement_words": found_measurement_words,
            "score": min(100, len(found_measurements) * 10 + len(found_measurement_words) * 3)
        }
    
    def _analyze_industry_keywords(self, text: str, industry: str) -> Dict[str, Any]:
        """Analyze industry-specific keywords"""
        if industry not in self.industry_critical_keywords:
            return {
                "count": 0,
                "found_keywords": [],
                "score": 50,  # Neutral score for unknown industry
                "coverage": 0
            }
        
        industry_keywords = self.industry_critical_keywords[industry]
        found_keywords = []
        
        for keyword in industry_keywords:
            if keyword in text:
                found_keywords.append(keyword)
        
        coverage = (len(found_keywords) / len(industry_keywords)) * 100
        
        return {
            "count": len(found_keywords),
            "found_keywords": found_keywords,
            "total_keywords": len(industry_keywords),
            "coverage": round(coverage, 1),
            "score": min(100, coverage * 2)  # 2x coverage percentage
        }
    
    def _analyze_job_description_match(self, cv_text: str, job_description: str) -> Dict[str, Any]:
        """Analyze how well CV matches job description keywords"""
        if not job_description:
            return {}
        
        # Extract meaningful keywords from job description
        job_keywords = self._extract_job_keywords(job_description)
        
        # Find matches in CV
        matched_keywords = []
        missing_keywords = []
        
        for keyword in job_keywords:
            if keyword.lower() in cv_text:
                matched_keywords.append(keyword)
            else:
                missing_keywords.append(keyword)
        
        match_percentage = (len(matched_keywords) / len(job_keywords)) * 100 if job_keywords else 0
        
        return {
            "job_keywords": job_keywords,
            "matched_keywords": matched_keywords,
            "missing_keywords": missing_keywords[:10],  # Top 10 missing
            "match_percentage": round(match_percentage, 1),
            "score": min(100, match_percentage)
        }
    
    def _extract_job_keywords(self, job_description: str) -> List[str]:
        """Extract important keywords from job description"""
        # Remove common words
        common_words = {
            "the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with",
            "by", "from", "up", "about", "into", "through", "during", "before",
            "after", "above", "below", "between", "among", "this", "that", "these",
            "those", "you", "your", "we", "our", "will", "be", "have", "has",
            "had", "do", "does", "did", "can", "could", "should", "would", "may",
            "might", "must", "shall", "a", "an", "is", "are", "was", "were"
        }
        
        # Extract words and phrases
        words = re.findall(r'\b[a-zA-Z]+\b', job_description.lower())
        
        # Filter meaningful keywords
        keywords = []
        for word in words:
            if (len(word) > 3 and 
                word not in common_words and
                word not in keywords):
                keywords.append(word)
        
        # Extract important phrases (2-3 words)
        phrases = re.findall(r'\b[A-Za-z]+\s+[A-Za-z]+(?:\s+[A-Za-z]+)?\b', job_description)
        
        # Filter and add important phrases
        for phrase in phrases[:20]:  # Limit to top 20 phrases
            phrase_lower = phrase.lower()
            if (len(phrase_lower) > 8 and
                not any(common in phrase_lower for common in common_words) and
                phrase_lower not in [k.lower() for k in keywords]):
                keywords.append(phrase)
        
        return keywords[:30]  # Return top 30 keywords/phrases
    
    def _calculate_keyword_density(self, text: str, cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate keyword density and distribution across sections"""
        words = text.split()
        total_words = len(words)
        
        # Calculate density by section
        section_densities = {}
        
        sections = {
            "summary": cv_data.get("professional_summary", ""),
            "experience": " ".join([
                " ".join(exp.get("achievements", [])) 
                for exp in cv_data.get("work_experience", [])
            ]),
            "skills": " ".join([
                " ".join(skills) if isinstance(skills, list) else str(skills)
                for skills in cv_data.get("skills", {}).values()
            ])
        }
        
        for section_name, section_text in sections.items():
            if section_text:
                section_words = len(section_text.split())
                section_densities[section_name] = {
                    "word_count": section_words,
                    "percentage": round((section_words / total_words) * 100, 1) if total_words > 0 else 0
                }
        
        return {
            "total_words": total_words,
            "section_distribution": section_densities,
            "recommended_length": self._get_recommended_length(total_words)
        }
    
    def _get_recommended_length(self, current_words: int) -> Dict[str, Any]:
        """Get recommendations for CV length"""
        optimal_range = (400, 800)  # Optimal word count range
        
        if current_words < optimal_range[0]:
            return {
                "status": "too_short",
                "message": f"CV is too short ({current_words} words). Aim for {optimal_range[0]}-{optimal_range[1]} words.",
                "recommendation": "Add more details to your achievements and experience"
            }
        elif current_words > optimal_range[1]:
            return {
                "status": "too_long", 
                "message": f"CV is too long ({current_words} words). Aim for {optimal_range[0]}-{optimal_range[1]} words.",
                "recommendation": "Condense content and focus on most relevant achievements"
            }
        else:
            return {
                "status": "optimal",
                "message": f"CV length is optimal ({current_words} words)",
                "recommendation": "Maintain current length while optimizing content quality"
            }
    
    def _calculate_keyword_score(self, action_verbs: Dict, soft_skills: Dict, 
                                measurements: Dict, industry: Dict, 
                                job_matching: Dict, density: Dict) -> int:
        """Calculate overall keyword optimization score"""
        scores = []
        weights = []
        
        # Action verbs (25% weight)
        scores.append(action_verbs["score"])
        weights.append(0.25)
        
        # Soft skills (15% weight)
        scores.append(soft_skills["score"])
        weights.append(0.15)
        
        # Measurements (20% weight)
        scores.append(measurements["score"])
        weights.append(0.20)
        
        # Industry keywords (25% weight)
        scores.append(industry["score"])
        weights.append(0.25)
        
        # Job matching (15% weight, if available)
        if job_matching:
            scores.append(job_matching["score"])
            weights.append(0.15)
        else:
            # Redistribute weight
            weights = [w * 1.15 for w in weights]
        
        # Calculate weighted average
        weighted_score = sum(score * weight for score, weight in zip(scores, weights))
        return int(weighted_score)
    
    def _generate_keyword_recommendations(self, cv_text: str, action_verbs: Dict,
                                        soft_skills: Dict, measurements: Dict,
                                        industry: Dict, job_matching: Dict) -> List[str]:
        """Generate specific keyword optimization recommendations"""
        recommendations = []
        
        # Action verb recommendations
        if action_verbs["score"] < 60:
            recommendations.append(
                f"Add more action verbs. Currently using {action_verbs['count']} - aim for 15-20 strong action verbs."
            )
        
        # Soft skills recommendations
        if soft_skills["score"] < 40:
            recommendations.append(
                "Include more soft skills keywords relevant to your field (e.g., 'leadership', 'analytical', 'team-oriented')."
            )
        
        # Measurement recommendations
        if measurements["score"] < 50:
            recommendations.append(
                "Add quantifiable metrics to your achievements (percentages, dollar amounts, team sizes, timeframes)."
            )
        
        # Industry keyword recommendations
        if industry["score"] < 70:
            recommendations.append(
                f"Increase industry-specific keyword usage. Current coverage: {industry.get('coverage', 0)}%"
            )
        
        # Job matching recommendations
        if job_matching and job_matching["score"] < 70:
            missing = job_matching.get("missing_keywords", [])[:5]
            recommendations.append(
                f"Add job-specific keywords: {', '.join(missing)}"
            )
        
        return recommendations

class ATSFormatAnalyzer:
    """
    Analyzes CV formatting for ATS compatibility
    """
    
    def analyze_format(self, cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze formatting issues that might affect ATS parsing"""
        issues = []
        formatting_score = 100
        
        # Check section structure
        structure_analysis = self._analyze_section_structure(cv_data)
        issues.extend(structure_analysis["issues"])
        formatting_score -= structure_analysis["penalty"]
        
        # Check contact information format
        contact_analysis = self._analyze_contact_format(cv_data.get("personal_details", {}))
        issues.extend(contact_analysis["issues"])
        formatting_score -= contact_analysis["penalty"]
        
        # Check date formats
        date_analysis = self._analyze_date_formats(cv_data)
        issues.extend(date_analysis["issues"])
        formatting_score -= date_analysis["penalty"]
        
        # Check content organization
        organization_analysis = self._analyze_content_organization(cv_data)
        issues.extend(organization_analysis["issues"])
        formatting_score -= organization_analysis["penalty"]
        
        return {
            "score": max(0, formatting_score),
            "issues": issues,
            "recommendations": self._generate_format_recommendations(issues)
        }
    
    def _analyze_section_structure(self, cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze CV section structure for ATS compatibility"""
        issues = []
        penalty = 0
        
        # Required sections
        required_sections = ["personal_details", "work_experience"]
        recommended_sections = ["professional_summary", "education", "skills"]
        
        for section in required_sections:
            if section not in cv_data or not cv_data[section]:
                issues.append(f"Missing required section: {section}")
                penalty += 20
        
        for section in recommended_sections:
            if section not in cv_data or not cv_data[section]:
                issues.append(f"Missing recommended section: {section}")
                penalty += 10
        
        # Check section order (experience should come before education for experienced professionals)
        if "work_experience" in cv_data and "education" in cv_data:
            work_exp = cv_data["work_experience"]
            if work_exp and len(work_exp) > 0:
                # For experienced professionals, work experience should be prominent
                pass  # Structure seems appropriate
        
        return {"issues": issues, "penalty": penalty}
    
    def _analyze_contact_format(self, personal_details: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze contact information formatting"""
        issues = []
        penalty = 0
        
        # Check email format
        email = personal_details.get("email", "")
        if email:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                issues.append("Email format may not parse correctly")
                penalty += 5
        else:
            issues.append("Missing email address")
            penalty += 15
        
        # Check phone format
        phone = personal_details.get("phone", "")
        if phone:
            # Remove common formatting and check for reasonable length
            phone_digits = re.sub(r'[^\d]', '', phone)
            if len(phone_digits) < 10 or len(phone_digits) > 15:
                issues.append("Phone number format may not parse correctly")
                penalty += 5
        else:
            issues.append("Missing phone number")
            penalty += 15
        
        # Check name format
        name = personal_details.get("full_name", "")
        if not name:
            issues.append("Missing full name")
            penalty += 20
        elif len(name.split()) < 2:
            issues.append("Full name should include first and last name")
            penalty += 5
        
        return {"issues": issues, "penalty": penalty}
    
    def _analyze_date_formats(self, cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze date formatting consistency"""
        issues = []
        penalty = 0
        
        all_dates = []
        
        # Collect dates from work experience
        if "work_experience" in cv_data:
            for exp in cv_data["work_experience"]:
                if "start_date" in exp:
                    all_dates.append(exp["start_date"])
                if "end_date" in exp:
                    all_dates.append(exp["end_date"])
        
        # Collect dates from education
        if "education" in cv_data:
            for edu in cv_data["education"]:
                if "start_date" in edu:
                    all_dates.append(edu["start_date"])
                if "end_date" in edu:
                    all_dates.append(edu["end_date"])
        
        # Check date format consistency
        date_formats = []
        for date_str in all_dates:
            if date_str and date_str.lower() != "present":
                # Identify date format
                if re.match(r'^\d{4}$', date_str):
                    date_formats.append("YYYY")
                elif re.match(r'^\d{1,2}/\d{4}$', date_str):
                    date_formats.append("MM/YYYY")
                elif re.match(r'^\w{3,9}\s+\d{4}$', date_str):
                    date_formats.append("Month YYYY")
                else:
                    date_formats.append("Other")
        
        # Check for consistency
        unique_formats = set(date_formats)
        if len(unique_formats) > 2:
            issues.append("Inconsistent date formats across CV")
            penalty += 10
        
        return {"issues": issues, "penalty": penalty}
    
    def _analyze_content_organization(self, cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content organization and structure"""
        issues = []
        penalty = 0
        
        # Check work experience organization
        if "work_experience" in cv_data:
            work_exp = cv_data["work_experience"]
            if work_exp:
                # Check if experiences are in reverse chronological order
                # This is a simplified check - in reality, you'd need to parse dates properly
                
                # Check for missing job titles or companies
                for i, exp in enumerate(work_exp):
                    if not exp.get("job_title"):
                        issues.append(f"Missing job title in experience entry {i+1}")
                        penalty += 10
                    
                    if not exp.get("company"):
                        issues.append(f"Missing company name in experience entry {i+1}")
                        penalty += 10
                    
                    # Check for achievement bullets
                    achievements = exp.get("achievements", [])
                    if not achievements:
                        issues.append(f"No achievements listed for {exp.get('job_title', 'position')}")
                        penalty += 5
                    elif len(achievements) < 2:
                        issues.append(f"Too few achievements listed for {exp.get('job_title', 'position')}")
                        penalty += 3
        
        # Check education section
        if "education" in cv_data:
            education = cv_data["education"]
            if education:
                for i, edu in enumerate(education):
                    if not edu.get("degree"):
                        issues.append(f"Missing degree in education entry {i+1}")
                        penalty += 8
                    
                    if not edu.get("institution"):
                        issues.append(f"Missing institution in education entry {i+1}")
                        penalty += 8
        
        return {"issues": issues, "penalty": penalty}
    
    def _generate_format_recommendations(self, issues: List[str]) -> List[str]:
        """Generate formatting recommendations based on identified issues"""
        recommendations = []
        
        if any("Missing" in issue for issue in issues):
            recommendations.append("Ensure all required sections and fields are completed")
        
        if any("format" in issue.lower() for issue in issues):
            recommendations.append("Use consistent formatting throughout your CV")
        
        if any("date" in issue.lower() for issue in issues):
            recommendations.append("Use consistent date format (recommended: MM/YYYY)")
        
        if any("achievement" in issue.lower() for issue in issues):
            recommendations.append("Add 3-5 achievement bullet points for each position")
        
        # General ATS formatting recommendations
        recommendations.extend([
            "Use standard section headings (Experience, Education, Skills)",
            "Avoid tables, text boxes, and complex formatting",
            "Use simple bullet points for lists",
            "Ensure consistent font and formatting",
            "Save and submit as PDF or Word document"
        ])
        
        return list(set(recommendations))  # Remove duplicates

class ATSService:
    """
    Main ATS compatibility service
    """
    
    def __init__(self):
        self.keyword_analyzer = ATSKeywordAnalyzer()
        self.format_analyzer = ATSFormatAnalyzer()
    
    def analyze_ats_compatibility(self, cv_data: Dict[str, Any], 
                                 job_description: str = "",
                                 industry: str = "general") -> ATSAnalysisResult:
        """Comprehensive ATS compatibility analysis"""
        
        # Keyword analysis
        keyword_analysis = self.keyword_analyzer.analyze_keywords(cv_data, job_description, industry)
        
        # Format analysis
        format_analysis = self.format_analyzer.analyze_format(cv_data)
        
        # Parsing simulation
        parsing_analysis = self._simulate_ats_parsing(cv_data)
        
        # Combine analyses
        overall_score = self._calculate_overall_score(
            keyword_analysis["overall_score"],
            format_analysis["score"],
            parsing_analysis["score"]
        )
        
        # Generate issues
        issues = self._consolidate_issues(keyword_analysis, format_analysis, parsing_analysis)
        
        # Generate recommendations
        recommendations = self._generate_comprehensive_recommendations(
            keyword_analysis, format_analysis, parsing_analysis
        )
        
        # Identify strengths
        strengths = self._identify_ats_strengths(keyword_analysis, format_analysis)
        
        # Determine compatibility rating
        compatibility_rating = self._get_compatibility_rating(overall_score)
        
        return ATSAnalysisResult(
            overall_score=overall_score,
            issues=issues,
            strengths=strengths,
            recommendations=recommendations,
            keyword_analysis=keyword_analysis,
            parsing_analysis=parsing_analysis,
            compatibility_rating=compatibility_rating
        )
    
    def _simulate_ats_parsing(self, cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate how an ATS would parse the CV"""
        parsing_score = 100
        issues = []
        
        # Check if key information is easily extractable
        
        # Name extraction
        personal_details = cv_data.get("personal_details", {})
        if not personal_details.get("full_name"):
            parsing_score -= 20
            issues.append("Name may not be parsed correctly")
        
        # Contact information extraction
        if not personal_details.get("email"):
            parsing_score -= 15
            issues.append("Email may not be parsed correctly")
        
        if not personal_details.get("phone"):
            parsing_score -= 15
            issues.append("Phone number may not be parsed correctly")
        
        # Work experience extraction
        work_exp = cv_data.get("work_experience", [])
        if not work_exp:
            parsing_score -= 25
            issues.append("No work experience found")
        else:
            for exp in work_exp:
                if not exp.get("job_title"):
                    parsing_score -= 10
                    issues.append("Job title may not be parsed correctly")
                if not exp.get("company"):
                    parsing_score -= 10
                    issues.append("Company name may not be parsed correctly")
        
        # Skills extraction
        skills = cv_data.get("skills", {})
        if not skills:
            parsing_score -= 15
            issues.append("Skills section may not be parsed correctly")
        
        # Education extraction
        education = cv_data.get("education", [])
        if not education:
            parsing_score -= 10
            issues.append("Education information may not be parsed correctly")
        
        return {
            "score": max(0, parsing_score),
            "issues": issues,
            "extractable_fields": self._count_extractable_fields(cv_data)
        }
    
    def _count_extractable_fields(self, cv_data: Dict[str, Any]) -> Dict[str, int]:
        """Count how many fields can be easily extracted by ATS"""
        extractable = {
            "personal_info": 0,
            "work_experience": 0,
            "education": 0,
            "skills": 0
        }
        
        # Personal info
        personal = cv_data.get("personal_details", {})
        if personal.get("full_name"): extractable["personal_info"] += 1
        if personal.get("email"): extractable["personal_info"] += 1
        if personal.get("phone"): extractable["personal_info"] += 1
        if personal.get("location"): extractable["personal_info"] += 1
        
        # Work experience
        for exp in cv_data.get("work_experience", []):
            if exp.get("job_title"): extractable["work_experience"] += 1
            if exp.get("company"): extractable["work_experience"] += 1
            if exp.get("start_date"): extractable["work_experience"] += 1
        
        # Education
        for edu in cv_data.get("education", []):
            if edu.get("degree"): extractable["education"] += 1
            if edu.get("institution"): extractable["education"] += 1
        
        # Skills
        skills = cv_data.get("skills", {})
        if isinstance(skills, dict):
            for skill_list in skills.values():
                if isinstance(skill_list, list):
                    extractable["skills"] += len(skill_list)
        
        return extractable
    
    def _calculate_overall_score(self, keyword_score: int, format_score: int, parsing_score: int) -> int:
        """Calculate overall ATS compatibility score"""
        # Weighted average: keywords (40%), format (35%), parsing (25%)
        weights = [0.4, 0.35, 0.25]
        scores = [keyword_score, format_score, parsing_score]
        
        overall = sum(score * weight for score, weight in zip(scores, weights))
        return int(overall)
    
    def _consolidate_issues(self, keyword_analysis: Dict, format_analysis: Dict, 
                          parsing_analysis: Dict) -> List[ATSIssue]:
        """Consolidate issues from all analyses"""
        issues = []
        
        # Keyword issues
        if keyword_analysis["overall_score"] < 70:
            issues.append(ATSIssue(
                type=ATSIssueType.KEYWORDS,
                severity="high",
                title="Low Keyword Optimization",
                description="Your CV lacks important keywords that ATS systems look for",
                recommendation="Add more industry-relevant keywords and action verbs",
                impact_score=30 - (keyword_analysis["overall_score"] // 3)
            ))
        
        # Format issues
        for issue_text in format_analysis.get("issues", []):
            severity = "high" if "Missing required" in issue_text else "medium"
            issues.append(ATSIssue(
                type=ATSIssueType.FORMATTING,
                severity=severity,
                title="Formatting Issue",
                description=issue_text,
                recommendation="Fix formatting to improve ATS parsing",
                impact_score=15 if severity == "high" else 10
            ))
        
        # Parsing issues
        for issue_text in parsing_analysis.get("issues", []):
            issues.append(ATSIssue(
                type=ATSIssueType.PARSING,
                severity="medium",
                title="Parsing Issue",
                description=issue_text,
                recommendation="Ensure information is clearly structured for ATS parsing",
                impact_score=12
            ))
        
        return issues
    
    def _generate_comprehensive_recommendations(self, keyword_analysis: Dict, 
                                              format_analysis: Dict,
                                              parsing_analysis: Dict) -> List[str]:
        """Generate comprehensive ATS optimization recommendations"""
        recommendations = []
        
        # Keyword recommendations
        recommendations.extend(keyword_analysis.get("recommendations", []))
        
        # Format recommendations
        recommendations.extend(format_analysis.get("recommendations", []))
        
        # General ATS best practices
        general_recommendations = [
            "Use a simple, clean format with standard fonts",
            "Include relevant keywords naturally throughout your CV", 
            "Use standard section headings (Summary, Experience, Education, Skills)",
            "Quantify your achievements with specific numbers and metrics",
            "Tailor your CV to each job application",
            "Use consistent formatting for dates and contact information",
            "Avoid graphics, images, and complex layouts",
            "Submit your CV in PDF or Word format"
        ]
        
        recommendations.extend(general_recommendations)
        
        # Remove duplicates and return
        return list(set(recommendations))
    
    def _identify_ats_strengths(self, keyword_analysis: Dict, format_analysis: Dict) -> List[str]:
        """Identify ATS compatibility strengths"""
        strengths = []
        
        # Keyword strengths
        if keyword_analysis["action_verbs"]["score"] > 70:
            strengths.append("Good use of action verbs")
        
        if keyword_analysis["measurements"]["score"] > 60:
            strengths.append("Includes quantifiable metrics")
        
        if keyword_analysis["industry_keywords"]["score"] > 70:
            strengths.append("Strong industry keyword usage")
        
        # Format strengths
        if format_analysis["score"] > 80:
            strengths.append("Well-structured and organized")
        
        # General strengths
        if not strengths:
            strengths.append("CV follows basic ATS-friendly structure")
        
        return strengths
    
    def _get_compatibility_rating(self, score: int) -> str:
        """Get compatibility rating based on score"""
        if score >= 90:
            return "excellent"
        elif score >= 75:
            return "good"
        elif score >= 60:
            return "fair"
        else:
            return "poor"

# Global service instance
ats_service = ATSService()
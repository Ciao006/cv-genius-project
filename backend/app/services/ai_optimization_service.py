"""
AI-Powered Content Optimization Engine
Free and open-source CV content enhancement using multiple AI providers
"""

import re
import json
import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import httpx

logger = logging.getLogger(__name__)

class OptimizationType(Enum):
    GRAMMAR = "grammar"
    CLARITY = "clarity"
    IMPACT = "impact"
    ATS_KEYWORDS = "ats_keywords"
    QUANTIFICATION = "quantification"
    ACTION_VERBS = "action_verbs"
    INDUSTRY_TERMS = "industry_terms"

@dataclass
class OptimizationSuggestion:
    type: OptimizationType
    original_text: str
    suggested_text: str
    confidence: float
    explanation: str
    section: str
    priority: str  # high, medium, low

@dataclass
class ContentAnalysis:
    score: int  # 0-100
    suggestions: List[OptimizationSuggestion]
    metrics: Dict[str, Any]
    strengths: List[str]
    weaknesses: List[str]

class IndustryKeywordDatabase:
    """
    Comprehensive industry keyword database for ATS optimization
    """
    
    def __init__(self):
        self.keywords = {
            "technology": {
                "programming": [
                    "JavaScript", "Python", "Java", "React", "Node.js", "Angular", "Vue.js",
                    "TypeScript", "PHP", "Ruby", "Go", "Rust", "Swift", "Kotlin", "C++", "C#"
                ],
                "frameworks": [
                    "Django", "Flask", "Spring", "Express", "Laravel", "Rails", "ASP.NET",
                    "React Native", "Flutter", "Xamarin", "Bootstrap", "Tailwind"
                ],
                "databases": [
                    "MySQL", "PostgreSQL", "MongoDB", "Redis", "Cassandra", "DynamoDB",
                    "Oracle", "SQL Server", "SQLite", "Neo4j", "Elasticsearch"
                ],
                "cloud": [
                    "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Jenkins",
                    "Terraform", "Ansible", "Serverless", "Microservices", "DevOps"
                ],
                "methodologies": [
                    "Agile", "Scrum", "Kanban", "TDD", "CI/CD", "Git", "SOLID", "REST API",
                    "GraphQL", "Machine Learning", "AI", "Data Science", "Big Data"
                ]
            },
            "business": {
                "management": [
                    "Strategic Planning", "Team Leadership", "Project Management", "Budget Management",
                    "Performance Management", "Change Management", "Risk Management", "Stakeholder Management"
                ],
                "marketing": [
                    "Digital Marketing", "SEO", "SEM", "Social Media", "Content Marketing",
                    "Email Marketing", "Analytics", "CRM", "Lead Generation", "Brand Management"
                ],
                "sales": [
                    "B2B Sales", "B2C Sales", "CRM", "Salesforce", "Lead Qualification",
                    "Pipeline Management", "Account Management", "Customer Retention", "Negotiation"
                ],
                "finance": [
                    "Financial Analysis", "Budgeting", "Forecasting", "Financial Modeling",
                    "Excel", "SAP", "QuickBooks", "P&L", "ROI", "KPI", "Variance Analysis"
                ]
            },
            "healthcare": {
                "clinical": [
                    "Patient Care", "Clinical Assessment", "Medical Records", "HIPAA",
                    "Electronic Health Records", "Evidence-Based Practice", "Patient Safety",
                    "Quality Improvement", "Infection Control", "Medication Administration"
                ],
                "specialties": [
                    "Emergency Medicine", "Critical Care", "Pediatrics", "Cardiology",
                    "Oncology", "Orthopedics", "Neurology", "Psychiatry", "Radiology"
                ],
                "certifications": [
                    "BLS", "ACLS", "PALS", "CNA", "RN", "NP", "MD", "DO", "PA",
                    "Licensed", "Board Certified", "Fellowship Trained"
                ]
            },
            "creative": {
                "design": [
                    "Adobe Creative Suite", "Photoshop", "Illustrator", "InDesign", "Figma",
                    "Sketch", "UI/UX Design", "User Experience", "User Interface", "Wireframing",
                    "Prototyping", "Brand Identity", "Typography", "Color Theory"
                ],
                "content": [
                    "Content Creation", "Copywriting", "Editorial", "SEO Writing",
                    "Social Media Content", "Blog Writing", "Technical Writing",
                    "Creative Writing", "Proofreading", "Content Strategy"
                ]
            },
            "finance": {
                "analysis": [
                    "Financial Analysis", "Financial Modeling", "Valuation", "DCF",
                    "Excel", "SQL", "Python", "R", "Bloomberg", "Reuters", "Capital Markets"
                ],
                "accounting": [
                    "GAAP", "IFRS", "Financial Statements", "Audit", "Tax", "QuickBooks",
                    "SAP", "Oracle", "CPA", "Financial Reporting", "Reconciliation"
                ],
                "investment": [
                    "Investment Banking", "Private Equity", "Hedge Funds", "Asset Management",
                    "Portfolio Management", "Risk Management", "Derivatives", "Fixed Income"
                ]
            }
        }
        
        self.action_verbs = {
            "leadership": [
                "Led", "Managed", "Directed", "Supervised", "Coordinated", "Guided",
                "Mentored", "Facilitated", "Orchestrated", "Spearheaded", "Championed"
            ],
            "achievement": [
                "Achieved", "Exceeded", "Improved", "Increased", "Enhanced", "Optimized",
                "Delivered", "Accomplished", "Surpassed", "Maximized", "Streamlined"
            ],
            "creation": [
                "Developed", "Created", "Built", "Designed", "Implemented", "Established",
                "Launched", "Initiated", "Pioneered", "Founded", "Engineered"
            ],
            "analysis": [
                "Analyzed", "Evaluated", "Assessed", "Researched", "Investigated",
                "Examined", "Identified", "Diagnosed", "Audited", "Reviewed"
            ],
            "communication": [
                "Presented", "Communicated", "Negotiated", "Collaborated", "Consulted",
                "Advised", "Trained", "Educated", "Influenced", "Persuaded"
            ]
        }
    
    def get_keywords_for_industry(self, industry: str) -> List[str]:
        """Get all keywords for a specific industry"""
        if industry not in self.keywords:
            return []
        
        all_keywords = []
        for category in self.keywords[industry].values():
            all_keywords.extend(category)
        return all_keywords
    
    def get_action_verbs(self, category: Optional[str] = None) -> List[str]:
        """Get action verbs, optionally filtered by category"""
        if category and category in self.action_verbs:
            return self.action_verbs[category]
        
        all_verbs = []
        for verbs in self.action_verbs.values():
            all_verbs.extend(verbs)
        return all_verbs

class ContentAnalyzer:
    """
    Advanced content analysis using NLP and pattern matching
    """
    
    def __init__(self):
        self.keyword_db = IndustryKeywordDatabase()
        
        # Weak phrases to avoid
        self.weak_phrases = {
            "responsible for": "Led/Managed",
            "worked on": "Developed/Created", 
            "helped with": "Contributed to",
            "in charge of": "Directed/Oversaw",
            "duties included": "Accomplished/Delivered",
            "was part of": "Collaborated on",
            "assisted with": "Supported/Facilitated",
            "involved in": "Participated in",
            "familiar with": "Experienced in",
            "knowledge of": "Skilled in"
        }
        
        # Metrics patterns
        self.metric_patterns = [
            r'\d+%',  # percentages
            r'\$[\d,]+',  # dollar amounts
            r'\d+[kKmMbB]',  # thousands/millions/billions
            r'\d+\+?\s*(?:years?|months?)',  # time periods
            r'\d+\+?\s*(?:people|members|employees)',  # team sizes
            r'\d+\+?\s*(?:projects?|initiatives?|campaigns?)',  # quantities
        ]
    
    def analyze_content(self, text: str, section: str, industry: str = "general") -> ContentAnalysis:
        """Comprehensive content analysis"""
        suggestions = []
        metrics = {}
        
        # Grammar and clarity analysis
        grammar_suggestions = self._check_grammar_and_clarity(text, section)
        suggestions.extend(grammar_suggestions)
        
        # Action verb analysis
        action_verb_suggestions = self._analyze_action_verbs(text, section)
        suggestions.extend(action_verb_suggestions)
        
        # Quantification analysis
        quantification_suggestions = self._analyze_quantification(text, section)
        suggestions.extend(quantification_suggestions)
        
        # Industry keyword analysis
        keyword_suggestions = self._analyze_keywords(text, section, industry)
        suggestions.extend(keyword_suggestions)
        
        # Impact analysis
        impact_suggestions = self._analyze_impact(text, section)
        suggestions.extend(impact_suggestions)
        
        # Calculate metrics
        metrics = self._calculate_metrics(text, industry)
        
        # Generate overall score
        score = self._calculate_score(suggestions, metrics)
        
        # Identify strengths and weaknesses
        strengths, weaknesses = self._identify_strengths_weaknesses(text, suggestions, metrics)
        
        return ContentAnalysis(
            score=score,
            suggestions=suggestions,
            metrics=metrics,
            strengths=strengths,
            weaknesses=weaknesses
        )
    
    def _check_grammar_and_clarity(self, text: str, section: str) -> List[OptimizationSuggestion]:
        """Check for grammar issues and clarity improvements"""
        suggestions = []
        
        # Check for weak phrases
        for weak, strong in self.weak_phrases.items():
            if weak.lower() in text.lower():
                suggestions.append(OptimizationSuggestion(
                    type=OptimizationType.CLARITY,
                    original_text=weak,
                    suggested_text=strong,
                    confidence=0.9,
                    explanation=f"Replace weak phrase '{weak}' with stronger alternative '{strong}'",
                    section=section,
                    priority="high"
                ))
        
        # Check for passive voice
        passive_patterns = [
            r'\bwas\s+\w+ed\b',
            r'\bwere\s+\w+ed\b',
            r'\bbeen\s+\w+ed\b'
        ]
        
        for pattern in passive_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                suggestions.append(OptimizationSuggestion(
                    type=OptimizationType.CLARITY,
                    original_text="passive voice detected",
                    suggested_text="use active voice",
                    confidence=0.8,
                    explanation="Convert passive voice to active voice for stronger impact",
                    section=section,
                    priority="medium"
                ))
                break
        
        # Check sentence length
        sentences = re.split(r'[.!?]+', text)
        long_sentences = [s for s in sentences if len(s.split()) > 25]
        
        if long_sentences:
            suggestions.append(OptimizationSuggestion(
                type=OptimizationType.CLARITY,
                original_text="long sentences detected",
                suggested_text="break into shorter sentences",
                confidence=0.7,
                explanation="Break long sentences into shorter ones for better readability",
                section=section,
                priority="low"
            ))
        
        return suggestions
    
    def _analyze_action_verbs(self, text: str, section: str) -> List[OptimizationSuggestion]:
        """Analyze and suggest better action verbs"""
        suggestions = []
        
        if section not in ["experience", "achievements"]:
            return suggestions
        
        # Extract sentences/bullet points
        sentences = self._extract_sentences(text)
        
        action_verbs = self.keyword_db.get_action_verbs()
        weak_starts = ["responsible", "worked", "helped", "assisted", "was", "were"]
        
        for sentence in sentences:
            first_word = sentence.split()[0].lower() if sentence.split() else ""
            
            # Check if starts with weak word
            if first_word in weak_starts:
                # Suggest strong action verbs based on context
                context_verbs = self._suggest_context_appropriate_verbs(sentence)
                
                suggestions.append(OptimizationSuggestion(
                    type=OptimizationType.ACTION_VERBS,
                    original_text=sentence[:50] + "...",
                    suggested_text=f"Start with: {', '.join(context_verbs[:3])}",
                    confidence=0.8,
                    explanation=f"Replace weak opening '{first_word}' with strong action verb",
                    section=section,
                    priority="high"
                ))
            
            # Check if already uses action verbs
            elif first_word.capitalize() in action_verbs:
                continue  # Good - already using action verbs
            
            else:
                # Suggest adding action verbs
                context_verbs = self._suggest_context_appropriate_verbs(sentence)
                
                suggestions.append(OptimizationSuggestion(
                    type=OptimizationType.ACTION_VERBS,
                    original_text=sentence[:50] + "...",
                    suggested_text=f"Consider starting with: {', '.join(context_verbs[:3])}",
                    confidence=0.6,
                    explanation="Start bullet points with strong action verbs",
                    section=section,
                    priority="medium"
                ))
        
        return suggestions
    
    def _analyze_quantification(self, text: str, section: str) -> List[OptimizationSuggestion]:
        """Analyze quantification and suggest adding metrics"""
        suggestions = []
        
        if section not in ["experience", "achievements", "summary"]:
            return suggestions
        
        # Count existing metrics
        metric_count = 0
        for pattern in self.metric_patterns:
            metric_count += len(re.findall(pattern, text))
        
        sentences = self._extract_sentences(text)
        
        # If few metrics, suggest adding them
        if metric_count < len(sentences) * 0.3:  # Less than 30% have metrics
            suggestions.append(OptimizationSuggestion(
                type=OptimizationType.QUANTIFICATION,
                original_text="content lacks specific metrics",
                suggested_text="add numbers, percentages, or timeframes",
                confidence=0.9,
                explanation="Add specific metrics to quantify your achievements (e.g., '25% increase', '$50K budget', '10-person team')",
                section=section,
                priority="high"
            ))
        
        # Suggest specific metric types based on content
        metric_suggestions = self._suggest_metric_types(text)
        for suggestion in metric_suggestions:
            suggestions.append(OptimizationSuggestion(
                type=OptimizationType.QUANTIFICATION,
                original_text=suggestion["context"],
                suggested_text=suggestion["suggestion"],
                confidence=suggestion["confidence"],
                explanation=suggestion["explanation"],
                section=section,
                priority=suggestion["priority"]
            ))
        
        return suggestions
    
    def _analyze_keywords(self, text: str, section: str, industry: str) -> List[OptimizationSuggestion]:
        """Analyze industry keyword usage"""
        suggestions = []
        
        industry_keywords = self.keyword_db.get_keywords_for_industry(industry)
        if not industry_keywords:
            return suggestions
        
        # Count keyword usage
        text_lower = text.lower()
        used_keywords = [kw for kw in industry_keywords if kw.lower() in text_lower]
        keyword_density = len(used_keywords) / len(industry_keywords) if industry_keywords else 0
        
        # If keyword density is low, suggest adding relevant keywords
        if keyword_density < 0.1:  # Less than 10% keyword usage
            # Suggest most relevant keywords based on context
            relevant_keywords = self._suggest_relevant_keywords(text, industry_keywords)
            
            suggestions.append(OptimizationSuggestion(
                type=OptimizationType.ATS_KEYWORDS,
                original_text="low industry keyword density",
                suggested_text=f"Consider adding: {', '.join(relevant_keywords[:5])}",
                confidence=0.8,
                explanation=f"Add relevant {industry} keywords to improve ATS compatibility",
                section=section,
                priority="high"
            ))
        
        return suggestions
    
    def _analyze_impact(self, text: str, section: str) -> List[OptimizationSuggestion]:
        """Analyze impact and achievement focus"""
        suggestions = []
        
        if section not in ["experience", "achievements", "summary"]:
            return suggestions
        
        # Check for result-oriented language
        impact_indicators = [
            "increased", "decreased", "improved", "enhanced", "optimized",
            "achieved", "exceeded", "delivered", "reduced", "saved",
            "generated", "created", "built", "launched", "implemented"
        ]
        
        text_lower = text.lower()
        impact_count = sum(1 for indicator in impact_indicators if indicator in text_lower)
        
        sentences = self._extract_sentences(text)
        impact_ratio = impact_count / len(sentences) if sentences else 0
        
        # If low impact language, suggest improvements
        if impact_ratio < 0.3:  # Less than 30% impact-focused
            suggestions.append(OptimizationSuggestion(
                type=OptimizationType.IMPACT,
                original_text="content lacks impact focus",
                suggested_text="emphasize results and achievements",
                confidence=0.8,
                explanation="Focus on results and impact rather than just responsibilities",
                section=section,
                priority="high"
            ))
        
        # Check for task-focused vs. achievement-focused language
        task_indicators = ["responsible for", "duties included", "worked on", "managed"]
        task_count = sum(1 for task in task_indicators if task in text_lower)
        
        if task_count > impact_count:
            suggestions.append(OptimizationSuggestion(
                type=OptimizationType.IMPACT,
                original_text="too task-focused",
                suggested_text="shift focus to achievements and results",
                confidence=0.9,
                explanation="Transform task descriptions into achievement statements",
                section=section,
                priority="high"
            ))
        
        return suggestions
    
    def _extract_sentences(self, text: str) -> List[str]:
        """Extract sentences or bullet points from text"""
        # Split by bullet points or sentences
        sentences = re.split(r'[•\-\*]|\n|\.(?=\s|$)', text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
        return sentences
    
    def _suggest_context_appropriate_verbs(self, sentence: str) -> List[str]:
        """Suggest action verbs based on sentence context"""
        sentence_lower = sentence.lower()
        
        if any(word in sentence_lower for word in ["team", "people", "staff", "group"]):
            return self.keyword_db.get_action_verbs("leadership")
        elif any(word in sentence_lower for word in ["increase", "improve", "achieve", "deliver"]):
            return self.keyword_db.get_action_verbs("achievement")
        elif any(word in sentence_lower for word in ["create", "build", "develop", "design"]):
            return self.keyword_db.get_action_verbs("creation")
        elif any(word in sentence_lower for word in ["analyze", "research", "evaluate", "assess"]):
            return self.keyword_db.get_action_verbs("analysis")
        elif any(word in sentence_lower for word in ["present", "communicate", "train", "negotiate"]):
            return self.keyword_db.get_action_verbs("communication")
        else:
            return self.keyword_db.get_action_verbs("achievement")  # Default to achievement verbs
    
    def _suggest_metric_types(self, text: str) -> List[Dict[str, Any]]:
        """Suggest specific types of metrics to add"""
        suggestions = []
        text_lower = text.lower()
        
        metric_suggestions_map = {
            "budget": {
                "keywords": ["budget", "cost", "expense", "financial", "money"],
                "suggestion": "Add budget amounts (e.g., '$50K budget', '15% cost reduction')",
                "confidence": 0.8,
                "priority": "high"
            },
            "team": {
                "keywords": ["team", "staff", "people", "group", "members"],
                "suggestion": "Add team size (e.g., 'team of 8', '25-person department')",
                "confidence": 0.9,
                "priority": "high"
            },
            "time": {
                "keywords": ["project", "deadline", "timeline", "schedule"],
                "suggestion": "Add timeframes (e.g., '6-month project', 'within 2 weeks')",
                "confidence": 0.8,
                "priority": "medium"
            },
            "performance": {
                "keywords": ["improve", "increase", "enhance", "optimize", "boost"],
                "suggestion": "Add performance metrics (e.g., '25% improvement', '40% faster')",
                "confidence": 0.9,
                "priority": "high"
            },
            "volume": {
                "keywords": ["customers", "users", "clients", "sales", "revenue"],
                "suggestion": "Add volume metrics (e.g., '500+ customers', '1M+ users')",
                "confidence": 0.8,
                "priority": "high"
            }
        }
        
        for metric_type, info in metric_suggestions_map.items():
            if any(keyword in text_lower for keyword in info["keywords"]):
                suggestions.append({
                    "context": f"mentions {metric_type}",
                    "suggestion": info["suggestion"],
                    "confidence": info["confidence"],
                    "explanation": f"Quantify {metric_type}-related achievements with specific numbers",
                    "priority": info["priority"]
                })
        
        return suggestions
    
    def _suggest_relevant_keywords(self, text: str, keywords: List[str]) -> List[str]:
        """Suggest most relevant keywords based on text content"""
        text_lower = text.lower()
        
        # Score keywords based on context relevance
        keyword_scores = {}
        
        for keyword in keywords:
            score = 0
            keyword_lower = keyword.lower()
            
            # Exact match
            if keyword_lower in text_lower:
                score += 10
                continue  # Already present
            
            # Partial match or related terms
            keyword_words = keyword_lower.split()
            for word in keyword_words:
                if word in text_lower:
                    score += 3
            
            # Context-based scoring
            if any(related in text_lower for related in self._get_related_terms(keyword_lower)):
                score += 2
            
            if score > 0:
                keyword_scores[keyword] = score
        
        # Return top scored keywords
        sorted_keywords = sorted(keyword_scores.items(), key=lambda x: x[1], reverse=True)
        return [kw[0] for kw in sorted_keywords[:10]]
    
    def _get_related_terms(self, keyword: str) -> List[str]:
        """Get related terms for a keyword"""
        related_terms_map = {
            "javascript": ["js", "web", "frontend", "react", "node"],
            "python": ["programming", "script", "automation", "data"],
            "management": ["manage", "lead", "supervise", "direct"],
            "analysis": ["analyze", "data", "research", "evaluate"],
            "marketing": ["campaign", "brand", "promotion", "advertising"],
            "sales": ["revenue", "customer", "client", "business"],
        }
        
        return related_terms_map.get(keyword.lower(), [])
    
    def _calculate_metrics(self, text: str, industry: str) -> Dict[str, Any]:
        """Calculate various content metrics"""
        words = text.split()
        sentences = self._extract_sentences(text)
        
        # Basic metrics
        word_count = len(words)
        sentence_count = len(sentences)
        avg_sentence_length = word_count / sentence_count if sentence_count else 0
        
        # Quantification metrics
        metric_count = 0
        for pattern in self.metric_patterns:
            metric_count += len(re.findall(pattern, text))
        
        quantification_ratio = metric_count / sentence_count if sentence_count else 0
        
        # Action verb metrics
        action_verbs = self.keyword_db.get_action_verbs()
        action_verb_count = sum(1 for word in words if word.capitalize() in action_verbs)
        action_verb_ratio = action_verb_count / sentence_count if sentence_count else 0
        
        # Industry keyword metrics
        industry_keywords = self.keyword_db.get_keywords_for_industry(industry)
        keyword_count = sum(1 for kw in industry_keywords if kw.lower() in text.lower())
        keyword_density = keyword_count / len(industry_keywords) if industry_keywords else 0
        
        # Readability (simplified)
        readability_score = max(0, min(100, 100 - (avg_sentence_length - 15) * 2))
        
        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "avg_sentence_length": round(avg_sentence_length, 1),
            "metric_count": metric_count,
            "quantification_ratio": round(quantification_ratio, 2),
            "action_verb_count": action_verb_count,
            "action_verb_ratio": round(action_verb_ratio, 2),
            "keyword_count": keyword_count,
            "keyword_density": round(keyword_density, 2),
            "readability_score": round(readability_score)
        }
    
    def _calculate_score(self, suggestions: List[OptimizationSuggestion], metrics: Dict[str, Any]) -> int:
        """Calculate overall content score (0-100)"""
        base_score = 100
        
        # Deduct points for suggestions
        for suggestion in suggestions:
            if suggestion.priority == "high":
                base_score -= 15
            elif suggestion.priority == "medium":
                base_score -= 10
            else:
                base_score -= 5
        
        # Add points for good metrics
        if metrics["quantification_ratio"] > 0.5:
            base_score += 10
        
        if metrics["action_verb_ratio"] > 0.8:
            base_score += 10
        
        if metrics["keyword_density"] > 0.15:
            base_score += 10
        
        if 10 <= metrics["avg_sentence_length"] <= 20:
            base_score += 5
        
        return max(0, min(100, base_score))
    
    def _identify_strengths_weaknesses(self, text: str, suggestions: List[OptimizationSuggestion], 
                                     metrics: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """Identify content strengths and weaknesses"""
        strengths = []
        weaknesses = []
        
        # Analyze strengths
        if metrics["quantification_ratio"] > 0.4:
            strengths.append("Good use of quantifiable metrics")
        
        if metrics["action_verb_ratio"] > 0.7:
            strengths.append("Strong action verbs throughout")
        
        if metrics["keyword_density"] > 0.1:
            strengths.append("Industry-relevant keywords present")
        
        if 12 <= metrics["avg_sentence_length"] <= 18:
            strengths.append("Good sentence length for readability")
        
        if metrics["readability_score"] > 70:
            strengths.append("Clear and readable content")
        
        # Analyze weaknesses based on suggestions
        suggestion_types = [s.type for s in suggestions]
        
        if OptimizationType.QUANTIFICATION in suggestion_types:
            weaknesses.append("Lacks specific metrics and numbers")
        
        if OptimizationType.ACTION_VERBS in suggestion_types:
            weaknesses.append("Could use stronger action verbs")
        
        if OptimizationType.ATS_KEYWORDS in suggestion_types:
            weaknesses.append("Missing industry-relevant keywords")
        
        if OptimizationType.CLARITY in suggestion_types:
            weaknesses.append("Could improve clarity and impact")
        
        if OptimizationType.IMPACT in suggestion_types:
            weaknesses.append("Focus more on achievements than tasks")
        
        # Default messages if none found
        if not strengths:
            strengths.append("Content is well-structured")
        
        if not weaknesses and not suggestions:
            strengths.append("Excellent content quality")
        
        return strengths, weaknesses

class AIOptimizationService:
    """
    Main AI optimization service that coordinates all optimization features
    """
    
    def __init__(self):
        self.content_analyzer = ContentAnalyzer()
        
        # Free AI API endpoints (you can add your own API keys)
        self.ai_endpoints = {
            "huggingface": "https://api-inference.huggingface.co/models/",
            "openai_compatible": None,  # Add your own OpenAI-compatible endpoint
        }
    
    async def optimize_cv_content(self, cv_data: Dict[str, Any], 
                                 job_description: str = "", 
                                 industry: str = "general") -> Dict[str, Any]:
        """Comprehensive CV content optimization"""
        optimization_results = {
            "overall_score": 0,
            "section_analyses": {},
            "global_suggestions": [],
            "improved_content": {},
            "ats_compatibility": {}
        }
        
        sections_to_analyze = [
            ("professional_summary", "summary"),
            ("work_experience", "experience"),
            ("education", "education"),
            ("skills", "skills")
        ]
        
        all_suggestions = []
        section_scores = []
        
        # Analyze each section
        for section_key, section_type in sections_to_analyze:
            if section_key in cv_data and cv_data[section_key]:
                text = self._extract_text_from_section(cv_data[section_key], section_key)
                
                if text.strip():
                    analysis = self.content_analyzer.analyze_content(text, section_type, industry)
                    
                    optimization_results["section_analyses"][section_key] = {
                        "score": analysis.score,
                        "suggestions": [self._suggestion_to_dict(s) for s in analysis.suggestions],
                        "metrics": analysis.metrics,
                        "strengths": analysis.strengths,
                        "weaknesses": analysis.weaknesses
                    }
                    
                    all_suggestions.extend(analysis.suggestions)
                    section_scores.append(analysis.score)
        
        # Calculate overall score
        optimization_results["overall_score"] = sum(section_scores) // len(section_scores) if section_scores else 0
        
        # Generate global suggestions
        optimization_results["global_suggestions"] = self._generate_global_suggestions(all_suggestions, cv_data)
        
        # Generate improved content using AI
        if job_description:
            optimization_results["improved_content"] = await self._generate_improved_content(
                cv_data, job_description, all_suggestions
            )
        
        # ATS compatibility analysis
        optimization_results["ats_compatibility"] = self._analyze_ats_compatibility(cv_data, industry)
        
        return optimization_results
    
    def _extract_text_from_section(self, section_data: Any, section_key: str) -> str:
        """Extract text content from different section types"""
        if isinstance(section_data, str):
            return section_data
        
        if isinstance(section_data, list):
            text_parts = []
            for item in section_data:
                if isinstance(item, dict):
                    if section_key == "work_experience":
                        # Extract job title, company, and achievements
                        parts = [
                            item.get("job_title", ""),
                            item.get("company", ""),
                            " ".join(item.get("achievements", []))
                        ]
                        text_parts.extend([p for p in parts if p])
                    
                    elif section_key == "education":
                        # Extract degree and institution
                        parts = [
                            item.get("degree", ""),
                            item.get("institution", "")
                        ]
                        text_parts.extend([p for p in parts if p])
                    
                    else:
                        # Generic extraction
                        for value in item.values():
                            if isinstance(value, str):
                                text_parts.append(value)
                            elif isinstance(value, list):
                                text_parts.extend([str(v) for v in value])
                
                elif isinstance(item, str):
                    text_parts.append(item)
            
            return " ".join(text_parts)
        
        if isinstance(section_data, dict):
            if section_key == "skills":
                # Extract all skills
                all_skills = []
                for skill_list in section_data.values():
                    if isinstance(skill_list, list):
                        all_skills.extend(skill_list)
                return " ".join(all_skills)
            else:
                # Generic dict extraction
                text_parts = []
                for value in section_data.values():
                    if isinstance(value, str):
                        text_parts.append(value)
                    elif isinstance(value, list):
                        text_parts.extend([str(v) for v in value])
                return " ".join(text_parts)
        
        return str(section_data)
    
    def _suggestion_to_dict(self, suggestion: OptimizationSuggestion) -> Dict[str, Any]:
        """Convert OptimizationSuggestion to dictionary"""
        return {
            "type": suggestion.type.value,
            "original_text": suggestion.original_text,
            "suggested_text": suggestion.suggested_text,
            "confidence": suggestion.confidence,
            "explanation": suggestion.explanation,
            "section": suggestion.section,
            "priority": suggestion.priority
        }
    
    def _generate_global_suggestions(self, all_suggestions: List[OptimizationSuggestion], 
                                   cv_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate high-level suggestions for the entire CV"""
        global_suggestions = []
        
        # Count suggestion types
        suggestion_counts = {}
        for suggestion in all_suggestions:
            suggestion_counts[suggestion.type] = suggestion_counts.get(suggestion.type, 0) + 1
        
        # Generate global recommendations
        if suggestion_counts.get(OptimizationType.QUANTIFICATION, 0) > 2:
            global_suggestions.append({
                "type": "quantification",
                "priority": "high",
                "title": "Add More Metrics",
                "description": "Your CV would benefit from more specific numbers and metrics to quantify your achievements.",
                "examples": ["25% increase in sales", "$50K budget managed", "Team of 8 developers"]
            })
        
        if suggestion_counts.get(OptimizationType.ACTION_VERBS, 0) > 2:
            global_suggestions.append({
                "type": "action_verbs",
                "priority": "high", 
                "title": "Strengthen Action Verbs",
                "description": "Start more bullet points with strong action verbs to create greater impact.",
                "examples": ["Led", "Achieved", "Implemented", "Optimized", "Delivered"]
            })
        
        if suggestion_counts.get(OptimizationType.ATS_KEYWORDS, 0) > 1:
            global_suggestions.append({
                "type": "ats_keywords",
                "priority": "medium",
                "title": "Improve ATS Compatibility", 
                "description": "Add more industry-relevant keywords to improve your CV's compatibility with Applicant Tracking Systems.",
                "examples": ["Include relevant technologies", "Add industry buzzwords", "Use job posting keywords"]
            })
        
        return global_suggestions
    
    async def _generate_improved_content(self, cv_data: Dict[str, Any], 
                                       job_description: str,
                                       suggestions: List[OptimizationSuggestion]) -> Dict[str, Any]:
        """Generate improved content using AI (free implementation)"""
        improved_content = {}
        
        # For now, provide rule-based improvements
        # In a full implementation, you could integrate with free AI APIs
        
        # Improve professional summary
        if "professional_summary" in cv_data:
            improved_summary = self._improve_summary_rule_based(
                cv_data["professional_summary"], 
                job_description,
                suggestions
            )
            improved_content["professional_summary"] = improved_summary
        
        # Improve work experience
        if "work_experience" in cv_data:
            improved_experience = self._improve_experience_rule_based(
                cv_data["work_experience"],
                suggestions
            )
            improved_content["work_experience"] = improved_experience
        
        return improved_content
    
    def _improve_summary_rule_based(self, original_summary: str, 
                                  job_description: str,
                                  suggestions: List[OptimizationSuggestion]) -> str:
        """Improve summary using rule-based approach"""
        improved = original_summary
        
        # Extract key terms from job description
        if job_description:
            job_keywords = self._extract_key_terms(job_description)
            
            # Add relevant keywords if missing
            for keyword in job_keywords[:3]:
                if keyword.lower() not in improved.lower():
                    improved = improved.replace(".", f" with expertise in {keyword}.")
                    break
        
        # Apply suggestions
        for suggestion in suggestions:
            if suggestion.section == "summary":
                if suggestion.type == OptimizationType.CLARITY:
                    # Replace weak phrases
                    if suggestion.original_text in improved:
                        improved = improved.replace(suggestion.original_text, suggestion.suggested_text)
        
        return improved
    
    def _improve_experience_rule_based(self, experience_list: List[Dict[str, Any]],
                                     suggestions: List[OptimizationSuggestion]) -> List[Dict[str, Any]]:
        """Improve experience entries using rule-based approach"""
        improved_experience = []
        
        for exp in experience_list:
            improved_exp = exp.copy()
            
            if "achievements" in improved_exp:
                improved_achievements = []
                
                for achievement in improved_exp["achievements"]:
                    improved_achievement = achievement
                    
                    # Apply action verb improvements
                    for suggestion in suggestions:
                        if suggestion.section == "experience" and suggestion.type == OptimizationType.ACTION_VERBS:
                            # Replace weak starts with strong action verbs
                            weak_starts = ["responsible for", "worked on", "helped with"]
                            for weak in weak_starts:
                                if achievement.lower().startswith(weak):
                                    action_verbs = ["Led", "Managed", "Developed", "Implemented"]
                                    import random
                                    new_verb = random.choice(action_verbs)
                                    improved_achievement = achievement.replace(weak, new_verb, 1)
                                    break
                    
                    improved_achievements.append(improved_achievement)
                
                improved_exp["achievements"] = improved_achievements
            
            improved_experience.append(improved_exp)
        
        return improved_experience
    
    def _extract_key_terms(self, text: str) -> List[str]:
        """Extract key terms from text (simplified implementation)"""
        # Remove common words
        common_words = {
            "the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with",
            "by", "from", "up", "about", "into", "through", "during", "before",
            "after", "above", "below", "between", "among", "this", "that", "these",
            "those", "i", "me", "my", "myself", "we", "our", "ours", "ourselves",
            "you", "your", "yours", "yourself", "yourselves", "he", "him", "his",
            "himself", "she", "her", "hers", "herself", "it", "its", "itself",
            "they", "them", "their", "theirs", "themselves", "what", "which",
            "who", "whom", "this", "that", "these", "those", "am", "is", "are",
            "was", "were", "be", "been", "being", "have", "has", "had", "having",
            "do", "does", "did", "doing", "a", "an", "will", "would", "should",
            "could", "can", "may", "might", "must", "shall"
        }
        
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        key_terms = []
        
        for word in words:
            if (len(word) > 3 and 
                word not in common_words and
                word not in key_terms):
                key_terms.append(word.capitalize())
        
        return key_terms[:10]  # Return top 10 key terms
    
    def _analyze_ats_compatibility(self, cv_data: Dict[str, Any], industry: str) -> Dict[str, Any]:
        """Analyze ATS compatibility"""
        ats_score = 100
        issues = []
        recommendations = []
        
        # Check for standard section names
        standard_sections = ["professional_summary", "work_experience", "education", "skills"]
        for section in standard_sections:
            if section not in cv_data:
                ats_score -= 10
                issues.append(f"Missing standard section: {section}")
        
        # Check for industry keywords
        if industry != "general":
            keyword_db = IndustryKeywordDatabase()
            industry_keywords = keyword_db.get_keywords_for_industry(industry)
            
            if industry_keywords:
                cv_text = str(cv_data).lower()
                keyword_count = sum(1 for kw in industry_keywords if kw.lower() in cv_text)
                keyword_ratio = keyword_count / len(industry_keywords)
                
                if keyword_ratio < 0.1:
                    ats_score -= 20
                    issues.append("Low industry keyword density")
                    recommendations.append(f"Add more {industry} industry keywords")
        
        # Check for proper formatting
        if "work_experience" in cv_data:
            for exp in cv_data["work_experience"]:
                if not exp.get("job_title"):
                    ats_score -= 5
                    issues.append("Missing job titles")
                if not exp.get("company"):
                    ats_score -= 5
                    issues.append("Missing company names")
        
        # Generate recommendations
        if ats_score < 80:
            recommendations.extend([
                "Use standard section headings",
                "Include relevant keywords from job postings",
                "Ensure all dates and company names are properly formatted",
                "Use simple, clean formatting without tables or graphics"
            ])
        
        return {
            "score": max(0, ats_score),
            "issues": issues,
            "recommendations": recommendations,
            "keyword_suggestions": keyword_db.get_keywords_for_industry(industry)[:10] if industry != "general" else []
        }

# Global service instance
ai_optimization_service = AIOptimizationService()
"""
Auto-Layout Algorithm for Optimal CV Formatting
Free and open-source intelligent layout system for professional CVs
"""

import math
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class LayoutType(Enum):
    SINGLE_COLUMN = "single_column"
    TWO_COLUMN = "two_column"
    MODERN_SIDEBAR = "modern_sidebar"
    EXECUTIVE = "executive"
    ACADEMIC = "academic"
    CREATIVE = "creative"

class SectionPriority(Enum):
    CRITICAL = 1  # Must fit on first page
    HIGH = 2      # Should fit on first page
    MEDIUM = 3    # Can overflow to second page
    LOW = 4       # Can be minimized or moved

@dataclass
class PageConstraints:
    width_mm: float = 210  # A4 width
    height_mm: float = 297  # A4 height
    margin_top_mm: float = 20
    margin_bottom_mm: float = 20
    margin_left_mm: float = 20
    margin_right_mm: float = 20
    
    @property
    def content_width_mm(self) -> float:
        return self.width_mm - self.margin_left_mm - self.margin_right_mm
    
    @property
    def content_height_mm(self) -> float:
        return self.height_mm - self.margin_top_mm - self.margin_bottom_mm

@dataclass
class SectionDimensions:
    section_id: str
    section_type: str
    priority: SectionPriority
    min_height_mm: float
    preferred_height_mm: float
    max_height_mm: float
    can_split: bool = False
    items_count: int = 0
    
@dataclass
class LayoutElement:
    element_id: str
    element_type: str  # header, section, item, spacer
    x_mm: float
    y_mm: float
    width_mm: float
    height_mm: float
    page_number: int
    z_index: int = 0

@dataclass
class LayoutResult:
    pages: List[List[LayoutElement]]
    total_pages: int
    overflow_sections: List[str]
    layout_score: float
    recommendations: List[str]

class ContentMeasurer:
    """
    Estimates content dimensions for layout calculations
    """
    
    def __init__(self):
        # Standard typography measurements (approximate)
        self.font_sizes = {
            "header_name": {"size": 24, "line_height": 1.3},
            "header_title": {"size": 16, "line_height": 1.3},
            "section_title": {"size": 14, "line_height": 1.4},
            "body_text": {"size": 11, "line_height": 1.5},
            "small_text": {"size": 9, "line_height": 1.4}
        }
        
        # Approximate character widths (in mm for different font sizes)
        self.char_widths = {
            24: 4.8,  # Header name
            16: 3.2,  # Header title
            14: 2.8,  # Section titles
            11: 2.2,  # Body text
            9: 1.8    # Small text
        }
    
    def estimate_text_height(self, text: str, font_size: int, 
                           max_width_mm: float, line_height: float = 1.5) -> float:
        """Estimate height needed for text block"""
        if not text:
            return 0
        
        char_width = self.char_widths.get(font_size, 2.2)
        chars_per_line = int(max_width_mm / char_width)
        
        if chars_per_line <= 0:
            return font_size * 0.35  # Fallback: 1 line
        
        lines_needed = math.ceil(len(text) / chars_per_line)
        line_height_mm = font_size * 0.35 * line_height  # Convert pt to mm
        
        return lines_needed * line_height_mm
    
    def estimate_list_height(self, items: List[str], font_size: int,
                           max_width_mm: float, line_height: float = 1.5) -> float:
        """Estimate height needed for a list of items"""
        if not items:
            return 0
        
        total_height = 0
        for item in items:
            item_height = self.estimate_text_height(item, font_size, max_width_mm, line_height)
            total_height += item_height + 2  # Add 2mm spacing between items
        
        return total_height
    
    def estimate_header_height(self, personal_details: Dict[str, Any], 
                             layout_type: LayoutType, max_width_mm: float) -> float:
        """Estimate header section height"""
        height = 0
        
        # Name
        name = personal_details.get("full_name", "")
        if name:
            name_height = self.estimate_text_height(name, 24, max_width_mm, 1.3)
            height += name_height + 5  # 5mm spacing
        
        # Title/Position
        position = personal_details.get("desired_position", "")
        if position:
            position_height = self.estimate_text_height(position, 16, max_width_mm, 1.3)
            height += position_height + 3  # 3mm spacing
        
        # Contact info (estimated as 2 lines)
        contact_info = [
            personal_details.get("email", ""),
            personal_details.get("phone", ""),
            personal_details.get("location", ""),
            personal_details.get("linkedin_url", "")
        ]
        contact_items = [item for item in contact_info if item]
        
        if contact_items:
            # Assume 2-3 lines for contact info
            contact_lines = math.ceil(len(contact_items) / 2)
            contact_height = contact_lines * (11 * 0.35 * 1.4)  # 11pt font
            height += contact_height + 5  # 5mm spacing
        
        # Add padding for header background/styling
        height += 20  # 20mm total padding
        
        return height

class SectionAnalyzer:
    """
    Analyzes CV sections to determine layout requirements
    """
    
    def __init__(self):
        self.measurer = ContentMeasurer()
        
        # Section priorities for layout optimization
        self.section_priorities = {
            "header": SectionPriority.CRITICAL,
            "professional_summary": SectionPriority.HIGH,
            "work_experience": SectionPriority.CRITICAL,
            "skills": SectionPriority.HIGH,
            "education": SectionPriority.MEDIUM,
            "projects": SectionPriority.MEDIUM,
            "certifications": SectionPriority.LOW,
            "awards": SectionPriority.LOW,
            "languages": SectionPriority.LOW,
            "interests": SectionPriority.LOW
        }
    
    def analyze_cv_sections(self, cv_data: Dict[str, Any], 
                           page_constraints: PageConstraints,
                           layout_type: LayoutType) -> List[SectionDimensions]:
        """Analyze all CV sections and estimate their dimensions"""
        sections = []
        content_width = page_constraints.content_width_mm
        
        # Adjust content width for two-column layouts
        if layout_type in [LayoutType.TWO_COLUMN, LayoutType.MODERN_SIDEBAR]:
            content_width = content_width * 0.65  # Main column width
        
        # Header section
        if "personal_details" in cv_data:
            header_height = self.measurer.estimate_header_height(
                cv_data["personal_details"], layout_type, content_width
            )
            sections.append(SectionDimensions(
                section_id="header",
                section_type="header",
                priority=SectionPriority.CRITICAL,
                min_height_mm=header_height * 0.8,
                preferred_height_mm=header_height,
                max_height_mm=header_height * 1.2,
                can_split=False
            ))
        
        # Professional Summary
        if cv_data.get("professional_summary"):
            summary_height = self._estimate_summary_height(
                cv_data["professional_summary"], content_width
            )
            sections.append(SectionDimensions(
                section_id="professional_summary",
                section_type="summary",
                priority=SectionPriority.HIGH,
                min_height_mm=summary_height * 0.9,
                preferred_height_mm=summary_height,
                max_height_mm=summary_height * 1.3,
                can_split=True
            ))
        
        # Work Experience
        if cv_data.get("work_experience"):
            exp_height, item_count = self._estimate_experience_height(
                cv_data["work_experience"], content_width
            )
            sections.append(SectionDimensions(
                section_id="work_experience",
                section_type="experience",
                priority=SectionPriority.CRITICAL,
                min_height_mm=exp_height * 0.7,  # Can condense achievements
                preferred_height_mm=exp_height,
                max_height_mm=exp_height * 1.4,
                can_split=True,
                items_count=item_count
            ))
        
        # Skills
        if cv_data.get("skills"):
            skills_height = self._estimate_skills_height(
                cv_data["skills"], content_width, layout_type
            )
            sections.append(SectionDimensions(
                section_id="skills",
                section_type="skills",
                priority=SectionPriority.HIGH,
                min_height_mm=skills_height * 0.8,
                preferred_height_mm=skills_height,
                max_height_mm=skills_height * 1.5,
                can_split=True
            ))
        
        # Education
        if cv_data.get("education"):
            edu_height, item_count = self._estimate_education_height(
                cv_data["education"], content_width
            )
            sections.append(SectionDimensions(
                section_id="education",
                section_type="education",
                priority=SectionPriority.MEDIUM,
                min_height_mm=edu_height * 0.9,
                preferred_height_mm=edu_height,
                max_height_mm=edu_height * 1.3,
                can_split=True,
                items_count=item_count
            ))
        
        # Projects (if present)
        if cv_data.get("projects"):
            projects_height = self._estimate_projects_height(
                cv_data["projects"], content_width
            )
            sections.append(SectionDimensions(
                section_id="projects",
                section_type="projects",
                priority=SectionPriority.MEDIUM,
                min_height_mm=projects_height * 0.8,
                preferred_height_mm=projects_height,
                max_height_mm=projects_height * 1.4,
                can_split=True
            ))
        
        return sections
    
    def _estimate_summary_height(self, summary: str, max_width_mm: float) -> float:
        """Estimate professional summary section height"""
        section_title_height = 14 * 0.35 * 1.4 + 8  # Title + spacing
        text_height = self.measurer.estimate_text_height(summary, 11, max_width_mm, 1.5)
        return section_title_height + text_height + 10  # 10mm section spacing
    
    def _estimate_experience_height(self, experience_list: List[Dict], 
                                  max_width_mm: float) -> Tuple[float, int]:
        """Estimate work experience section height"""
        section_title_height = 14 * 0.35 * 1.4 + 8  # Title + spacing
        total_height = section_title_height
        
        for exp in experience_list:
            # Job title and company (2 lines typically)
            job_info_height = 2 * (11 * 0.35 * 1.4) + 5  # 2 lines + spacing
            
            # Achievements
            achievements = exp.get("achievements", [])
            if achievements:
                achievements_height = self.measurer.estimate_list_height(
                    achievements, 11, max_width_mm - 10, 1.5  # Indent by 10mm
                )
                job_info_height += achievements_height
            
            # Dates and spacing
            job_info_height += 15  # Additional spacing between jobs
            total_height += job_info_height
        
        return total_height, len(experience_list)
    
    def _estimate_skills_height(self, skills: Dict, max_width_mm: float, 
                              layout_type: LayoutType) -> float:
        """Estimate skills section height"""
        section_title_height = 14 * 0.35 * 1.4 + 8  # Title + spacing
        
        if layout_type == LayoutType.TWO_COLUMN:
            # Skills in sidebar - more compact
            skills_height = len(skills) * 25  # 25mm per skill category
        else:
            # Skills in main column - grid layout
            total_skills = sum(len(skill_list) for skill_list in skills.values() if skill_list)
            skills_per_row = max(1, int(max_width_mm / 40))  # Assume 40mm per skill tag
            rows_needed = math.ceil(total_skills / skills_per_row)
            skills_height = rows_needed * 15 + len(skills) * 10  # 15mm per row, 10mm per category
        
        return section_title_height + skills_height + 10
    
    def _estimate_education_height(self, education_list: List[Dict], 
                                 max_width_mm: float) -> Tuple[float, int]:
        """Estimate education section height"""
        section_title_height = 14 * 0.35 * 1.4 + 8  # Title + spacing
        total_height = section_title_height
        
        for edu in education_list:
            # Degree, institution, dates (typically 3 lines)
            edu_height = 3 * (11 * 0.35 * 1.4) + 10  # 3 lines + spacing
            total_height += edu_height
        
        return total_height, len(education_list)
    
    def _estimate_projects_height(self, projects_list: List[Dict], 
                                max_width_mm: float) -> float:
        """Estimate projects section height"""
        section_title_height = 14 * 0.35 * 1.4 + 8  # Title + spacing
        total_height = section_title_height
        
        for project in projects_list:
            # Project title
            project_height = 11 * 0.35 * 1.4 + 3  # Title + spacing
            
            # Project description
            description = project.get("description", "")
            if description:
                desc_height = self.measurer.estimate_text_height(description, 10, max_width_mm, 1.4)
                project_height += desc_height
            
            # Technologies (if present)
            technologies = project.get("technologies", [])
            if technologies:
                tech_height = 10 * 0.35 * 1.4 + 5  # One line for tech tags
                project_height += tech_height
            
            project_height += 10  # Spacing between projects
            total_height += project_height
        
        return total_height

class LayoutOptimizer:
    """
    Optimizes CV layout using intelligent algorithms
    """
    
    def __init__(self):
        self.analyzer = SectionAnalyzer()
    
    def optimize_layout(self, cv_data: Dict[str, Any], 
                       layout_type: LayoutType = LayoutType.SINGLE_COLUMN,
                       page_constraints: PageConstraints = None) -> LayoutResult:
        """Optimize CV layout for best presentation"""
        
        if page_constraints is None:
            page_constraints = PageConstraints()
        
        # Analyze sections
        sections = self.analyzer.analyze_cv_sections(cv_data, page_constraints, layout_type)
        
        # Choose optimal layout strategy
        if layout_type == LayoutType.SINGLE_COLUMN:
            return self._optimize_single_column(sections, page_constraints)
        elif layout_type == LayoutType.TWO_COLUMN:
            return self._optimize_two_column(sections, page_constraints)
        elif layout_type == LayoutType.MODERN_SIDEBAR:
            return self._optimize_sidebar(sections, page_constraints)
        else:
            # Default to single column
            return self._optimize_single_column(sections, page_constraints)
    
    def _optimize_single_column(self, sections: List[SectionDimensions], 
                              constraints: PageConstraints) -> LayoutResult:
        """Optimize single-column layout"""
        pages = []
        current_page = []
        current_y = constraints.margin_top_mm
        page_number = 1
        overflow_sections = []
        
        available_height = constraints.content_height_mm
        
        for section in sections:
            # Check if section fits on current page
            if current_y + section.preferred_height_mm <= constraints.height_mm - constraints.margin_bottom_mm:
                # Section fits - add it
                element = LayoutElement(
                    element_id=section.section_id,
                    element_type="section",
                    x_mm=constraints.margin_left_mm,
                    y_mm=current_y,
                    width_mm=constraints.content_width_mm,
                    height_mm=section.preferred_height_mm,
                    page_number=page_number
                )
                current_page.append(element)
                current_y += section.preferred_height_mm + 5  # 5mm spacing between sections
            
            elif section.can_split and section.min_height_mm < available_height:
                # Try to fit minimum version
                element = LayoutElement(
                    element_id=section.section_id,
                    element_type="section",
                    x_mm=constraints.margin_left_mm,
                    y_mm=current_y,
                    width_mm=constraints.content_width_mm,
                    height_mm=section.min_height_mm,
                    page_number=page_number
                )
                current_page.append(element)
                current_y += section.min_height_mm + 5
                
                # Mark remaining content for next page
                if section.max_height_mm > section.min_height_mm:
                    overflow_sections.append(section.section_id)
            
            else:
                # Move to next page
                if current_page:
                    pages.append(current_page)
                
                current_page = []
                page_number += 1
                current_y = constraints.margin_top_mm
                
                # Add section to new page
                height_to_use = min(section.preferred_height_mm, available_height)
                element = LayoutElement(
                    element_id=section.section_id,
                    element_type="section",
                    x_mm=constraints.margin_left_mm,
                    y_mm=current_y,
                    width_mm=constraints.content_width_mm,
                    height_mm=height_to_use,
                    page_number=page_number
                )
                current_page.append(element)
                current_y += height_to_use + 5
        
        # Add last page
        if current_page:
            pages.append(current_page)
        
        # Calculate layout score
        layout_score = self._calculate_layout_score(pages, overflow_sections, sections)
        
        # Generate recommendations
        recommendations = self._generate_layout_recommendations(
            pages, overflow_sections, sections, layout_score
        )
        
        return LayoutResult(
            pages=pages,
            total_pages=len(pages),
            overflow_sections=overflow_sections,
            layout_score=layout_score,
            recommendations=recommendations
        )
    
    def _optimize_two_column(self, sections: List[SectionDimensions], 
                           constraints: PageConstraints) -> LayoutResult:
        """Optimize two-column layout"""
        # Separate sections into main column and sidebar
        main_sections = []
        sidebar_sections = []
        
        for section in sections:
            if section.section_type in ["header", "professional_summary", "work_experience"]:
                main_sections.append(section)
            else:
                sidebar_sections.append(section)
        
        # Layout main column (65% width)
        main_width = constraints.content_width_mm * 0.65
        main_constraints = PageConstraints(
            width_mm=main_width,
            height_mm=constraints.height_mm,
            margin_top_mm=constraints.margin_top_mm,
            margin_bottom_mm=constraints.margin_bottom_mm,
            margin_left_mm=constraints.margin_left_mm,
            margin_right_mm=5  # 5mm gap between columns
        )
        
        # Layout sidebar (30% width)
        sidebar_width = constraints.content_width_mm * 0.30
        sidebar_x = constraints.margin_left_mm + main_width + 10  # 10mm gap
        
        pages = []
        current_page = []
        
        # Layout main column
        current_y = constraints.margin_top_mm
        page_number = 1
        
        for section in main_sections:
            element = LayoutElement(
                element_id=section.section_id,
                element_type="section",
                x_mm=constraints.margin_left_mm,
                y_mm=current_y,
                width_mm=main_width,
                height_mm=section.preferred_height_mm,
                page_number=page_number
            )
            current_page.append(element)
            current_y += section.preferred_height_mm + 5
        
        # Layout sidebar
        sidebar_y = constraints.margin_top_mm + 60  # Start below header
        
        for section in sidebar_sections:
            element = LayoutElement(
                element_id=section.section_id,
                element_type="section",
                x_mm=sidebar_x,
                y_mm=sidebar_y,
                width_mm=sidebar_width,
                height_mm=section.preferred_height_mm,
                page_number=page_number
            )
            current_page.append(element)
            sidebar_y += section.preferred_height_mm + 5
        
        pages.append(current_page)
        
        layout_score = 85  # Two-column layouts generally score well
        
        return LayoutResult(
            pages=pages,
            total_pages=1,
            overflow_sections=[],
            layout_score=layout_score,
            recommendations=["Two-column layout provides good information density"]
        )
    
    def _optimize_sidebar(self, sections: List[SectionDimensions], 
                        constraints: PageConstraints) -> LayoutResult:
        """Optimize modern sidebar layout"""
        # Similar to two-column but with different proportions and styling
        return self._optimize_two_column(sections, constraints)
    
    def _calculate_layout_score(self, pages: List[List[LayoutElement]], 
                              overflow_sections: List[str],
                              sections: List[SectionDimensions]) -> float:
        """Calculate layout quality score (0-100)"""
        score = 100
        
        # Penalize multiple pages
        if len(pages) > 1:
            score -= (len(pages) - 1) * 15
        
        # Penalize overflow sections
        score -= len(overflow_sections) * 10
        
        # Check page utilization
        for page in pages:
            total_height = sum(element.height_mm for element in page)
            page_height = 297 - 40  # A4 minus margins
            utilization = total_height / page_height
            
            if utilization < 0.7:  # Under-utilized
                score -= 10
            elif utilization > 0.95:  # Over-packed
                score -= 15
        
        # Bonus for critical sections on first page
        if pages:
            first_page_sections = [elem.element_id for elem in pages[0]]
            critical_sections = [s.section_id for s in sections if s.priority == SectionPriority.CRITICAL]
            
            critical_on_first = len([s for s in critical_sections if s in first_page_sections])
            score += critical_on_first * 5
        
        return max(0, min(100, score))
    
    def _generate_layout_recommendations(self, pages: List[List[LayoutElement]],
                                       overflow_sections: List[str],
                                       sections: List[SectionDimensions],
                                       score: float) -> List[str]:
        """Generate layout improvement recommendations"""
        recommendations = []
        
        if len(pages) > 2:
            recommendations.append("Consider condensing content to fit within 2 pages")
        
        if overflow_sections:
            recommendations.append(f"Sections may be truncated: {', '.join(overflow_sections)}")
        
        if score < 70:
            recommendations.append("Layout could be optimized for better presentation")
        
        # Check section balance
        if pages:
            first_page_height = sum(elem.height_mm for elem in pages[0])
            if first_page_height > 250:  # Very full first page
                recommendations.append("Consider moving some content to second page for better balance")
        
        # Experience-specific recommendations
        experience_sections = [s for s in sections if s.section_type == "experience"]
        if experience_sections and experience_sections[0].items_count > 5:
            recommendations.append("Consider limiting work experience to 4-5 most relevant positions")
        
        if not recommendations:
            recommendations.append("Layout is well-optimized for readability and ATS compatibility")
        
        return recommendations

class ResponsiveLayoutService:
    """
    Service for responsive and adaptive layout generation
    """
    
    def __init__(self):
        self.optimizer = LayoutOptimizer()
    
    def generate_optimal_layout(self, cv_data: Dict[str, Any], 
                              target_format: str = "pdf",
                              experience_level: str = "mid",
                              industry: str = "general") -> LayoutResult:
        """Generate optimal layout based on content and context"""
        
        # Choose layout type based on content and experience level
        layout_type = self._choose_optimal_layout_type(cv_data, experience_level, industry)
        
        # Adjust page constraints based on target format
        constraints = self._get_format_constraints(target_format)
        
        # Optimize layout
        result = self.optimizer.optimize_layout(cv_data, layout_type, constraints)
        
        # Post-process for responsive adjustments
        result = self._apply_responsive_adjustments(result, cv_data)
        
        return result
    
    def _choose_optimal_layout_type(self, cv_data: Dict[str, Any], 
                                  experience_level: str, industry: str) -> LayoutType:
        """Choose optimal layout type based on content analysis"""
        
        # Count content sections
        work_experience_count = len(cv_data.get("work_experience", []))
        has_projects = bool(cv_data.get("projects"))
        has_certifications = bool(cv_data.get("certifications"))
        skills_count = sum(len(skills) for skills in cv_data.get("skills", {}).values())
        
        # For senior professionals with lots of content
        if experience_level == "senior" and work_experience_count >= 4:
            return LayoutType.EXECUTIVE
        
        # For creative industries
        if industry in ["creative", "design", "marketing"] and has_projects:
            return LayoutType.CREATIVE
        
        # For tech professionals with many skills
        if industry == "technology" and skills_count > 15:
            return LayoutType.TWO_COLUMN
        
        # For academic/research positions
        if industry in ["education", "research"] or cv_data.get("publications"):
            return LayoutType.ACADEMIC
        
        # Default to single column for simplicity and ATS compatibility
        return LayoutType.SINGLE_COLUMN
    
    def _get_format_constraints(self, target_format: str) -> PageConstraints:
        """Get page constraints based on target format"""
        if target_format == "pdf":
            return PageConstraints()  # Standard A4
        elif target_format == "letter":
            return PageConstraints(width_mm=215.9, height_mm=279.4)  # US Letter
        elif target_format == "web":
            return PageConstraints(width_mm=190, height_mm=1000, margin_left_mm=10, margin_right_mm=10)
        else:
            return PageConstraints()  # Default A4
    
    def _apply_responsive_adjustments(self, result: LayoutResult, 
                                    cv_data: Dict[str, Any]) -> LayoutResult:
        """Apply responsive adjustments to layout"""
        
        # If layout score is low, try alternative approaches
        if result.layout_score < 60:
            # Try condensing content
            result.recommendations.insert(0, "Consider condensing content for better layout")
            
            # Suggest content optimizations
            if len(result.pages) > 2:
                result.recommendations.append("Prioritize most relevant experience and skills")
        
        # Add mobile-friendly recommendations
        result.recommendations.append("Layout is optimized for both print and digital viewing")
        
        return result

# Global service instance
layout_service = ResponsiveLayoutService()